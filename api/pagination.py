from pydantic import BaseModel
from typing import TypeVar, Generic
from fastapi_pagination.bases import RawParams, AbstractParams
from fastapi_pagination.default import Page as BasePage, Params as BaseParams
from fastapi import Query

T = TypeVar("T")

class Params(BaseModel, AbstractParams):
    total_items: int = 10
    return_per_page: int = 10000

    def to_raw_params(self) -> RawParams:
        return RawParams(
            limit=self.total_items,
            offset=self.total_items * self.return_per_page,
        )


class ParamsCustom(BaseParams):
    size: int = Query(50, ge=1, le=10000, description="Page size")


class Page(BasePage[T], Generic[T]):
    __params_type__ = ParamsCustom
