from app.config.config import defalut
from redis import Redis


redis_session = Redis(host=defalut.REDIS_HOST, port=defalut.REDIS_PORT)
