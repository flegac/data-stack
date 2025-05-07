from redis.asyncio import Redis

from message_queue_redis.redis_config import RedisConfig


class RedisConnection:
    def __init__(self, config: RedisConfig):
        self.config = config
        self._connection: Redis | None = None

    async def ensure_connection(self) -> Redis:
        if self._connection is None:
            self._connection = Redis(
                host=self.config.host,
                port=self.config.port,
                db=self.config.db,
                decode_responses=True,
            )
        return self._connection

    async def close(self):
        if self._connection:
            await self._connection.close()
            self._connection = None
