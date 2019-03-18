from redact_text import redact_text
import pytest


@pytest.mark.parametrize('email', [
    'sagiv.oulu@gmail.com',
    'sagiv.oulu@yahoo.co.il',
])
def test_redact_email(email):
    classified = f'my classified email is {email}'
    redacted = redact_text(classified)
    assert email not in redacted, f'found {email} in redacted output: {redacted}'


@pytest.mark.parametrize('ip', [
    '1.1.1.1',
    '192.168.1.1',
    '221.44.44.44'
])
def test_redact_ip(ip):
    classified = f'my classified ip is {ip}'
    redacted = redact_text(classified)
    assert ip not in redacted, f'found {email} in redacted output: {redacted}'
