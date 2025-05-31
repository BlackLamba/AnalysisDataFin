from fastapi import APIRouter

class BaseRouter:
    def __init__(self, prefix: str, tags: list[str]):
        self.router = APIRouter(prefix=prefix, tags=tags)