from contextlib import asynccontextmanager
from contextvars import ContextVar
from typing import Optional
from uuid import uuid1

from fastapi import FastAPI
from sqlalchemy.orm import scoped_session, sessionmaker
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

from app.api.v1.endpoint import api
from app.config.db.database import engine


def include_router(app: FastAPI):
    app.include_router(api)


def set_cors(app):
    originls_ = [
        "localhost:8000",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=originls_,
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=["*"],
    )


def start_application() -> FastAPI:
    app = FastAPI()

    include_router(app)
    set_cors(app)
    return app


app = start_application()

_request_id_var: ContextVar[Optional[str]] = ContextVar("request_id", default=None)


def get_requestion_id():
    return _request_id_var.get()


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request_id = str(uuid1())
    request_token = _request_id_var.set(request_id)

    try:
        session = scoped_session(
            sessionmaker(bind=engine, autoflush=True, autocommit=False),
            scopefunc=get_requestion_id,
        )
        request.state.db = session()

        response = await call_next(request)
    except Exception as e:
        raise e

    finally:
        request.state.db.close()
    _request_id_var.reset(request_token)
    return response
