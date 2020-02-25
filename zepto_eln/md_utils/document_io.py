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


class DocumentYfmError(Exception):

    def __init__(self, msg="", file=None, causing_exception=None):
        super().__init__(msg)
        self.msg = msg
        self.file = file
        self.causing_exception = causing_exception

    def __str__(self):
        return (f"Error while parsing document YFM "
                f"(msg: {self.msg}, file: '{self.file}', causing_exception: {self.causing_exception!r})")


def find_md_files(basedir='.'):
    return glob.glob(os.path.join(basedir, '**/*.md'))


def load_document(
        filepath, add_fileinfo_to_meta=True,
        yfm_parsing=True, yfm_errors='raise', meta_if_no_yfm=None,
):
    """ Reads a document file and extracts the metadata / YAML front matter and the main content.

    Args:
        filepath: The document file to read.
        add_fileinfo_to_meta: Whether to add file info directly into the main document dict.
            Adding file info like this may clutter/override metadata from the YFM.
        yfm_parsing: Attempt to parse YAML front-matter (YFM) from file.
        yfm_errors: What to do if an error is encountered during YFM parsing,
            e.g. 'raise' to raise an exception or 'warn' to print a warning to sys.stderr.

    Returns:
        document dict, with keys:
            filename:
            fileinfo:
            raw_content: The whole file content.
            content: The markdown content part of the file.
            meta: The YFM metadata.

    """
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
    if yfm_parsing:
        try:
            yfm, md_content = parse_yfm(raw_content)
        except (yaml.error.YAMLError, ValueError, AssertionError) as exc:
            # Hmm, I'm not really sure about this approach of "tell the inner function which errors to ignore".
            # There is at least 4 known errors that may arise when trying to parse_yfm of content from a text file.
            # It is probably better to catch this in the outer function.
            # Or maybe have a "require_yfm" or "raise_if_no_yfm" or "raise_yfm_errors" or "missing_yfm_behavior"?
            # Maybe check the behavior of the "frontmatter" package to make it consistent.
            if 'warn' in yfm_errors or 'report' in yfm_errors:
                print(f"WARNING: {exc!r} while parsing YFM of file {filepath}.")
            if 'raise' in yfm_errors:
                raise DocumentYfmError(msg="", file=filepath, causing_exception=exc)
            # else, e.g. yfm_errors='ignore':
            yfm = meta_if_no_yfm
            md_content = raw_content
    else:
        yfm, md_content = None, raw_content

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
        basedir='.', add_fileinfo_to_meta=True, exclude_if_missing_yfm=True, yfm_parsing=True, yfm_errors='skip-file'):
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
        if yfm_errors == 'skip-file':
            try:
                document = load_document(fn, add_fileinfo_to_meta=add_fileinfo_to_meta, yfm_parsing=yfm_parsing)
            except DocumentYfmError:
                pass
            else:
                documents.append(document)
        else:
            document = load_document(
                fn, add_fileinfo_to_meta=add_fileinfo_to_meta, yfm_parsing=yfm_parsing, yfm_errors=yfm_errors
            )
            if document['meta'] is not None or not exclude_if_missing_yfm:
                documents.append(document)
    return documents


def load_all_documents_metadata(
        basedir='.', add_fileinfo_to_meta=True, yfm_parsing=True, yfm_errors='skip-file',
        exclude_if_missing_yfm=True):
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
        yfm_parsing=yfm_parsing, yfm_errors=yfm_errors,
        exclude_if_missing_yfm=exclude_if_missing_yfm
    )
    # print("\n".join("{}: {}".format(j['filename'], type(j['meta'])) for j in journals))
    metadata = [document['meta'] for document in documents]
    return metadata


