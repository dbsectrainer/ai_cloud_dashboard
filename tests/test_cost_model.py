"""Tests for TCO calculation service."""

import pytest

from src.services.cost_model import (
    ComputeResource,
    PricingModel,
    TCOCalculator,
    TCOInputs,
)


class TestTCOCalculator:
    """Test cases for TCO calculator."""

    @pytest.fixture
    def calculator(self):
        """Create calculator instance."""
        return TCOCalculator()

    @pytest.fixture
    def base_compute(self):
        """Base compute resource."""
        return ComputeResource(vcpu=4, memory_gb=16, storage_gb=100, quantity=10)

    def test_on_demand_calculation(self, calculator, base_compute):
        """Test basic on-demand TCO calculation."""
        inputs = TCOInputs(
            base_hourly_rate=0.10,
            compute=base_compute,
            pricing_model=PricingModel.ON_DEMAND,
            years=3,
        )

        result = calculator.calculate(inputs)

        # Verify basic calculations
        assert result.total_cost > 0
        assert result.monthly_cost > 0
        assert result.yearly_cost > 0
        assert result.effective_hourly_rate == 0.10  # No discount for on-demand

        # Verify monthly cost calculation
        # 10 instances * $0.10/hr * 730 hrs/month = $730/month
        expected_monthly_compute = 730.0
        assert abs(result.monthly_cost - expected_monthly_compute) < 1.0

    def test_reserved_instance_discount(self, calculator, base_compute):
        """Test that reserved instances get appropriate discounts."""
        base_inputs = TCOInputs(
            base_hourly_rate=0.10,
            compute=base_compute,
            pricing_model=PricingModel.ON_DEMAND,
            years=3,
        )

        on_demand_result = calculator.calculate(base_inputs)

        # Test 1-year reserved
        reserved_1y_inputs = TCOInputs(
            base_hourly_rate=0.10,
            compute=base_compute,
            pricing_model=PricingModel.RESERVED_1Y,
            years=3,
        )
        reserved_1y_result = calculator.calculate(reserved_1y_inputs)

        # Should be cheaper than on-demand
        assert reserved_1y_result.total_cost < on_demand_result.total_cost

        # Test 3-year reserved (should be cheapest)
        reserved_3y_inputs = TCOInputs(
            base_hourly_rate=0.10,
            compute=base_compute,
            pricing_model=PricingModel.RESERVED_3Y,
            years=3,
        )
        reserved_3y_result = calculator.calculate(reserved_3y_inputs)

        assert reserved_3y_result.total_cost < reserved_1y_result.total_cost
        assert reserved_3y_result.total_cost < on_demand_result.total_cost

    def test_storage_costs(self, calculator, base_compute):
        """Test storage cost calculations."""
        inputs = TCOInputs(
            base_hourly_rate=0.10,
            compute=base_compute,
            pricing_model=PricingModel.ON_DEMAND,
            years=1,
            storage_cost_gb_month=0.10,  # $0.10 per GB/month
        )

        result = calculator.calculate(inputs)

        # 100 GB * 10 instances * $0.10/GB/month * 12 months = $1200
        expected_storage = 1200.0
        assert abs(result.storage_cost - expected_storage) < 1.0

    def test_data_transfer_costs(self, calculator, base_compute):
        """Test data transfer cost calculations."""
        inputs = TCOInputs(
            base_hourly_rate=0.10,
            compute=base_compute,
            pricing_model=PricingModel.ON_DEMAND,
            years=1,
            data_transfer_tb_month=10.0,  # 10 TB/month
        )

        result = calculator.calculate(inputs)

        # 10 TB * 1024 GB/TB * $0.09/GB * 12 months
        assert result.data_transfer_cost > 0

    def test_support_costs(self, calculator, base_compute):
        """Test support cost calculations."""
        inputs = TCOInputs(
            base_hourly_rate=0.10,
            compute=base_compute,
            pricing_model=PricingModel.ON_DEMAND,
            years=1,
            support_cost_percent=10.0,  # 10% of base costs
        )

        result = calculator.calculate(inputs)

        # Support should be 10% of compute + storage
        base_cost = result.compute_cost + result.storage_cost
        expected_support = base_cost * 0.10
        assert abs(result.support_cost - expected_support) < 1.0

    def test_additional_discount(self, calculator, base_compute):
        """Test additional negotiated discount."""
        inputs_no_discount = TCOInputs(
            base_hourly_rate=0.10,
            compute=base_compute,
            pricing_model=PricingModel.ON_DEMAND,
            years=1,
            discount_percent=0.0,
        )

        inputs_with_discount = TCOInputs(
            base_hourly_rate=0.10,
            compute=base_compute,
            pricing_model=PricingModel.ON_DEMAND,
            years=1,
            discount_percent=15.0,  # 15% discount
        )

        result_no_discount = calculator.calculate(inputs_no_discount)
        result_with_discount = calculator.calculate(inputs_with_discount)

        # Should apply 15% discount
        expected_discount = result_no_discount.total_cost * 0.15
        assert abs(result_with_discount.discount_amount - expected_discount) < 1.0

        # Total with discount should be less
        assert result_with_discount.total_cost < result_no_discount.total_cost

    def test_compare_pricing_models(self, calculator, base_compute):
        """Test comparing multiple pricing models."""
        inputs = TCOInputs(
            base_hourly_rate=0.10,
            compute=base_compute,
            pricing_model=PricingModel.ON_DEMAND,
            years=3,
        )

        comparison = calculator.compare_pricing_models(inputs)

        # Should return results for all models
        assert len(comparison) == len(PricingModel)

        # On-demand should be most expensive
        on_demand_cost = comparison[PricingModel.ON_DEMAND].total_cost
        for model, result in comparison.items():
            if model != PricingModel.ON_DEMAND:
                assert result.total_cost <= on_demand_cost

    def test_roi_calculation(self, calculator):
        """Test ROI payback period calculation."""
        # Scenario: $100k/year on-prem, $60k/year cloud, $50k migration
        roi_years = calculator.calculate_roi_years(
            on_prem_cost=100000, cloud_cost=60000, migration_cost=50000
        )

        # $40k annual savings, $50k migration = 1.25 years payback
        assert roi_years == 1.25

    def test_roi_no_savings(self, calculator):
        """Test ROI when cloud is more expensive."""
        # Scenario: Cloud more expensive than on-prem
        roi_years = calculator.calculate_roi_years(
            on_prem_cost=60000, cloud_cost=100000, migration_cost=50000
        )

        # No savings, never pays back
        assert roi_years is None

    def test_zero_quantity(self, calculator):
        """Test edge case with zero resources."""
        inputs = TCOInputs(
            base_hourly_rate=0.10,
            compute=ComputeResource(vcpu=4, memory_gb=16, storage_gb=100, quantity=0),
            pricing_model=PricingModel.ON_DEMAND,
            years=1,
        )

        result = calculator.calculate(inputs)

        # Should have minimal/zero compute costs
        assert result.compute_cost == 0.0
