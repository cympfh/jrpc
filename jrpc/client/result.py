from dataclasses import dataclass
from typing import Any, Union


@dataclass
class Success:
    result: Any
    id: str


@dataclass
class Failed:
    code: int
    message: str


Result = Union[Success, Failed]


def from_json(o: dict) -> Result:

    if o.get("result", None):
        result = o.get("result")
        request_id = o.get("id")
        return Success(result, request_id)
