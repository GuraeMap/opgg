import os


class Config:
    DB_HOST = os.environ.get("DB_HOST", "mysql")
    DB_DATABASE = os.environ.get("DB_DATABASE", "test")
    DB_USER = os.environ.get("DB_USER", "admin")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "1234")
    REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
    REDIS_PORT = os.environ.get("REDIS_PORT", 6379)

    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "1f823daf-ffbe-11ee-abbi")

    @property
    def DB_URL(self):
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:3306/{self.DB_DATABASE}?charset=utf8mb4"


defalut = Config()
