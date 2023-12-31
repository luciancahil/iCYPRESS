import argparse


def parse_args(name = "example_custom.yaml" ) -> argparse.Namespace:
    r"""Parses the command line arguments."""
    parser = argparse.ArgumentParser(description='GraphGym')

    parser.add_argument('--cfg',
                        dest='cfg_file',
                        type=str,
                        default='configs/' + name,
                        help='The configuration file path.')
    parser.add_argument('--repeat',
                        type=int,
                        default=1,
                        help='The number of repeated jobs.')
    parser.add_argument('--mark_done',
                        action='store_true',
                        default=[],
                        help='Mark yaml as done after a job has finished.')
    parser.add_argument('opts',
                        default=None,
                        nargs=argparse.REMAINDER,
                        help='See graphgym/config.py for remaining options.')

    return parser.parse_args()
