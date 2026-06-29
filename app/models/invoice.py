from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import List

class LineItem(BaseModel):
    description: str
    price: float

class Invoice(BaseModel):
    line_items: List[LineItem]
    vendor: str
    date: str
    amount: float

    @field_validator("date")
    @classmethod
    def validate_date(cls, v: str) -> str:
        formats = ["%Y-%m-%d", "%d/%m/%Y", "%B %d %Y"]
        for fmt in formats:
            try:
                datetime.strptime(v, fmt)
                return v
            except ValueError:
                continue
        raise ValueError(f"Unrecognized date format: {v}")