
"""

Zepto ELN core: Core ZeptoELN library, including functions, and CLIs for reading/parsing/analyzing/converting
ZeptoELN markdown documents, and generating reports and HTML pages..

For local and online journal presentation.

Can be used together with ZeptoELN-Server for serving Markdown documents as HTML-compiled web pages.

"""

# from distutils.core import setup
from setuptools import find_packages, setup


# To update entry points, just bump verison number and do `$ pip install -e .`
# Update 'version' for each new release.
# OBS: ZeptoELN is distributed as namespace packages.
# This means that the top-level "zepto_eln" cannot contain any `__init__.py`
# file in ANY of the projects that use the zepto_eln namespace.
# See https://packaging.python.org/guides/packaging-namespace-packages/#native-namespace-packages
# Example: https://github.com/pypa/sample-namespace-packages
setup(
    name='zepto-eln-core',  # old names: eln-md-pico-server
    description=('Core ZeptoELN library, including functions, and CLIs for reading/parsing/analyzing/converting '
                 'ZeptoELN markdown documents, and generating reports and HTML pages..'),
    long_description=__doc__,
    # long_description=open('README.txt').read(),
    version='0.0.4',  # Update for each new version
    # Since we are using namespace distributions, we must manually list all sub-packages to include in the dist.
    packages=['zepto_eln.md_utils', 'zepto_eln.eln_cli'],
    url='https://github.com/scholer/zepto-eln-core',
    # download_url='https://github.com/scholer/rsenv/tarball/0.1.0',
    download_url='https://github.com/scholer/zepto-eln-core/archive/master.zip',  # Update for each new version
    author='Rasmus Scholer Sorensen',
    author_email='rasmusscholer@gmail.com',
    license='GNU Affero General Public License v3',
    keywords=[
        "ELN", "Journal", "Research", "wiki",
        "Molecular biology", "Biotechnology", "Bioinformatics",
        "DNA", "DNA sequences", "sequence manipulation",
        "Data analysis", "Data processing", "plotting", "Data visualization",
        "Image analysis", "AFM", "Microscopy", "TEM", "HPLC", "Chromatograms",
    ],

    # Automatic script creation using entry points has largely super-seeded the "scripts" keyword.
    # you specify: name-of-executable-script: [package.]module:function
    # When the package is installed with pip, a script is automatically created (.exe for Windows).
    # The entry points are stored in ./gelutils.egg-info/entry_points.txt, which is used by pkg_resources.
    entry_points={
        'console_scripts': [
            # console_scripts should all be lower-case, else you may get an error when uninstalling:
            'eln-print-started-exps=zepto_eln.eln_cli.reports_cli:print_started_exps_cli',
            'eln-print-unfinished-exps=zepto_eln.eln_cli.reports_cli:print_unfinished_exps_cli',
            'eln-print-journal-yfm-issues=zepto_eln.eln_cli.reports_cli:print_journal_yfm_issues_cli',
            'eln-md-to-html=zepto_eln.eln_cli.converter_cli:convert_md_file_to_html_cli',
        ],
    },

    install_requires=[
        'pyyaml',
        'markdown',
        'requests',  # Used for github-markdown parsing.
        'click',     # Easy creation of command line interfaces (CLI).
        # 'python-dotenv',
    ],
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        # 'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Healthcare Industry',

        # 'Topic :: Software Development :: Build Tools',
        'Topic :: Education',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',

        # Pick your license as you wish (should match "license" above)
        # 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'License :: OSI Approved :: GNU Affero General Public License v3',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',

        'Operating System :: MacOS',
        'Operating System :: Microsoft',
        'Operating System :: POSIX :: Linux',
    ],

)
