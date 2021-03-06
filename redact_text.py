import logging
import re


default_mapping = {
    r'([a-z0-9_-]*?)@[^.\s]+(?:\.[^.\s]+)*': r'DOMAIN_USER',
    r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)': 'REDACTED_IP',
    r'(telaviv|eilat|la|galil)': 'REDACTED_SITE'
}


def redact_text(classified, mapping=None):
    """
    Redacts the given text, using a [{regular expression: replacement}, ...] mapping.

    :param classified: Classified text to redact.
    :param mapping: A dict for redacting classified text. the
        keys are regular expression, & the values are the replacing strings.
        If not given a default mapping will be used
        Note: this function uses the re.sub function, so you can use syntax
        such as \g<1> to replace strings.
    :return: The redacted version of the classified string.
    """

    if not mapping:
        mapping = default_mapping
    redacted = classified
    for pattern, substitute in mapping.items():
        redacted, count = re.subn(pattern, substitute, redacted, flags=re.IGNORECASE)
        logging.debug(f'Replaced {pattern} to {substitute} {count} times')
    return redacted
