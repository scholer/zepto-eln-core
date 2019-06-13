
import click

from zepto_eln.eln_utils.eln_config import get_combined_app_config
from zepto_eln.eln_utils.eln_md_to_html import convert_md_files_to_html, convert_md_file_to_html


_SYSCONFIG = get_combined_app_config()
# click.Command(context_settings={'max_content_width': 400})
# Using a Context with max_content_width isn't enough to prevent rewrapping,
# probably have to define a custom click.HelpFormatter.
convert_md_file_to_html_cli = click.Command(
    callback=convert_md_files_to_html,
    name=convert_md_file_to_html.__name__,
    help=convert_md_file_to_html.__doc__,  # Using inspect.getdoc() will un-indent the docstring.
    # context_settings={'max_content_width': 400},  # Control help text rewrapping
    params=[
        click.Option(
            ['--outputfn'], default=_SYSCONFIG.get('outputfn'), help="Specify the Markdown parser/generator to use."),
        click.Option(
            ['--parser'], default=_SYSCONFIG.get('parser'), help="Specify the Markdown parser/generator to use."),
        click.Option(
            ['--extensions'], default=_SYSCONFIG.get('extensions'), multiple=True,
            help="Specify which Markdown extensions to use."),
        click.Option(
            ['--template'], default=_SYSCONFIG.get('template'),
            help="Load and apply a specific template (file)."),
        click.Option(
            ['--template-dir'], default=_SYSCONFIG.get('template_dir'),
            help="The directory to look for templates. Each markdown file can then choose which template (name) "
                 "to use to render the converted markdown."),
        click.Option(
            ['--apply-template/--no-apply-template'], default=_SYSCONFIG.get('apply_template'),
            help="Enable/disable template application."),
        click.Option(
            ['--open-webbrowser/--no-open-webbrowser'], default=_SYSCONFIG.get('open_webbrowser'),
            help="Open the generated HTML file in the default web browser."),
        click.Option(
            ['--config'], default=None, help="Read a specific configuration file."),
        # click.Option(
        #     ['--default-config/--no-default-config'], default=_SYSCONFIG.get('outputfn'),
        #              help="Enable/disable loading default configuration file."),
        # click.Argument(['inputfn'])  # cannot add help to click arguments.
        click.Argument(['inputfns'], nargs=-1)  # cannot add help to click arguments.
    ]
)
