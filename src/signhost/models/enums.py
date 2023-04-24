from __future__ import annotations

from enum import Enum


class Betrouwbaarheidsniveau1(Enum):
    Basis = "Basis"
    Midden = "Midden"
    Substantieel = "Substantieel"
    Hoog = "Hoog"


class Code(Enum):
    integer_101 = 101
    integer_102 = 102
    integer_103 = 103
    integer_104 = 104
    integer_105 = 105
    integer_201 = 201
    integer_202 = 202
    integer_203 = 203
    integer_301 = 301
    integer_302 = 302
    integer_303 = 303
    integer_401 = 401
    integer_402 = 402
    integer_403 = 403


class Language(Enum):
    DE = "de-DE"
    US = "en-US"
    ES = "es-ES"
    FR = "fr-FR"
    IT = "it-IT"
    PL = "pl-PL"
    NL = "nl-NL"


class Rel(Enum):
    file = "file"
    receipt = "receipt"
    signer_sign = "signer.sign"
    signer_download = "signer.download"


class Status(Enum):
    WAITING_FOR_DOCUMENT = 5
    WAITING_FOR_SIGNER = 10
    IN_PROGRESS = 20
    SIGNED = 30
    REJECTED = 40
    EXPIRED = 50
    CANCELLED = 60
    FAILED = 70


class Type(Enum):
    DigiD = "DigiD"
    PhoneNumber = "PhoneNumber"


class FormSetType(Enum):
    Seal = "Seal"
    Signature = "Signature"
    Check = "Check"
    SingleLine = "SingleLine"


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
