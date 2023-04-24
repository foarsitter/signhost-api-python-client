# flake8: noqa
from __future__ import annotations

from datetime import date
from typing import List
from typing import Literal
from typing import Optional
from typing import Union

from pydantic import BaseModel
from pydantic import Field
from typing_extensions import Annotated

from signhost.models import enums


class Verification(BaseModel):
    pass


class Consent(Verification):
    Type: Literal["Consent"] = "Consent"


class DigiD(Verification):
    Type: Literal["DigiD"] = "DigiD"
    Bsn: Optional[str] = Field(
        None,
        description="When provided, the provided value must match the BSN of the credentials returned by DigiD.\nThe BSN is required to match an '11-proef'.\n",
        # noqa
    )
    Betrouwbaarheidsniveau: Optional[enums.Betrouwbaarheidsniveau] = Field(
        None,
        description="The level of confidence with which the identity of the signer has been determined.\nFor further information, please refer to [Logius](https://www.logius.nl/diensten/digid/hoe-werkt-het).\n",
        # noqa
    )


class EHerkenning(Verification):
    Type: Literal["eHerkenning"] = "eHerkenning"
    Uid: Optional[str] = None
    EntityConcernIdKvkNr: Optional[str] = Field(
        None,
        description="When provided, the provided value must match the KvK number returned by eHerkenning.\n",
    )


class IDeal(Verification):
    Type: Literal["iDeal"] = "iDeal"
    Iban: Optional[str] = Field(
        None,
        description="The IBAN of the signer.\nWhen provided during the creation of the transaction this IBAN is\nverified during the verification flow to make sure these and the actual IBAN number match.\n",
        # noqa
        example="NL13TEST0123456789",
    )
    AccountHolderName: Optional[str] = None
    AccountHolderCity: Optional[str] = None


class IDIN(Verification):
    Type: Literal["iDIN"] = "iDIN"
    AccountHolderName: Optional[str] = Field(
        None,
        description="Name of the idin consumer / signer.\nCurrently we don't support supplying a value in this property to ensure the expected account holder name matches.\nThis could change in the future.\n",
    )
    AccountHolderAddress1: Optional[str] = None
    AccountHolderAddress2: Optional[str] = None
    AccountHolderDateOfBirth: Optional[date] = Field(
        None,
        description="Date of birth of idin consumer / signer",
        example="2001-12-31",
    )
    Attributes: Optional[List[str]] = Field(
        None,
        description="Contains all available iDIN attributes.\nThese attributes may change, therefore we cannot guarantee the availability of any of these attributes.\n",
        # noqa
    )


class IPAddress(Verification):
    Type: Literal["IPAddress"] = "IPAddress"
    IPAddress: Optional[str] = None


class PhoneNumber(Verification):
    Type: Literal["PhoneNumber"] = "PhoneNumber"
    Number: Optional[str] = Field(
        None,
        description="The mobile phone number of the signer.\n"
        "Must conform to E.164,\n"
        "[the international public telecommunication numbering plan](https://en.wikipedia.org/wiki/E.164),\n"
        "which requires the country calling code (e.g. +31).\n",
        example="+31123456789",
    )


class Scribble(Verification):
    Type: Literal["Scribble"] = "Scribble"
    RequireHandsignature: Optional[bool] = Field(
        False,
        description="When set the signer is required to draw a hand signature,\n"
        "either via computer mouse, trackpad, or touchscreen.\n",
    )
    ScribbleNameFixed: Optional[bool] = Field(
        False,
        description="When set the signer will not be able to change its scribble name.\n"
        "When not set the signer can correct or provide a scribble name.\n",
    )
    ScribbleName: Optional[str] = Field(
        None,
        description="The name of the signer, this will be pre filled in the scribble form.\n"
        "Required if `ScribbleNameFixed` is set.\n",
    )


class SigningCertificate(Verification):
    Type: Literal["SigningCertificate"] = "SigningCertificate"
    Issuer: Optional[str] = None
    Subject: Optional[str] = None
    Thumbprint: Optional[str] = None


class SURFnet(Verification):
    Type: Literal["SURFnet"] = "SURFnet"
    Uid: Optional[str] = None
    Attributes: Optional[List[str]] = Field(
        None,
        description="Contains all available SURFnet attributes.\n"
        "These attributes may change, therefore we cannot guarantee "
        "the availability of any of these attributes.\n",
    )


VerificationAnnotatedType = Annotated[
    Union[
        Consent,
        DigiD,
        EHerkenning,
        IDeal,
        IDIN,
        IPAddress,
        PhoneNumber,
        Scribble,
        SigningCertificate,
        SURFnet,
    ],
    Field(discriminator="Type"),
]
