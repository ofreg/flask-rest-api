import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
import time
from fastapi import Request, HTTPException
from unittest.mock import AsyncMock, patch
from api.rate_limiter import rate_limit

class DummyRequest:
    def __init__(self, host):
        self.client = type("Client", (), {"host": host})()

@pytest.mark.asyncio
@patch("api.rate_limiter.r")
async def test_rate_limit_authenticated_under_limit(mock_redis):
    
    mock_redis.zremrangebyscore = AsyncMock()
    mock_redis.zcard = AsyncMock(return_value=5)  
    mock_redis.zadd = AsyncMock()
    mock_redis.expire = AsyncMock()

    request = DummyRequest("127.0.0.1")
    
    await rate_limit(request, "user123")

@patch("api.rate_limiter.r")
@pytest.mark.asyncio
async def test_rate_limit_authenticated_over_limit(mock_redis):
    mock_redis.zremrangebyscore = AsyncMock()
    mock_redis.zcard = AsyncMock(return_value=10)  
    mock_redis.zadd = AsyncMock()
    mock_redis.expire = AsyncMock()

    request = DummyRequest("127.0.0.1")
    with pytest.raises(HTTPException) as exc:
        await rate_limit(request, "user123")
    assert exc.value.status_code == 429

@patch("api.rate_limiter.r")
@pytest.mark.asyncio
async def test_rate_limit_anonymous_under_limit(mock_redis):
    mock_redis.zremrangebyscore = AsyncMock()
    mock_redis.zcard = AsyncMock(return_value=1)  
    mock_redis.zadd = AsyncMock()
    mock_redis.expire = AsyncMock()

    request = DummyRequest("127.0.0.1")
    await rate_limit(request, None)

@patch("api.rate_limiter.r")
@pytest.mark.asyncio
async def test_rate_limit_anonymous_over_limit(mock_redis):
    mock_redis.zremrangebyscore = AsyncMock()
    mock_redis.zcard = AsyncMock(return_value=2)  
    mock_redis.zadd = AsyncMock()
    mock_redis.expire = AsyncMock()

    request = DummyRequest("127.0.0.1")
    with pytest.raises(HTTPException) as exc:
        await rate_limit(request, None)
    assert exc.value.status_code == 429
