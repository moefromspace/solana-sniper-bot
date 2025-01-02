import redis.asyncio as redis
import logging
import json
from typing import Callable, Optional

logger = logging.getLogger(__name__)

redis_client = None

async def connect_redis(redis_url: str = "redis://localhost:6379"):
    """Establish a connection to Redis."""
    global redis_client
    redis_client = redis.from_url(redis_url, decode_responses=True)
    logger.info("Connected to Redis")


async def disconnect_redis():
    """Close the Redis connection."""
    global redis_client
    if redis_client:
        await redis_client.close()
        logger.info("Disconnected from Redis")


async def publish_to_redis(channel: str, message: dict):
    """
    Publish a message to a Redis channel.
    """
    if not redis_client:
        raise RuntimeError("Redis connection not initialized. Call connect_redis() first.")
    serialized_message = json.dumps(message)
    await redis_client.publish(channel, serialized_message)
    logger.debug(f"Published message to channel '{channel}': {serialized_message}")


async def subscribe_to_redis(channel: str, callback: Callable[[str], None]):
    """
    Subscribe to a Redis channel and process messages with the provided callback.
    """
    if not redis_client:
        raise RuntimeError("Redis connection not initialized. Call connect_redis() first.")
    pubsub = redis_client.pubsub()
    await pubsub.subscribe(channel)
    logger.info(f"Subscribed to channel: {channel}")

    async for message in pubsub.listen():
        if message["type"] == "message":
            logger.debug(f"Message received on channel '{channel}': {message['data']}")
            await callback(message["data"])
