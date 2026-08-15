from typing import TypeVar
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

def to_response(
    response_model: type[T],
    data: object,
) -> T:
    return response_model.model_validate(data)
