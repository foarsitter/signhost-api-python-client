# flake8: noqa
# generated by datamodel-codegen:
#   filename:  signhost_openapi.yml
#   timestamp: 2023-02-09T16:34:43+00:00

from __future__ import annotations

from datetime import date
from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel
from pydantic import Field


class Language(Enum):
    de_DE = "de-DE"
    en_US = "en-US"
    es_ES = "es-ES"
    fr_FR = "fr-FR"
    it_IT = "it-IT"
    pl_PL = "pl-PL"
    nl_NL = "nl-NL"


class Language1(Enum):
    de_DE = "de-DE"
    en_US = "en-US"
    es_ES = "es-ES"
    fr_FR = "fr-FR"
    it_IT = "it-IT"
    pl_PL = "pl-PL"
    nl_NL = "nl-NL"


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


class Activity(BaseModel):
    Id: str | None = None
    Code: Code | None = Field(
        None,
        description="* 101 -\tInvitation sent\n* 102 -\tReceived\n* 103 -\tOpened\n* 104 -\tReminder sent\n* 105 -\tDocument opened, Info property contains the file id of the opened document.\n* 201 -\tCancelled\n* 202 -\tRejected\n* 203 -\tSigned\n* 301 -\tSigned document sent\n* 302 -\tSigned document opended\n* 303 -\tSigned document downloaded\n* 401 -\tReceipt sent\n* 402 -\tReceipt opened\n* 403 -\tReceipt downloaded\n",  # noqa
    )
    Info: str | None = Field(
        None,
        description="May contain additional information belonging to this activity",
    )
    CreatedDateTime: datetime | None = None


class Receiver(BaseModel):
    Name: str = Field(..., description="The name of the receiver.")
    Email: str = Field(..., description="The e-mail address of the reveiver.")
    Language: str | None = Field(
        "nl-NL",
        description="The language of the receiver, only de-DE, en-US, es-ES, fr-FR, it-IT and nl-NL are allowed.",
    )
    Subject: str | None = Field(
        None,
        description="The subject of the receiver email in plain text.\nMaximum of 64 characters allowed.\nOmitting this parameter will enable the default subject.\n",  # noqa
    )
    Message: str = Field(
        ...,
        description="The email message towards the receiver in plain text. Newlines can be created by including a \\n in the json, HTML is not allowed.",  # noqa
    )
    Reference: str | None = Field(None, description="The reference of the receiver.")
    Context: dict[str, Any] | None = Field(
        None,
        description="Any valid json object which we will return back to you when doing a GET on the transaction or when we send a postback.",  # noqa
    )


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


class Authentication(BaseModel):
    Type: Type = Field(
        ...,
        description="Type of the authentication object.\nThe `Type` property **must** be the first property in the json!\n\nThe order in which the authentications are provided determine in which order the signer will have to perform the specified method.\n",  # noqa
    )


class Type1(Enum):
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


class Verification(BaseModel):
    Type: Type1 = Field(
        ...,
        description="Type of the verification object.\nThe `Type` property **must** be the first property in the json!\n\nThe order in which the verifications are provided determine in which order the signer will have to perform the specified method.\nYou **must** use one of the following verifications as the last method:\n- Consent\n- itsme sign*\n- PhoneNumber\n- Scribble\n- SigningCertificate*\n- ZealiD Qualified*\n\n* These verifications can not be used in any other position than the last.\n",  # noqa
    )


class Consent(Verification):
    pass


class Betrouwbaarheidsniveau(Enum):
    Basis = "Basis"
    Midden = "Midden"
    Substantieel = "Substantieel"
    Hoog = "Hoog"


class DigiD(Verification):
    Bsn: str | None = Field(
        None,
        description="When provided, the provided value must match the BSN of the credentials returned by DigiD.\nThe BSN is required to match an '11-proef'.\n",  # noqa
    )
    Betrouwbaarheidsniveau: Betrouwbaarheidsniveau | None = Field(
        None,
        description="The level of confidence with which the identity of the signer has been determined.\nFor further information, please refer to [Logius](https://www.logius.nl/diensten/digid/hoe-werkt-het).\n",  # noqa
    )


class EHerkenning(Verification):
    Uid: str | None = None
    EntityConcernIdKvkNr: str | None = Field(
        None,
        description="When provided, the provided value must match the KvK number returned by eHerkenning.\n",
    )


class IDeal(Verification):
    Iban: str | None = Field(
        None,
        description="The IBAN of the signer.\nWhen provided during the creation of the transaction this IBAN is\nverified during the verification flow to make sure these and the actual IBAN number match.\n",  # noqa
        example="NL13TEST0123456789",
    )
    AccountHolderName: str | None = None
    AccountHolderCity: str | None = None


