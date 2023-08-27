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
    "make_inline_vyper_interface",
    help="Computes the inline vyper interface from a .sol file"
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
subparser4_parser = subparsers.add_parser(
    "make_importable_vyper_interface",
    help="Computes the importable vyper interface from a .sol file"
)
subparser4_parser.add_argument(
    "filename",
    help="The name of the .sol file"
)