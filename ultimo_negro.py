import argparse
from argparse import RawTextHelpFormatter
import logging
from ntpath import basename
import os
from os.path import isdir, isfile
import rarfile
from rarfile import RarFile
from redact_text import redact_text
import shutil
import tarfile
import zipfile


def extractable(path):
    """
    Checks if the given file is an extractable archive file
    :param path: The path to the file
    :return: True if the path is to an extractable file
    """

    if not isfile(path):
        return False
    file_path_without_extention, extension = split_path(path)
    return extension in ['.zip', '.rar', '.tar', '.tar.gz']


def extract(archive, extract=None, delet_archive=False):
    """
    Extracts the given archive file. currently supports .zip, .rar or .tar archives

    :param archive: Path to archive file.
    :param extract: Path to the extracted files. if not given the
        archive path (without the extention) will be used
    :param delet_archive: If true, the archive file will be deleted after extraction
    :return: None
    """

    file_path_without_extention, extension = split_path(archive)
    if extract:
        assert isdir(extract)
    else:
        os.makedirs(file_path_without_extention)
        extract = file_path_without_extention

    if extension == '.zip':
        with zipfile.ZipFile(archive, "r") as zip_ref:
            zip_ref.extractall(extract)
    elif extension == '.rar':
        with RarFile(archive, 'r') as rf:
            rf.extract(extract)
    elif extension == '.tar':
        with tarfile.open(archive) as tf:
            tf.extractall(extract)
    elif archive.endswith('tar.gz'):
        with tarfile.open(archive, 'r:gz') as tf:
            tf.extractall(archive[0:-1 * len('.tar.gz')])
    else:
        raise Exception(f'Can not extract {extension} file type')

    if delet_archive:
        os.remove(archive)


def is_binary(path):
    """
    Reads the contents of the given file path, and determines if it is a binary file or not.

    :param path: The path to the file to check.
    :return: True if the file is binary, False otherwise.
    """

    assert isfile(path), f'path {path} must be a valid file'
    textchars = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) - {0x7f})
    with open(path, "rb") as f:
        content = f.read(1024)
        return bool(content.translate(None, textchars))


def redact(path):
    """
    Redacts recursevly the given path, untill all files are
    extracted (if they are .zip, .rar, .tar or .tar.gz files), redacted (if they ar text files) &
    deleted (if they are binary files). after extracting archives, the extracted files are redacted as well.

    :param path: A path to a directory or file to redact
    :return: None
    """

    logging.info(f'Redacting path: {path}')
    # If given a dir, redact each item in it
    if isdir(path):
        for item in os.listdir(path):
            redact(os.path.join(path, item))
    else:
        # If given an archive, extract it and redact the directory
        file_path_without_extention, extension = split_path(path)
        if extractable(path):
            logging.info(f'Extracting archive: {path}')
            extract(path, delet_archive=True)
            redact(file_path_without_extention)
        elif is_binary(path):
            logging.info(f'Deleting binary file: {path}')
            os.remove(path)
        else:
            logging.info(f'Redacting file: {path}')
            # The path is a text file, redact its contents
            with open(path, 'r') as f:
                classified = f.read()
                redacted = redact_text(classified)
            with open(path, 'w') as f:
                f.write(redacted)


def split_path(path):
    """
    Returns a tuple (file_path, extension) of the given path

    :param path: Path to split
    :return: Tuple (file_path, extension). for example: /usr/admin/bla.txt -> ('/usr/admin/bla', '.txt')
    """

    if path.endswith('.tar.gz'):
        return path[0:-1 * len('.tar.gz')], '.tar.gz'
    return os.path.splitext(path)


def get_all_file_paths(path):
    """
    Collects all file paths (recursively) in the given path

    :param path: The path to the directory or file
    :returns: A list of strings, containing file paths
    """

    # initializing empty file paths list
    file_paths = []

    if isfile(path):
        return path

    # crawling through directory and subdirectories
    for root, directories, files in os.walk(path):
        for filename in files:
            # join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)

            # returning all file paths
    return file_paths


def main(args):

    # If unrar tool path is given, use it
    if hasattr(args, 'unrar_tool') and args.unrar_tool:
        rarfile.UNRAR_TOOL = args.unrar_tool

    # Copy classified file/dir for redaction
    # file_path_without_extention, extension = split_path(args.classified_path)
    # redacted_path = f'{file_path_without_extention}-REDACTED{extension}'
    redacted_path = f'{args.classified_path}-REDACTED'
    if isfile(args.classified_path):
        if isfile(redacted_path):
            os.remove(redacted_path)
        shutil.copyfile(args.classified_path, redacted_path)
    elif isdir(args.classified_path):
        if isdir(redacted_path):
            shutil.rmtree(redacted_path)
        shutil.copytree(args.classified_path, redacted_path)

    redact(redacted_path)

    # If specified, archive the redacted result & delete the unarchived result
    if args.archive:
        file_path_without_extention, extension = split_path(redacted_path)
        zip_path = f'{file_path_without_extention}.zip'
        if isfile(zip_path):
            os.remove(zip_path)
        if isdir(redacted_path):
            file_paths = get_all_file_paths(redacted_path)
            with zipfile.ZipFile(zip_path, 'w') as zip_file:
                for file_path in file_paths:
                    zip_file.write(file_path, os.path.relpath(file_path, redacted_path))
            shutil.rmtree(redacted_path)
        elif isfile(redacted_path):
            with zipfile.ZipFile(zip_path, 'w') as zip_file:
                zip_file.write(redacted_path, basename(redacted_path))
            os.remove(redacted_path)

    # If over write is given, deleted classified path
    if args.over_write:
        if isdir(args.classified_path):
            shutil.rmtree(args.classified_path)
        elif isfile(args.classified_path):
            os.remove(args.classified_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter,
                                     prog='ultimo_negro',
                                     description='''
Ultimo negro (From spanish meaning "ultimate black") is a tool for
redacting classified documents. given a path to file, directory or archive
file the tool will generate a redacted version of it.
                                     ''',
                                     epilog='''
Notes:
  * The tool can only classify text files. non archive binary files will not
  show in the redacted output

  * The tool modifies the given file, directory or archive. you might want to
  backup the original file
                                     '''
                                     )
    parser.add_argument('-c', '--classified',
                        dest='classified_path',
                        type=str,
                        help='The path to the classified file or directory',
                        required=True)
    parser.add_argument('-u', '--unrar-tool',
                        dest='unrar_tool',
                        type=str,
                        help='''
The path to the unrar tool, this tool is necessary for extracting rar files.
If you don't have rar files, this parameter is irrelevant.
The tool can be downloaded from: https://www.rarlab.com/rar_add.htm
                        ''',
                        required=False)
    parser.add_argument('-o', '--over-write',
                        action='store_true',
                        dest='over_write',
                        default=False,
                        help='''
If specified, classified path will be deleted at the end
''',
                        required=False)
    parser.add_argument('-a', '--archive',
                        action='store_true',
                        dest='archive',
                        default=False,
                        help='If specified result will be archived as a .zip file')
    parser.add_argument('-l', '--log-level',
                        dest='log_level',
                        choices=['DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL'],
                        default='INFO',
                        help='Sets the log level')
    args = parser.parse_args()

    log_level = logging.DEBUG
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=getattr(logging, args.log_level))

    main(args)
