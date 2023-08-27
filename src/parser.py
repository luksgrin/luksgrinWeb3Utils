import argparse

parser = argparse.ArgumentParser(
    prog="luksgrin's utils launcher",
    description="A launcher for luksgrin's utils",
)

subparsers = parser.add_subparsers(
    dest="subcommand"
)

subparser1_parser = subparsers.add_parser(
    "selector_getter",
    help="Computes the selectors present in a given .sol file"
)
subparser1_parser.add_argument(
    "filename",
    help="The name of the .sol file"
)
subparser2_parser = subparsers.add_parser(
    "vyper_interface_maker",
    help="Computes the vyper interface from a .sol file"
)
subparser2_parser.add_argument(
    "filename",
    help="The name of the .sol file"
)
subparser3_parser = subparsers.add_parser(
    "filter_selectors",
    help="Checks if a given selector is present in a .sol file"
)
subparser3_parser.add_argument(
    "filename",
    help="The name of the .sol file"
)
subparser3_parser.add_argument(
    "selector",
    help="The selector to filter"
)