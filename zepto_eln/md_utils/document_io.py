# Copyright 2018, Rasmus S. Sorensen, rasmusscholer@gmail.com

"""

Module for loading markdown documents, including parsing of optional YAML frontmatter (YFM) metadata.




"""


import os
import glob
import yaml
import yaml.scanner
from collections import defaultdict
from pprint import pprint

from .yfm import parse_yfm

WARN_MISSING_YFM = False
WARN_YAML_SCANNER_ERROR = True
NODEFAULT = object()


def find_md_files(basedir='.'):
    return glob.glob(os.path.join(basedir, '**/*.md'))


def load_document(filepath, add_fileinfo_to_meta=True, warn_yaml_scanner_error=None):
    """ Reads a document file and extracts the metadata / YAML front matter and the main content.

    Args:
        filepath: The document file to read.
        add_fileinfo_to_meta: Whether to add file info directly into the main document dict.
            Adding file info like this may clutter/override metadata from the YFM.
        warn_yaml_scanner_error:

    Returns:
        document dict, with keys:
            filename:
            fileinfo:
            raw_content: The whole file content.
            content: The markdown content part of the file.
            meta: The YFM metadata.

    """
    if warn_yaml_scanner_error is None:
        warn_yaml_scanner_error = WARN_YAML_SCANNER_ERROR
    dirname, basename = os.path.split(filepath)
    fnroot, fnext = os.path.splitext(basename)
    filepath_root, fnext = os.path.splitext(filepath)  # filepath_root
    fileinfo = {
        'filename': filepath,
        'filepath': filepath,
        'dirname': dirname,
        'basename': basename,
        'fnext': fnext,
        'fnroot': fnroot, 'filename_noext': fnroot,  # alias
        'filepath_root': filepath_root, 'filepath_noext': filepath_root,  # alias
    }
    # print("fileinfo:")
    # pprint(fileinfo)

    with open(filepath, 'r', encoding='utf-8') as fd:
        raw_content = fd.read()
    try:
        yfm, md_content = parse_yfm(raw_content)
    except yaml.scanner.ScannerError as exc:
        # Hmm, I'm not really sure about this approach of "tell the inner function which errors to ignore".
        # There is at least 4 known errors that may arise when trying to parse_yfm of content from a text file.
        # It is probably better to catch this in the outer function.
        # Or maybe have a "require_yfm" or "raise_if_no_yfm" or "raise_yfm_errors" or "missing_yfm_behavior"?
        # Maybe check the behavior of the "frontmatter" package to make it consistent.
        if warn_yaml_scanner_error:
            if warn_yaml_scanner_error == 'raise':
                raise exc
            elif warn_yaml_scanner_error == 'report':
                print(f"WARNING: YAML ScannerError while parsing YFM of file {filepath}.")
        yfm = None
        md_content = None

    if add_fileinfo_to_meta and yfm is not None:
        yfm.update(fileinfo)
    document = {
        'filename': filepath,
        'fileinfo': fileinfo,
        'raw_content': raw_content,
        # 'yfm_content': yfm_content,
        # 'md_content': md_content,
        'content': md_content,
        'meta': yfm,
        # 'meta' or 'metadata'? (Not 'yfm' - I want to be format agnostic)
        # I think I used 'meta' because that's the variablename used by Pico, e.g. '%meta.author%
    }
    return document


def load_all_documents(
        basedir='.', add_fileinfo_to_meta=True, exclude_if_missing_yfm=True, warn_yaml_scanner_error=None):
    """ Find all Markdown documents/journals (recursively) within a given base directory.

    Args:
        basedir: The directory to look for ELN documents/journals in.
        add_fileinfo_to_meta: Whether to add fileinfo to the document's metadata (the parsed YFM).
        exclude_if_missing_yfm: Exclude pages if they don't have YAML front-matter.

    Returns:
        List of documents (dicts).

    """
    files = find_md_files(basedir=basedir)  # glob.glob(os.path.join(basedir, '**/*.md'))
    documents = []
    for fn in files:
        document = load_document(
            fn, add_fileinfo_to_meta=add_fileinfo_to_meta, warn_yaml_scanner_error=warn_yaml_scanner_error
        )
        if document['meta'] is not None or not exclude_if_missing_yfm:
            documents.append(document)
    return documents


def load_all_documents_metadata(
        basedir='.', add_fileinfo_to_meta=True, exclude_if_missing_yfm=True, warn_yaml_scanner_error=None):
    """ Find and load Markdown documents and extract YFM metadata.

    Args:
        basedir: The directory to find journals in.
        add_fileinfo_to_meta: Whether to add fileinfo (e.g. filename, directory, etc).
        exclude_if_missing_yfm: Exclude journals/files if they don't have any YAML front-matter.

    Returns:
        List of metadata dicts (as read from the document YFM).
    """
    documents = load_all_documents(
        basedir=basedir, add_fileinfo_to_meta=add_fileinfo_to_meta,
        exclude_if_missing_yfm=exclude_if_missing_yfm, warn_yaml_scanner_error=warn_yaml_scanner_error
    )
    # print("\n".join("{}: {}".format(j['filename'], type(j['meta'])) for j in journals))
    metadata = [document['meta'] for document in documents]
    return metadata


