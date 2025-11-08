"""Cache manager for ingested data with TTL and size limits."""

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Optional

import pandas as pd

logger = logging.getLogger(__name__)


class CacheManager:
    """Manages cached data with TTL and size constraints."""

    def __init__(self, cache_dir: Path, ttl_seconds: int = 3600, max_size_mb: int = 500):
        """
        Initialize cache manager.

        Args:
            cache_dir: Directory for cache storage
            ttl_seconds: Time-to-live for cache entries in seconds
            max_size_mb: Maximum cache size in megabytes
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl_seconds = ttl_seconds
        self.max_size_mb = max_size_mb
        self.metadata_file = self.cache_dir / "cache_metadata.json"
        self._load_metadata()

    def _load_metadata(self) -> None:
        """Load cache metadata."""
        if self.metadata_file.exists():
            with open(self.metadata_file, "r") as f:
                self.metadata = json.load(f)
        else:
            self.metadata = {}
            self._save_metadata()

    def _save_metadata(self) -> None:
        """Save cache metadata."""
        with open(self.metadata_file, "w") as f:
            json.dump(self.metadata, f, indent=2)

    def get(self, key: str) -> Optional[pd.DataFrame]:
        """
        Retrieve cached data if valid.

        Args:
            key: Cache key

        Returns:
            Cached DataFrame or None if expired/missing
        """
        cache_file = self.cache_dir / f"{key}.parquet"

        if not cache_file.exists():
            logger.debug(f"Cache miss: {key}")
            return None

        # Check TTL
        entry_meta = self.metadata.get(key, {})
        cached_at = datetime.fromisoformat(entry_meta.get("cached_at", "1970-01-01"))
        ttl_expires = cached_at + timedelta(seconds=self.ttl_seconds)

        if datetime.now() > ttl_expires:
            logger.info(f"Cache expired: {key} (cached at {cached_at})")
            self.delete(key)
            return None

        try:
            df = pd.read_parquet(cache_file)
            logger.info(f"Cache hit: {key} ({len(df)} records)")
            return df
        except Exception as e:
            logger.error(f"Error reading cache {key}: {e}")
            self.delete(key)
            return None

    def set(self, key: str, data: pd.DataFrame, metadata: Optional[dict] = None) -> bool:
        """
        Store data in cache.

        Args:
            key: Cache key
            data: DataFrame to cache
            metadata: Optional metadata

        Returns:
            True if cached successfully
        """
        cache_file = self.cache_dir / f"{key}.parquet"

        try:
            # Write to parquet
            data.to_parquet(cache_file, compression="snappy", index=False)

            # Update metadata
            self.metadata[key] = {
                "cached_at": datetime.now().isoformat(),
                "size_bytes": cache_file.stat().st_size,
                "record_count": len(data),
                "metadata": metadata or {},
            }
            self._save_metadata()

            logger.info(
                f"Cached: {key} ({len(data)} records, "
                f"{cache_file.stat().st_size / 1024:.1f} KB)"
            )

            # Check and enforce size limit
            self._enforce_size_limit()

            return True
        except Exception as e:
            logger.error(f"Error caching {key}: {e}")
            return False

    def delete(self, key: str) -> None:
        """Delete cache entry."""
        cache_file = self.cache_dir / f"{key}.parquet"
        if cache_file.exists():
            cache_file.unlink()

        if key in self.metadata:
            del self.metadata[key]
            self._save_metadata()

        logger.debug(f"Deleted cache: {key}")

    def clear(self) -> None:
        """Clear all cache entries."""
        for cache_file in self.cache_dir.glob("*.parquet"):
            cache_file.unlink()
        self.metadata = {}
        self._save_metadata()
        logger.info("Cache cleared")

    def _enforce_size_limit(self) -> None:
        """Enforce maximum cache size by removing oldest entries."""
        total_size_bytes = sum(
            entry.get("size_bytes", 0) for entry in self.metadata.values()
        )
        max_size_bytes = self.max_size_mb * 1024 * 1024

        if total_size_bytes <= max_size_bytes:
            return

        # Sort by cached_at (oldest first)
        sorted_entries = sorted(
            self.metadata.items(),
            key=lambda x: x[1].get("cached_at", ""),
        )

        # Remove oldest until under limit
        for key, meta in sorted_entries:
            if total_size_bytes <= max_size_bytes:
                break
            self.delete(key)
            total_size_bytes -= meta.get("size_bytes", 0)
            logger.info(f"Removed old cache entry: {key}")

    def get_stats(self) -> dict[str, Any]:
        """Get cache statistics."""
        total_size = sum(entry.get("size_bytes", 0) for entry in self.metadata.values())
        total_records = sum(
            entry.get("record_count", 0) for entry in self.metadata.values()
        )

        return {
            "entry_count": len(self.metadata),
            "total_size_mb": total_size / (1024 * 1024),
            "total_records": total_records,
            "max_size_mb": self.max_size_mb,
            "ttl_seconds": self.ttl_seconds,
            "entries": self.metadata,
        }

    def get_freshness(self, key: str) -> Optional[datetime]:
        """Get the last cached time for a key."""
        entry = self.metadata.get(key)
        if not entry:
            return None
        return datetime.fromisoformat(entry["cached_at"])
