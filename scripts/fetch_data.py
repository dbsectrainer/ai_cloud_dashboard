#!/usr/bin/env python3
"""
Cron-able script to fetch cloud pricing data and cache to Parquet.

Usage:
    python scripts/fetch_data.py [--force]

Crontab example (daily at 2 AM):
    0 2 * * * cd /app && python scripts/fetch_data.py >> /var/log/cloud-dashboard-fetch.log 2>&1
"""

import argparse
import asyncio
import logging
import sys
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import settings
from src.ingestion.cache import CacheManager
from src.ingestion.fetcher import CloudDataFetcher

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


async def fetch_and_cache_data(force: bool = False) -> bool:
    """
    Fetch cloud pricing data and cache to Parquet.

    Args:
        force: Force fetch even if cache is valid

    Returns:
        True if successful
    """
    cache_manager = CacheManager(
        cache_dir=settings.CACHE_DIR,
        ttl_seconds=settings.CACHE_TTL_SECONDS,
        max_size_mb=settings.CACHE_MAX_SIZE_MB,
    )

    cache_key = "cloud_pricing_latest"

    # Check if cache is still valid
    if not force:
        cached_data = cache_manager.get(cache_key)
        if cached_data is not None:
            freshness = cache_manager.get_freshness(cache_key)
            logger.info(
                f"Using cached data from {freshness} "
                f"({len(cached_data)} records). Use --force to refresh."
            )
            return True

    # Fetch fresh data
    logger.info("Fetching fresh cloud pricing data...")
    start_time = datetime.now()

    try:
        async with CloudDataFetcher() as fetcher:
            pricing_data = await fetcher.fetch_all_pricing()

        if pricing_data.empty:
            logger.error("No pricing data fetched. Aborting.")
            return False

        # Cache the data
        success = cache_manager.set(
            cache_key,
            pricing_data,
            metadata={
                "source": "public_apis",
                "providers": pricing_data["provider"].unique().tolist(),
                "record_count": len(pricing_data),
            },
        )

        if not success:
            logger.error("Failed to cache pricing data")
            return False

        elapsed = (datetime.now() - start_time).total_seconds()
        logger.info(
            f"Successfully fetched and cached {len(pricing_data)} pricing records "
            f"from {pricing_data['provider'].nunique()} providers in {elapsed:.2f}s"
        )

        # Log cache stats
        stats = cache_manager.get_stats()
        logger.info(
            f"Cache stats: {stats['entry_count']} entries, "
            f"{stats['total_size_mb']:.2f} MB / {stats['max_size_mb']} MB"
        )

        # Write freshness badge data
        write_freshness_badge(pricing_data)

        return True

    except Exception as e:
        logger.error(f"Error during data fetch: {e}", exc_info=True)
        return False


def write_freshness_badge(data) -> None:
    """Write data freshness info for README badge."""
    freshness_file = Path("data/.freshness")
    freshness_file.parent.mkdir(parents=True, exist_ok=True)

    with open(freshness_file, "w") as f:
        f.write(
            f"{datetime.now().isoformat()}\n"
            f"records={len(data)}\n"
            f"providers={data['provider'].nunique()}\n"
        )

    logger.info(f"Updated freshness badge data: {freshness_file}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Fetch and cache cloud pricing data"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force fetch even if cache is valid",
    )
    args = parser.parse_args()

    logger.info("=" * 60)
    logger.info("Cloud Dashboard - Data Ingestion")
    logger.info(f"Started at: {datetime.now()}")
    logger.info(f"Cache dir: {settings.CACHE_DIR}")
    logger.info(f"Cache TTL: {settings.CACHE_TTL_SECONDS}s")
    logger.info(f"Force fetch: {args.force}")
    logger.info("=" * 60)

    success = asyncio.run(fetch_and_cache_data(force=args.force))

    if success:
        logger.info("Data fetch completed successfully")
        sys.exit(0)
    else:
        logger.error("Data fetch failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
