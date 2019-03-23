import pytest
import os
from os import path
from pathlib import Path
import ultimo_negro
import re
from redact_text import default_mapping as redaction_mapping


CLASSIFIED_VALIDATION_REGX = [
    '(eilat|la|telaviv|galil)'
]


@pytest.mark.parametrize('filename', [
    'log01.log'
])
def test_un_file(filename):
    project_dir = str(Path(ultimo_negro.__file__).parent)
    samples_dir = path.join(project_dir, 'tests', 'end2end_tests', 'samples')
    file_path = path.join(samples_dir, filename)
    redacted_path = path.join(samples_dir, f'{filename}-REDACTED')

    try:
        # Make sure the sampe log file exists
        assert path.isfile(file_path), f'sample log file not found in {file_path}'
        un_path = f'python {ultimo_negro.__file__}'

        # Redact the file & make sure it didn't fail
        exit_code = os.system(f'{un_path} --classified {file_path}')
        assert exit_code == 0, f'ultimo_negro exited with code: {exit_code}'

        # Make sure redacted file exists
        assert path.isfile(redacted_path), f'Expected to find redacted output in file: {redacted_path}, file not found'

        with open(redacted_path, 'r') as redacted_file:
            redacted = redacted_file.read()
            print(redacted)
            for regx in redaction_mapping.keys():
                assert not re.findall(regx, redacted, flags=re.IGNORECASE), f'Found redacted content in {redacted_path}: {regx}'
    finally:
        # Cleanup: delete redaced file
        if path.isfile(redacted_path):
            os.remove(redacted_path)
