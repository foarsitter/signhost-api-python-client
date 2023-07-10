from __future__ import annotations

from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class Location(BaseModel):
    Search: Optional[str] = Field(
        None,
        description="The text to search in the pdf document to use as "
        "the position for the field. For example `{{Signer1}}`.",
    )
    Occurence: Optional[int] = Field(
        None, description="When using text search, only match this matched occurence."
    )
    Top: Optional[int] = Field(
        None, description="Offset from the top of the search text or the page"
    )
    Right: Optional[int] = Field(
        None, description="Offset from the right of the search or the page"
    )
    Bottom: Optional[int] = Field(
        None, description="Offset from the bottom of the search or the page"
    )
    Left: Optional[int] = Field(
        None, description="Offset from the left of the search or the page"
    )
    Width: Optional[int] = Field(
        None,
        description="The width of the field, can’t be used when both Left and Right are specified.\n"
        "For signature and seal fields we suggest a width of 140.\n",
    )
    Height: Optional[int] = Field(
        None,
        description="The height of the field, can’t be used when both Bottom and Top are specified.\n"
        "For signature and seal fields we suggest a height of 70.\n",
    )
    PageNumber: Optional[int] = Field(
        None, description="On which page the field should be placed."
    )
