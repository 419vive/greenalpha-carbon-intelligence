"""
Tests for the Cache Manager.

This test suite validates the functionality of the CacheManager, ensuring that
it correctly handles connections, data serialization, TTL, and graceful
failure.
"""
import unittest
import sys
import os
import time
from unittest.mock import patch, MagicMock

# Add project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# We need to import the module to be tested
from api.core import cache_manager

# Force a reload of the module to apply patches
import importlib
importlib.reload(cache_manager)

class TestCacheManager(unittest.TestCase):
    """
    Tests the core functionality of the CacheManager.
    """

    def setUp(self):
        """Set up a fresh CacheManager instance for each test."""
        # This setup will run for each test, ensuring isolation.
        # We will use patching to mock Redis behavior.
        pass

    @patch('redis.Redis')
    def test_basic_set_get_delete(self, mock_redis_class):
        """Test basic set, get, and delete operations."""
        mock_redis_instance = MagicMock()
        with patch.object(cache_manager, 'cache_manager') as mock_cache_manager:
            mock_cache_manager.redis_instance = mock_redis_instance
            mock_cache_manager.is_available.return_value = True

            # Test SET
            test_data = {'status': 'ok', 'value': 42}
            mock_cache_manager.set('test_key', test_data)
            # Verify it was called with serialized data
            mock_redis_instance.setex.assert_called_with('test_key', 3600, '{"status": "ok", "value": 42}')

            # Test GET
            mock_redis_instance.get.return_value = '{"status": "ok", "value": 42}'
            retrieved_data = mock_cache_manager.get('test_key')
            self.assertEqual(retrieved_data, test_data)

            # Test DELETE
            mock_cache_manager.delete('test_key')
            mock_redis_instance.delete.assert_called_with('test_key')

    @patch('redis.Redis')
    def test_cache_expiration_ttl(self, mock_redis_class):
        """Test that the TTL is correctly passed to Redis."""
        mock_redis_instance = MagicMock()
        with patch.object(cache_manager, 'cache_manager') as mock_cache_manager:
            mock_cache_manager.redis_instance = mock_redis_instance
            mock_cache_manager.is_available.return_value = True

            test_data = {'message': 'ephemeral'}
            custom_ttl = 60  # 1 minute
            mock_cache_manager.set('ttl_test', test_data, ttl_seconds=custom_ttl)
            mock_redis_instance.setex.assert_called_with('ttl_test', custom_ttl, '{"message": "ephemeral"}')

    @patch('redis.Redis', side_effect=redis.exceptions.ConnectionError)
    def test_fallback_when_cache_unavailable(self, mock_redis_class):
        """Test that the system falls back gracefully when Redis is down."""
        # Re-instantiate the manager to trigger the connection error
        local_cache_manager = cache_manager.CacheManager()
        
        self.assertFalse(local_cache_manager.is_available())
        self.assertIsNone(local_cache_manager.redis_instance)

        # Operations should do nothing and not raise errors
        retrieved = local_cache_manager.get('any_key')
        self.assertIsNone(retrieved)
        
        # set and delete should be no-ops
        local_cache_manager.set('any_key', {'data': 'value'})
        local_cache_manager.delete('any_key')

    @patch('redis.Redis')
    def test_get_non_existent_key(self, mock_redis_class):
        """Test that getting a non-existent key returns None."""
        mock_redis_instance = MagicMock()
        mock_redis_instance.get.return_value = None
        
        with patch.object(cache_manager, 'cache_manager') as mock_cache_manager:
            mock_cache_manager.redis_instance = mock_redis_instance
            mock_cache_manager.is_available.return_value = True
            
            result = mock_cache_manager.get('non_existent_key')
            self.assertIsNone(result)

    # Note: Testing concurrent access patterns typically requires more complex setups
    # with threading or multiprocessing, which is beyond the scope of this basic
    # test suite. The connection pooling in Redis is designed to handle this.

if __name__ == '__main__':
    unittest.main()
