from __future__ import annotations

from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import Field

from signhost.models import enums
from signhost.models import location


class Signers(BaseModel):
    FormSets: Optional[List[str]] = Field(
        None, description="List of formset keys to be assigned to this signer."
    )


class FormSets(BaseModel):
    Type: Optional[enums.FormSetType] = Field(
        None,
        description="Field type to create.\n"
        "\n"
        "* Seal is not yet implemented, this will specify the properties of a seal.\n"
        "* Signature, specifies a signature field\n"
        "* Check, specifies a checkbox. You'll have to set the `value` property\n"
        "* SingleLine, specifies a single line textbox\n",
    )
    Location: Optional[location.Location] = Field(
        None,
        description="Specify where the field should be placed within the document.",
    )
