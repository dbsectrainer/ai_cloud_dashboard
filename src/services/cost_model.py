"""TCO (Total Cost of Ownership) calculation service with testable business logic."""

from dataclasses import dataclass
from enum import Enum


class PricingModel(Enum):
    """Cloud pricing models."""

    ON_DEMAND = "on_demand"
    RESERVED_1Y = "reserved_1y"
    RESERVED_3Y = "reserved_3y"
    SPOT = "spot"
    SAVINGS_PLAN = "savings_plan"


@dataclass
class ComputeResource:
    """Compute resource specification."""

    vcpu: int
    memory_gb: float
    storage_gb: float
    quantity: int = 1


@dataclass
class TCOInputs:
    """Inputs for TCO calculation."""

    base_hourly_rate: float
    compute: ComputeResource
    pricing_model: PricingModel = PricingModel.ON_DEMAND
    years: int = 3
    data_transfer_tb_month: float = 0.0
    storage_cost_gb_month: float = 0.0
    support_cost_percent: float = 0.0
    discount_percent: float = 0.0


@dataclass
class TCOResult:
    """TCO calculation results."""

    total_cost: float
    monthly_cost: float
    yearly_cost: float
    compute_cost: float
    storage_cost: float
    data_transfer_cost: float
    support_cost: float
    discount_amount: float
    effective_hourly_rate: float


class TCOCalculator:
    """
    Calculate Total Cost of Ownership for cloud resources.

    Isolated business logic with no external dependencies for easy testing.
    """

    # Pricing model discounts (percentage off on-demand)
    PRICING_DISCOUNTS = {
        PricingModel.ON_DEMAND: 0.0,
        PricingModel.RESERVED_1Y: 30.0,
        PricingModel.RESERVED_3Y: 50.0,
        PricingModel.SPOT: 70.0,  # Average spot discount
        PricingModel.SAVINGS_PLAN: 40.0,
    }

    # Industry average costs
    DATA_TRANSFER_COST_PER_GB = 0.09  # $0.09 per GB
    DEFAULT_STORAGE_COST_GB_MONTH = 0.023  # $0.023 per GB/month

    def calculate(self, inputs: TCOInputs) -> TCOResult:
        """
        Calculate TCO based on inputs.

        Args:
            inputs: TCO calculation inputs

        Returns:
            Detailed TCO breakdown
        """
        # Apply pricing model discount
        pricing_discount = self.PRICING_DISCOUNTS[inputs.pricing_model]
        effective_hourly_rate = inputs.base_hourly_rate * (1 - pricing_discount / 100)

        # Compute costs
        hours_per_month = 730  # Average hours per month
        months = inputs.years * 12

        compute_cost_monthly = effective_hourly_rate * hours_per_month * inputs.compute.quantity
        compute_cost_total = compute_cost_monthly * months

        # Storage costs
        storage_cost_monthly = (
            inputs.compute.storage_gb * inputs.compute.quantity * inputs.storage_cost_gb_month
        )
        if storage_cost_monthly == 0:
            storage_cost_monthly = (
                inputs.compute.storage_gb
                * inputs.compute.quantity
                * self.DEFAULT_STORAGE_COST_GB_MONTH
            )
        storage_cost_total = storage_cost_monthly * months

        # Data transfer costs
        data_transfer_cost_monthly = (
            inputs.data_transfer_tb_month * 1024 * self.DATA_TRANSFER_COST_PER_GB
        )
        data_transfer_cost_total = data_transfer_cost_monthly * months

        # Support costs (percentage of compute + storage)
        base_monthly = compute_cost_monthly + storage_cost_monthly
        support_cost_monthly = base_monthly * (inputs.support_cost_percent / 100)
        support_cost_total = support_cost_monthly * months

        # Calculate total before discount
        total_before_discount = (
            compute_cost_total + storage_cost_total + data_transfer_cost_total + support_cost_total
        )

        # Apply additional discount
        discount_amount = total_before_discount * (inputs.discount_percent / 100)
        total_cost = total_before_discount - discount_amount

        # Monthly and yearly averages
        monthly_cost = total_cost / months
        yearly_cost = total_cost / inputs.years

        return TCOResult(
            total_cost=round(total_cost, 2),
            monthly_cost=round(monthly_cost, 2),
            yearly_cost=round(yearly_cost, 2),
            compute_cost=round(compute_cost_total, 2),
            storage_cost=round(storage_cost_total, 2),
            data_transfer_cost=round(data_transfer_cost_total, 2),
            support_cost=round(support_cost_total, 2),
            discount_amount=round(discount_amount, 2),
            effective_hourly_rate=round(effective_hourly_rate, 4),
        )

    def compare_pricing_models(self, base_inputs: TCOInputs) -> dict[PricingModel, TCOResult]:
        """
        Compare TCO across different pricing models.

        Args:
            base_inputs: Base inputs (pricing_model will be overridden)

        Returns:
            Dictionary mapping pricing model to TCO result
        """
        results = {}
        for model in PricingModel:
            inputs = TCOInputs(
                base_hourly_rate=base_inputs.base_hourly_rate,
                compute=base_inputs.compute,
                pricing_model=model,
                years=base_inputs.years,
                data_transfer_tb_month=base_inputs.data_transfer_tb_month,
                storage_cost_gb_month=base_inputs.storage_cost_gb_month,
                support_cost_percent=base_inputs.support_cost_percent,
                discount_percent=base_inputs.discount_percent,
            )
            results[model] = self.calculate(inputs)
        return results

    def calculate_roi_years(
        self, on_prem_cost: float, cloud_cost: float, migration_cost: float
    ) -> float | None:
        """
        Calculate ROI payback period in years.

        Args:
            on_prem_cost: Annual on-premises cost
            cloud_cost: Annual cloud cost
            migration_cost: One-time migration cost

        Returns:
            Years to ROI, or None if never positive
        """
        annual_savings = on_prem_cost - cloud_cost

        if annual_savings <= 0:
            return None  # No savings, never pays back

        return round(migration_cost / annual_savings, 2)
