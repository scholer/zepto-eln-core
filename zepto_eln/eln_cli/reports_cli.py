# Copyright 2018 Rasmus Scholer Sorensen, <rasmusscholer@gmail.com>

import inspect
import click

from zepto_eln.eln_utils.eln_md_pico import print_document_yfm_issues
from zepto_eln.eln_utils.eln_exp_filters import print_started_exps, print_unfinished_exps


print_started_exps_cli = click.Command(
    callback=print_started_exps,
    name=print_started_exps.__name__,
    help=inspect.getdoc(print_started_exps),
    params=[
        # remember: param_decls is a list, *decls.
        click.Option(['--rowfmt'], default='{status:^10}: {expid:<10} {titledesc}'),
        click.Argument(
            ['basedir'], default='.', nargs=1, type=click.Path(dir_okay=True, file_okay=False, exists=True))
])


print_unfinished_exps_cli = click.Command(
    callback=print_unfinished_exps,
    name=print_unfinished_exps.__name__,
    help=inspect.getdoc(print_unfinished_exps),
    params=[
        click.Option(['--rowfmt'], default='{status:^10}: {expid:<10} {titledesc:<40}  [enddate: {enddate}]'),
        click.Argument(
            ['basedir'], default='.', nargs=1, type=click.Path(dir_okay=True, file_okay=False, exists=True))
])


print_journal_yfm_issues_cli = click.Command(
    callback=print_document_yfm_issues,
    name=print_document_yfm_issues.__name__,
    help=inspect.getdoc(print_document_yfm_issues),
    params=[
        # click.Option(['--rowfmt'], default='{status:^10}: {expid:<10} {titledesc} (enddate={enddate})'),
        click.Argument(
            ['basedir'], default='.', nargs=1, type=click.Path(dir_okay=True, file_okay=False, exists=True))
])



if __name__ == '__main__':
    # For testing only...
    # print_started_exps_cli()
    # print_unfinished_exps_cli()
    print_journal_yfm_issues_cli()
    # convert_md_file_to_html_cli()
