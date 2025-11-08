"""Tests for ingestion cache manager."""

import tempfile
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import pytest

from src.ingestion.cache import CacheManager


class TestCacheManager:
    """Test cases for cache manager."""

    @pytest.fixture
    def temp_cache_dir(self):
        """Create temporary cache directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.fixture
    def cache_manager(self, temp_cache_dir):
        """Create cache manager with temp directory."""
        return CacheManager(cache_dir=temp_cache_dir, ttl_seconds=3600, max_size_mb=10)

    @pytest.fixture
    def sample_data(self):
        """Create sample DataFrame."""
        return pd.DataFrame(
            {
                "provider": ["AWS", "Azure", "GCP"],
                "service": ["EC2", "VM", "Compute"],
                "price": [0.10, 0.12, 0.09],
            }
        )

    def test_cache_set_and_get(self, cache_manager, sample_data):
        """Test basic cache set and get operations."""
        key = "test_pricing"

        # Set cache
        success = cache_manager.set(key, sample_data)
        assert success

        # Get cache
        cached_data = cache_manager.get(key)
        assert cached_data is not None
        assert len(cached_data) == len(sample_data)
        pd.testing.assert_frame_equal(cached_data, sample_data)

    def test_cache_miss(self, cache_manager):
        """Test cache miss for non-existent key."""
        result = cache_manager.get("nonexistent_key")
        assert result is None

    def test_cache_metadata(self, cache_manager, sample_data):
        """Test cache metadata storage."""
        key = "test_with_metadata"
        metadata = {"source": "test", "provider": "AWS"}

        cache_manager.set(key, sample_data, metadata=metadata)

        stats = cache_manager.get_stats()
        assert key in stats["entries"]
        assert stats["entries"][key]["metadata"] == metadata
        assert stats["entries"][key]["record_count"] == len(sample_data)

    def test_cache_ttl_expiration(self, cache_manager, sample_data):
        """Test that cache expires after TTL."""
        # Create cache with very short TTL
        short_ttl_cache = CacheManager(
            cache_dir=cache_manager.cache_dir, ttl_seconds=1, max_size_mb=10
        )

        key = "expiring_key"
        short_ttl_cache.set(key, sample_data)

        # Immediately should work
        result = short_ttl_cache.get(key)
        assert result is not None

        # After TTL, should be expired
        import time

        time.sleep(2)
        result = short_ttl_cache.get(key)
        assert result is None

    def test_cache_delete(self, cache_manager, sample_data):
        """Test cache deletion."""
        key = "to_delete"

        cache_manager.set(key, sample_data)
        assert cache_manager.get(key) is not None

        cache_manager.delete(key)
        assert cache_manager.get(key) is None

    def test_cache_clear(self, cache_manager, sample_data):
        """Test clearing all cache."""
        cache_manager.set("key1", sample_data)
        cache_manager.set("key2", sample_data)

        stats = cache_manager.get_stats()
        assert stats["entry_count"] == 2

        cache_manager.clear()

        stats = cache_manager.get_stats()
        assert stats["entry_count"] == 0

    def test_cache_size_limit(self, temp_cache_dir, sample_data):
        """Test cache size enforcement."""
        # Create large DataFrame
        large_data = pd.DataFrame(
            {"col" + str(i): range(1000) for i in range(100)}
        )

        # Create cache with small size limit (1 MB)
        small_cache = CacheManager(
            cache_dir=temp_cache_dir, ttl_seconds=3600, max_size_mb=1
        )

        # Add multiple entries
        small_cache.set("entry1", large_data)
        small_cache.set("entry2", large_data)
        small_cache.set("entry3", large_data)

        # Should enforce size limit by removing oldest
        stats = small_cache.get_stats()
        assert stats["total_size_mb"] <= 1.0

    def test_cache_freshness(self, cache_manager, sample_data):
        """Test getting cache freshness timestamp."""
        key = "fresh_data"

        before = datetime.now()
        cache_manager.set(key, sample_data)
        after = datetime.now()

        freshness = cache_manager.get_freshness(key)
        assert freshness is not None
        assert before <= freshness <= after

    def test_cache_stats(self, cache_manager, sample_data):
        """Test cache statistics."""
        cache_manager.set("data1", sample_data)
        cache_manager.set("data2", sample_data)

        stats = cache_manager.get_stats()

        assert stats["entry_count"] == 2
        assert stats["total_records"] == len(sample_data) * 2
        assert stats["total_size_mb"] > 0
        assert stats["max_size_mb"] == 10
        assert stats["ttl_seconds"] == 3600