class IDIN(Verification):
    AccountHolderName: str | None = Field(
        None,
        description="Name of the idin consumer / signer.\nCurrently we don't support supplying a value in this property to ensure the expected account holder name matches.\nThis could change in the future.\n",  # noqa
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
        description="Contains all available iDIN attributes.\nThese attributes may change, therefore we cannot guarantee the availability of any of these attributes.\n",  # noqa
    )


class IPAddress(Verification):
    IPAddress: str | None = None


class PhoneNumber(Verification):
    Number: str | None = Field(
        None,
        description="The mobile phone number of the signer.\nMust conform to E.164,\n[the international public telecommunication numbering plan](https://en.wikipedia.org/wiki/E.164),\nwhich requires the country calling code (e.g. +31).\n",  # noqa
        example="+31123456789",
    )


class Scribble(Verification):
    RequireHandsignature: bool | None = Field(
        False,
        description="When set the signer is required to draw a hand signature,\neither via computer mouse, trackpad, or touchscreen.\n",  # noqa
    )
    ScribbleNameFixed: bool | None = Field(
        False,
        description="When set the signer will not be able to change its scribble name.\nWhen not set the signer can correct or provide a scribble name.\n",  # noqa
    )
    ScribbleName: str | None = Field(
        None,
        description="The name of the signer, this will be pre filled in the scribble form.\nRequired if `ScribbleNameFixed` is set.\n",  # noqa
    )


class SigningCertificate(Verification):
    Issuer: str | None = None
    Subject: str | None = None
    Thumbprint: str | None = None


class SURFnet(Verification):
    Uid: str | None = None
    Attributes: list[str] | None = Field(
        None,
        description="Contains all available SURFnet attributes.\nThese attributes may change, therefore we cannot guarantee the availability of any of these attributes.\n",  # noqa
    )


class Rel(Enum):
    file = "file"
    receipt = "receipt"
    signer_sign = "signer.sign"
    signer_download = "signer.download"


class Link(BaseModel):
    Rel: Rel | None = Field(None, description="The type of file you can download.")
    Type: str | None = Field(
        None,
        description="The type of the file you can expect to download. Include this in your 'Accept' header when requesting the file.",  # noqa
    )
    Link: str | None = Field(None, description="Url containing the link to the file.")


class Signers(BaseModel):
    FormSets: list[str] | None = Field(
        None, description="List of formset keys to be assigned to this signer."
    )


class Type2(Enum):
    Seal = "Seal"
    Signature = "Signature"
    Check = "Check"
    SingleLine = "SingleLine"


class Location(BaseModel):
    Search: str | None = Field(
        None,
        description="The text to search in the pdf document to use as the position for the field. For example `{{Signer1}}`.",  # noqa
    )
    Occurence: int | None = Field(
        None, description="When using text search, only match this matched occurence."
    )
    Top: int | None = Field(
        None, description="Offset from the top of the search text or the page"
    )
    Right: int | None = Field(
        None, description="Offset from the right of the search or the page"
    )
    Bottom: int | None = Field(
        None, description="Offset from the bottom of the search or the page"
    )
    Left: int | None = Field(
        None, description="Offset from the left of the search or the page"
    )
    Width: int | None = Field(
        None,
        description="The width of the field, can’t be used when both Left and Right are specified.\nFor signature and seal fields we suggest a width of 140.\n",  # noqa
    )
    Height: int | None = Field(
        None,
        description="The height of the field, can’t be used when both Bottom and Top are specified.\nFor signature and seal fields we suggest a height of 70.\n",  # noqa
    )
    PageNumber: int | None = Field(
        None, description="On which page the field should be placed."
    )


class FormSets(BaseModel):
    Type: Type2 | None = Field(
        None,
        description="Field type to create.\n\n* Seal is not yet implemented, this will specify the properties of a seal.\n* Signature, specifies a signature field\n* Check, specifies a checkbox. You'll have to set the `value` property\n* SingleLine, specifies a single line textbox\n",  # noqa
    )
    Location: Location | None = Field(
        None,
        description="Specify where the field should be placed within the document.",
    )


class FileMetaData(BaseModel):
    DisplayOrder: int | None = Field(
        None, description="With what order number we'll display the file to the signer"
    )
    DisplayName: str | None = Field(
        None, description="With what name we'll display the file to the signer"
    )
    SetParaph: bool | None = Field(
        None,
        description="Places a copy of the signer's scribble image on the bottom right of every page where no signature is present.\nNote: due to the nature of advanced or qualified digital signatures, paraphs are merely a cosmetic addition.\n",  # noqa
    )
    Signers: dict[str, Signers] | None = Field(
        None,
        description="Map of array of formsets.\nEach key should be a valid signer id.\n",
    )
    FormSets: dict[str, dict[str, FormSets]] | None = Field(
        None,
        description="Map of one or more form set definitions.\nThe key of the map will be the formset name.\nThe value will be the formset definition\n",  # noqa
    )


