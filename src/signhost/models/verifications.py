# flake8: noqa
from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Annotated
from typing import Literal
from typing import Union

from pydantic import BaseModel
from pydantic import Field


class VerificationType(Enum):
    Consent = "Consent"
    DigiD = "DigiD"
    eHerkenning = "eHerkenning"
    eIDAS_Login = "eIDAS Login"
    iDeal = "iDeal"
    iDIN = "iDIN"
    itsme_Identification = "itsme Identification"
    PhoneNumber = "PhoneNumber"
    Scribble = "Scribble"
    itsme_sign = "itsme sign"
    SigningCertificate = "SigningCertificate"
    SURFnet = "SURFnet"
    ZealiD_Qualified = "ZealiD Qualified"
    IPAddress = "IPAddress"


class Betrouwbaarheidsniveau(Enum):
    Basis = "Basis"
    Midden = "Midden"
    Substantieel = "Substantieel"
    Hoog = "Hoog"


class Verification(BaseModel):
    pass


class Consent(Verification):
    Type: Literal[VerificationType.Consent] = VerificationType.Consent


class DigiD(Verification):
    Type: Literal[VerificationType.DigiD] = VerificationType.DigiD
    Bsn: str | None = Field(
        None,
        description="When provided, the provided value must match the BSN of the credentials returned by DigiD.\nThe BSN is required to match an '11-proef'.\n",
        # noqa
    )
    Betrouwbaarheidsniveau: Betrouwbaarheidsniveau | None = Field(
        None,
        description="The level of confidence with which the identity of the signer has been determined.\nFor further information, please refer to [Logius](https://www.logius.nl/diensten/digid/hoe-werkt-het).\n",
        # noqa
    )


class EHerkenning(Verification):
    Type: Literal[VerificationType.eHerkenning] = VerificationType.eHerkenning
    Uid: str | None = None
    EntityConcernIdKvkNr: str | None = Field(
        None,
        description="When provided, the provided value must match the KvK number returned by eHerkenning.\n",
    )


class IDeal(Verification):
    Type: Literal[VerificationType.iDeal] = VerificationType.iDeal
    Iban: str | None = Field(
        None,
        description="The IBAN of the signer.\nWhen provided during the creation of the transaction this IBAN is\nverified during the verification flow to make sure these and the actual IBAN number match.\n",
        # noqa
        example="NL13TEST0123456789",
    )
    AccountHolderName: str | None = None
    AccountHolderCity: str | None = None


class IDIN(Verification):
    Type: Literal[VerificationType.iDIN] = VerificationType.iDIN
    AccountHolderName: str | None = Field(
        None,
        description="Name of the idin consumer / signer.\nCurrently we don't support supplying a value in this property to ensure the expected account holder name matches.\nThis could change in the future.\n",
    )
    AccountHolderAddress1: str | None = None
    AccountHolderAddress2: str | None = None
    AccountHolderDateOfBirth: date | None = Field(
        None,
        description="Date of birth of idin consumer / signer",
        example="2001-12-31",
    )
    Attributes: list[str] | None = Field(
        None,
        description="Contains all available iDIN attributes.\nThese attributes may change, therefore we cannot guarantee the availability of any of these attributes.\n",
        # noqa
    )


class IPAddress(Verification):
    Type: Literal[VerificationType.IPAddress] = VerificationType.IPAddress
    IPAddress: str | None = None


class PhoneNumber(Verification):
    Type: Literal[VerificationType.PhoneNumber] = VerificationType.PhoneNumber
    Number: str | None = Field(
        None,
        description="The mobile phone number of the signer.\n"
        "Must conform to E.164,\n"
        "[the international public telecommunication numbering plan](https://en.wikipedia.org/wiki/E.164),\n"
        "which requires the country calling code (e.g. +31).\n",
        example="+31123456789",
    )


class Scribble(Verification):
    Type: Literal[VerificationType.Scribble] = VerificationType.Scribble
    RequireHandsignature: bool | None = Field(
        False,
        description="When set the signer is required to draw a hand signature,\n"
        "either via computer mouse, trackpad, or touchscreen.\n",
    )
    ScribbleNameFixed: bool | None = Field(
        False,
        description="When set the signer will not be able to change its scribble name.\n"
        "When not set the signer can correct or provide a scribble name.\n",
    )
    ScribbleName: str | None = Field(
        None,
        description="The name of the signer, this will be pre filled in the scribble form.\n"
        "Required if `ScribbleNameFixed` is set.\n",
    )


class SigningCertificate(Verification):
    Type: Literal[
        VerificationType.SigningCertificate
    ] = VerificationType.SigningCertificate
    Issuer: str | None = None
    Subject: str | None = None
    Thumbprint: str | None = None


class SURFnet(Verification):
    Type: Literal[VerificationType.SURFnet] = VerificationType.SURFnet
    Uid: str | None = None
    Attributes: list[str] | None = Field(
        None,
        description="Contains all available SURFnet attributes.\nThese attributes may change, therefore we cannot guarantee the availability of any of these attributes.\n",
        # noqa
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
