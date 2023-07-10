from signhost.models import Signer
from signhost.models import verifications


def test_validation_discriminated_union() -> None:
    s = Signer(
        Verifications=[
            verifications.Consent(),
            verifications.DigiD(),
            verifications.EHerkenning(),
            verifications.IDeal(),
            verifications.IDIN(),
            verifications.IPAddress(),
            verifications.PhoneNumber(),
            verifications.Scribble(),
            verifications.SigningCertificate(),
            verifications.SURFnet(),
        ],
        Email="test@pytest.io",
    )

    p = Signer.model_validate(s.model_dump())

    assert isinstance(p.Verifications[0], verifications.Consent)
    assert isinstance(p.Verifications[1], verifications.DigiD)
    assert isinstance(p.Verifications[2], verifications.EHerkenning)
    assert isinstance(p.Verifications[3], verifications.IDeal)
    assert isinstance(p.Verifications[4], verifications.IDIN)
    assert isinstance(p.Verifications[5], verifications.IPAddress)
    assert isinstance(p.Verifications[6], verifications.PhoneNumber)
    assert isinstance(p.Verifications[7], verifications.Scribble)
    assert isinstance(p.Verifications[8], verifications.SigningCertificate)
    assert isinstance(p.Verifications[9], verifications.SURFnet)
