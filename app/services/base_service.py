from typing import Generic, TypeVar
from app.repositories.base_repository import BaseRepository
from pydantic import BaseModel

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, repository: BaseRepository[ModelType, CreateSchemaType, UpdateSchemaType]):
        self.repository = repository

    async def get(self, **kwargs):
        return await self.repository.get(**kwargs)

    async def get_multi(self, *, skip: int = 0, limit: int = 100):
        return await self.repository.get_multi(skip=skip, limit=limit)

    async def create(self, obj_in: CreateSchemaType):
        return await self.repository.create(obj_in=obj_in)

    async def update(self, *, obj_id: int, obj_in: UpdateSchemaType | dict[str, any]):
        return await self.repository.update(obj_id=obj_id, obj_in=obj_in)

    async def delete(self, *, obj_id: int):
        return await self.repository.delete(obj_id=obj_id)