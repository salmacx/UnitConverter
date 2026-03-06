from typing import Optional

from pydantic import BaseModel, Field


class ConvertRequest(BaseModel):
    input: str = Field(..., min_length=1, description="Natural language conversion request")


class ConvertResponse(BaseModel):
    value: float
    from_unit: str
    to_unit: str
    result: float
    tool: str
    error: Optional[str] = None


class ParsedConversion(BaseModel):
    value: float
    from_unit: str
    to_unit: str