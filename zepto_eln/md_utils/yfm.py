# Copyright 2018 Rasmus Scholer Sorensen

"""

Module for extracting and parsing YAML Front-Matter from documents.

"""

import re
import yaml
import sys
# try:
#     import frontmatter
# except ImportError:
#     print("`frontmatter` package not available; using local routines.")
#     frontmatter = None
# The frontmatter package doesn't provide very good error control, unless you go so low-level
# that it is easier to just use re.split() + yaml.load() directly.

YFM_boundary_regex = re.compile(r'^-{3,}$', re.MULTILINE)


def split_yfm(raw_content, sep_regex=YFM_boundary_regex, require_leading_marker='raise', require_empty_pre=True):
    """ Split raw_content into two parts, YAML frontmatter part and the main content part.



    Args:
        raw_content: The input text to split YFM from.
        sep_regex: The regex pattern to use to split the YFM from the main content.
        require_leading_marker: Will require the YFM to be prefixed with the sep_regex pattern, i.e. "---\n".
            If 'raise' or True, will raise ValueError.
            If 'warn', simply provide a warning on sys.stderr.
        require_empty_pre: If True

    Returns:
        (yfm_content, md_content) 2-tuple,
        where yfm_content is the text-string containing the yfm,
        and md_content is the rest of the document after the YFM.

    Raises:

        ValueError, if raw_content can only be split into two parts, and require_leading_marker is True or 'raise'.
        ValueError, if raw_content can only be split into one part.
        AssertingError, if there is any text before the first boundary marker, and require_empty_pre is True.

    """
    if isinstance(sep_regex, str):
        sep_regex = re.compile(sep_regex, re.MULTILINE)
    splitted = sep_regex.split(raw_content, 2)  # Split at most two times (into three parts) on regex matches.

    if len(splitted) == 1:
        raise ValueError(f"Unable to extract YAML frontmatter from text; "
                         f"no matches for boundary marker {sep_regex.pattern!r}")
    if len(splitted) == 2:
        if require_leading_marker:
            if require_leading_marker == 'warn':
                print(f"WARNING: Only found one YFM boundary marker ({sep_regex.pattern!r}).", file=sys.stderr)
            else:
                raise ValueError(f"Only found one YFM boundary marker ({sep_regex.pattern!r}).")
        yfm_content, md_content = splitted
    else:
        pre, yfm_content, md_content = splitted
        if require_empty_pre:
            if not pre.strip():
                raise AssertionError(f"Non-empty text before YFM boundary marker ({sep_regex.pattern!r}). Text is:"
                                     f"{pre}" if len(pre) < 100 else f"{len(pre)} chars.")
    return yfm_content, md_content


# def parse_with_frontmatter(text):
#     """ Parse, using the 'frontmatter' package. Reference function mostly.
#
#     There are at least two 'frontmatter' projects:
#         * https://github.com/eyeseast/python-frontmatter - 95 stars
#         * https://github.com/jonbeebe/frontmatter - 2 stars
#             * This is only about 40 lines of code, with a weird use of class methods.
#             *
#
#     What is the behavior of eyeseast/python-frontmatter ?
#
#         * frontmatter.parse(text, **default_metadata):
#             * Returns (default_metadata, text) 2-tuple if we fail to split YFM.
#             * strips() content after extracting YFM.
#             * I don't like that `default_metadata` is using **kwargs contraction.
#                 What if I want a default attribute key called 'text', or 'handler', or 'encoding'?
#                 Why not just have a dict argument? Poor design decision.
#         * frontmatter.Post class
#         * frontmatter.dumps(post) to serialize a Post using a template. However, this is just basic python formatting,
#             not e.g. Jinja.
#
#         * The best approach is probably to use frontmatter.default_handlers.YAMLHandler directly:
#             * YAMLHandler.split() to check if document contains a frontmatter section.
#                 * This is simply YAMLHandler.FM_BOUNDARY.split(text, 2), where
#                     `FM_BOUNDARY = re.compile(r'^-{3,}$', re.MULTILINE)`.
#                 * This gives a ValueError "not enough values to unpack (expected 3, got 1)" if
#             * YAMLHandler.load(fm, **kwargs) simply calls yaml.load(fm, **kwargs), using SafeLoader as default.
#
#     In conclusion:
#         * There isn't really much to gain from using the frontmatter package.
#         * We loose control of how errors are handled, unless we use YAMLHandler directly, in which case the small
#             number of lines of code that we use don't really justifying adding an additional project dependency.
#
#     """
#     import frontmatter
#     from frontmatter import YAMLHandler
#     # Unfortunately, frontmatter.parse doesn't have any way to determine if splitting gives an error (only YAML load).
#     metadata, content = frontmatter.parse(text, handler=YAMLHandler)
#     return metadata, content


def parse_yfm(raw_content, sep_regex=YFM_boundary_regex, require_leading_marker='raise', require_empty_pre=True):
    """ Parse Yaml Front Matter from text and return metadata dict and stripped content.

    Args:
        raw_content:
        sep_regex: The regex on which the YFM is separated from the surrounding text.
        require_leading_marker: Raise error if only one YFM marker is found.
        require_empty_pre: Raise error if the part before the YFM is not empty.

    Returns:
        Two-tuple of (frontmatter/metadata dict, and remaining, stripped, content).

    Raises:
        ValueError, if there is an error splitting YFM from raw_content (e.g. missing boundaries).
        AssertionError, if `require_empty_pre` is True and there is any text before the YFM.
            This is a good way to prevent accidentally interpreting horizontal lines `---`
            in the content as an YFM boundary marker.
        yaml.error.YAMLError
        +- yaml.error.MarkedYAMLError
            +- yaml.scanner.ScannerError, if there is an error in the YFM YAML markup.
    """

    yfm_content, md_content = split_yfm(
        raw_content, sep_regex=sep_regex,
        require_leading_marker=require_leading_marker, require_empty_pre=require_empty_pre)
    yfm = yaml.load(yfm_content, Loader=yaml.SafeLoader)  # Exceptions caught in outer functions that knows filename.
    return yfm, md_content
