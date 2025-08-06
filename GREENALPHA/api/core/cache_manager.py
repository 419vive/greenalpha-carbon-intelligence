"""
Cache Manager for handling Redis connections and operations.

This module provides a centralized cache management system using Redis,
including connection pooling, graceful error handling, and basic cache
operations (get, set, delete).
"""
import redis
import os
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CacheManager:
    """
    Manages Redis cache connections and operations.
    
    Handles connection pooling and gracefully disables caching if Redis is
    unavailable.
    """
    _pool = None

    def __init__(self):
        """
        Initializes the Redis connection pool.
        
        Reads configuration from environment variables:
        - REDIS_HOST: The hostname of the Redis server (default: 'localhost')
        - REDIS_PORT: The port of the Redis server (default: 6379)
        - REDIS_DB: The database number to use (default: 0)
        """
        if CacheManager._pool is None:
            try:
                redis_host = os.environ.get('REDIS_HOST', 'localhost')
                redis_port = int(os.environ.get('REDIS_PORT', 6379))
                redis_db = int(os.environ.get('REDIS_DB', 0))
                
                CacheManager._pool = redis.ConnectionPool(
                    host=redis_host,
                    port=redis_port,
                    db=redis_db,
                    decode_responses=True # Decode responses to strings
                )
                self.redis_instance = redis.Redis(connection_pool=self._pool)
                # Test the connection
                self.redis_instance.ping()
                logger.info("✅ Successfully connected to Redis cache.")
            except redis.exceptions.ConnectionError as e:
                logger.warning(f"⚠️ Could not connect to Redis: {e}. Caching will be disabled.")
                CacheManager._pool = None
                self.redis_instance = None

    def is_available(self):
        """Check if the cache is available."""
        return self.redis_instance is not None

    def get(self, key):
        """
        Retrieves a value from the cache for a given key.
        
        Args:
            key (str): The key to retrieve.
            
        Returns:
            The value from the cache, or None if the key is not found or cache is unavailable.
        """
        if not self.is_available():
            return None
            
        try:
            value = self.redis_instance.get(key)
            return json.loads(value) if value else None
        except Exception as e:
            logger.error(f"Error getting key '{key}' from cache: {e}")
            return None

    def set(self, key, value, ttl_seconds=3600):
        """
        Sets a value in the cache with a Time-To-Live (TTL).
        
        Args:
            key (str): The key for the cache entry.
            value: The value to store (must be JSON serializable).
            ttl_seconds (int): The time-to-live in seconds (default: 1 hour).
        """
        if not self.is_available():
            return
            
        try:
            serialized_value = json.dumps(value)
            self.redis_instance.setex(key, ttl_seconds, serialized_value)
            logger.info(f"Cached data for key: {key} with TTL: {ttl_seconds}s")
        except TypeError as e:
            logger.error(f"Failed to serialize value for key '{key}': {e}")
        except Exception as e:
            logger.error(f"Error setting key '{key}' in cache: {e}")

    def delete(self, key):
        """
        Deletes a key from the cache.
        
        Args:
            key (str): The key to delete.
        """
        if not self.is_available():
            return
            
        try:
            self.redis_instance.delete(key)
            logger.info(f"Deleted key '{key}' from cache.")
        except Exception as e:
            logger.error(f"Error deleting key '{key}' from cache: {e}")

    def get_connection(self):
        """Returns the raw Redis connection instance."""
        return self.redis_instance

# Global instance of the cache manager
cache_manager = CacheManager()