class ErrorModel(BaseModel):
    Message: str | None = Field(
        None, description="Message describing the error in the request."
    )


class Betrouwbaarheidsniveau1(Enum):
    Basis = "Basis"
    Midden = "Midden"
    Substantieel = "Substantieel"
    Hoog = "Hoog"


class DigiDAuthentication(Authentication):
    Bsn: str | None = Field(
        None,
        description="The provided value must match the BSN of the credentials returned by DigiD.\nThe BSN is required to match an '11-proef'.          \n",  # noqa
    )
    Betrouwbaarheidsniveau: Betrouwbaarheidsniveau1 | None = Field(
        None,
        description="The level of confidence with which the identity of the signer has been determined.\nFor further information, please refer to [Logius](https://www.logius.nl/diensten/digid/hoe-werkt-het).\n",  # noqa
    )


class PhoneNumberAuthentication(Authentication):
    Number: str | None = Field(
        None,
        description="The mobile phone number of the signer.\nMust conform to E.164,\n[the international public telecommunication numbering plan](https://en.wikipedia.org/wiki/E.164),\nwhich requires the country calling code (e.g. +31).\n",  # noqa
        example="+31123456789",
    )


class EIDASLogin(Verification):
    Uid: str | None = Field(
        None, description="The unique identifier returned by eIDAS Login."
    )
    Level: str | None = Field(None, description="The Level of Assurance.")
    FirstName: str | None = Field(
        None, description="The first name of the signer as returned by eIDAS Login."
    )
    LastName: str | None = Field(
        None, description="The last name of the signer as returned by eIDAS Login."
    )
    DateOfBirth: date | None = Field(
        None, description="The date of birth of the signer as returned by eIDAS Login."
    )
    Attributes: list[str] | None = Field(
        None,
        description="Contains all available eIDAS Login attributes.\nThese attributes may change, therefore we cannot guarantee the availability of any of these attributes.\n",  # noqa
    )


class ItsmeIdentification(Verification):
    PhoneNumber: str | None = Field(
        None,
        description="The mobile phone number of the signer.\nMust be conform E.164,\n[the international public telecommunication numbering plan](https://en.wikipedia.org/wiki/E.164),\nwhich requires the country calling code (Only the Belgian country calling code is supported: +32).\n",  # noqa
        example="+32123456789",
    )
    Attributes: list[str] | None = Field(
        None,
        description="Contains all available itsme Identification attributes.\nThese attributes may change, therefore we cannot guarantee the availability of any of these attributes.\n",  # noqa
    )


class ItsmeSign(Verification):
    Issuer: str | None = None
    Subject: str | None = None
    Thumbprint: str | None = None


class ZealiDQualified(Verification):
    Issuer: str | None = None
    Subject: str | None = None
    Thumbprint: str | None = None


