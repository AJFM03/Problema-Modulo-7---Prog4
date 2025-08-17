import os
from dotenv import load_dotenv
import redis

# Cargar variables de entorno
load_dotenv()

def get_redis_connection():
    return redis.Redis(
        host=os.getenv("KEYDB_HOST", "localhost"),
        port=int(os.getenv("KEYDB_PORT", 6379)),
        password=os.getenv("KEYDB_PASSWORD", None),
        decode_responses=True
    )