class Signer(BaseModel):
    Id: str | None = Field(
        None,
        description="The id of the signer, must be unique within a transaction.\nIf you don't provide an id we will generate one for you.\n",  # noqa
    )
    Email: str = Field(
        ...,
        description="The e-mail address of the signer",
        example="john.doe@example.com",
    )
    IntroText: str | None = Field(
        None,
        description="An intro text to show to the user during the sign proces.\nThis will be shown on the first screen to the signer and supports limitted markdown markup.\n\nThe following markup is supported:\n- `# Headings`\n- `*Emphasis*` / `_Emphasis_`\n- `**Stong**` / `__Strong__`\n- `1. Ordered` and `- Unordered` lists\n",  # noqa
    )
    Authentications: list[Authentication] | None = Field(
        None,
        description="List of authentications that the signer has to authenticate with.\nThe order in which the authentications are provided determine in which order the signer will have to perform the specified method.\n\nAuthentications must be performed before the document(s) can be viewed.\n\nYou **must** explicitly specify the API-version when using this feature.\nThis is done with the header: 'Accept: application/vnd.signhost.v1+json'.\n",  # noqa
    )
    Verifications: list[Verification] | None = Field(
        None,
        description="List of verifications that the signer has to verify with.\nThe order in which the verifications are provided determine in which order the signer will have to perform the specified method.\n\nVerifications must be performed before the document(s) can be signed.\n\nYou **must** use one of the following verifications as the last method:\n- Consent\n- itsme sign*\n- PhoneNumber\n- Scribble\n- SigningCertificate*\n- ZealiD Qualified*\n\n* These verifications can not be used in any other position than the last.\n",  # noqa
    )
    SendSignRequest: bool | None = Field(
        True, description="Send a sign invitation to the signer his e-mail address."
    )
    SignUrl: str | None = Field(
        None,
        description="A unique URL per signer that provides the signing flow for the signer.\nAvailable / valid if `SendSignRequest` is set to false.\n",  # noqa
    )
    SignRequestSubject: str | None = Field(
        None,
        description="The subject of the sign request email in plain text.\nMaximum of 64 characters allowed.\nOmitting this parameter will enable the default subject.\n",  # noqa
    )
    SignRequestMessage: str = Field(
        None,
        description="The message of the sign request in plain text.\nNewlines can be created by including a \\n in the json, HTML is not allowed.\nRequired if `SendSignRequest` is true\n",  # noqa
    )
    SendSignConfirmation: bool | None = Field(
        None,
        description="Send the sign confirmation to the signer his e-mail address.\nDefault value is the value of `SendSignRequest`\n",  # noqa
    )
    Language: Language1 | None = Field(
        "nl-NL",
        description="The language of the receiving user, only de-DE, en-US, es-ES, fr-FR, it-IT, pl-PL and nl-NL are allowed.",  # noqa
    )
    ScribbleName: str | None = Field(
        None,
        description="The name of the signer, this will be pre filled in the scribble form.",
    )
    DaysToRemind: int | None = Field(
        7,
        description="Amount of days before reminding the signers. -1 to disable reminders.\nIgnored if `SendSignRequest` is set to false.\nBy default your organisation's setting will be used.\n",  # noqa
    )
    Expires: datetime | None = Field(
        None,
        description="When set the signer is no longer allowed to sign the transaction after this date.",
    )
    Reference: str | None = Field(None, description="The reference of the signer.")
    RejectReason: str | None = Field(
        None,
        description="The rejection reason that was given by the signer when the transaction was rejected.",
    )
    ReturnUrl: str | None = Field(
        "https://signhost.com",
        description="The url to redirect the user to after signing, rejecting or cancelling.",
    )
    Context: dict[str, Any] | None = Field(
        None,
        description="Any valid json object which we will return back to you when doing a GET on the transaction or when we send a postback.",  # noqa
    )
    Activities: list[Activity] | None = Field(
        None,
        description="List of activities attached to this signer.\nActivities are added by signhost when a signer event occured.\n",  # noqa
    )


class FileEntry(BaseModel):
    Links: list[Link] | None = None
    DisplayName: str | None = Field(
        None,
        description="The name of the document that was displayed to the user while signing the documents.",
    )


class Transaction(BaseModel):
    Id: str | None = Field(
        None,
        description="The id of the transaction.\nCurrently this property is read only but this may change in the future.\n",  # noqa
    )
    Files: dict[str, FileEntry] | None = Field(
        None, description="A map of files attached to this transaction."
    )
    Language: Language | None = Field(
        None,
        description="The language of the sender notifications and the receipt, only de-DE, en-US, es-ES, fr-FR, it-IT, pl-PL and nl-NL are allowed.",  # noqa
    )
    Seal: bool | None = Field(
        False, description="Seal the document before sending to the signers."
    )
    Signers: list[Signer] = Field(None, description="The signer information.")
    Receivers: list[Receiver] | None = None
    Reference: str | None = Field(
        None, description='The reference of the transaction. For example "1234"'
    )
    PostbackUrl: str | None = Field(
        None,
        description="The absolute url to postback the status updates. For example https://example.com/postback.php",
    )
    SignRequestMode: int | None = Field(
        2,
        description="Set to 1 for sending at once, to 2 for sequential.\nIgnored if `SendSignRequest` is set to false.\n",  # noqa
    )
    DaysToExpire: int | None = Field(
        60, description="Amount of days before expiration. Max 90 days."
    )
    SendEmailNotifications: bool | None = Field(
        True, description="Send e-mail notifications to the sender."
    )
    Status: Status | None = Field(
        None,
        description="Current transaction status.\n\n* 5 - Waiting for document\n* 10 - Waiting for signer\n* 20 - In progress\n* 30 - Signed (end state)\n* 40 - Rejected (end state)\n* 50 - Expired (end state)\n* 60 - Cancelled (end state)\n* 70 - Failed (end state)\n",  # noqa
    )
    CancelationReason: str | None = Field(
        None, description="The original cancellation reason given during a DELETE call."
    )
    Context: dict[str, Any] | None = Field(
        None,
        description="Any valid json object which we will return back to you when doing a GET on the transaction or when we send a postback.",  # noqa
    )
