import src.utils as utils
from src.parser import parser

def main():

    args = parser.parse_args()

    if not args.subcommand:
        parser.print_help()
        return

    if args.subcommand == "selector_getter":

        for contract, abi in utils.get_abi_solc(args.filename).items():
            header = 5*"=" + f" {contract} " + 5*"=" + "\n" 
            output = header + "\n".join(map(
                lambda x: f"    {x[0]} => {x[1]}",
                utils.get_signature_and_selector(abi)
            )) + "\n"
            print(output)
            return

    if args.subcommand == "vyper_interface_maker":
        
        for contract, abi in utils.get_abi_solc(args.filename).items():
            name = contract.split(":")[-1]
            if not name.startswith("I"):
                name = "I" + name
            print(utils.make_vyper_interface(abi, name))
            return

    if args.subcommand == "filter_selectors":

        for contract, abi in utils.get_abi_solc(args.filename).items():
            header = 5*"=" + f" {contract} " + 5*"=" + "\n" 
            output = header + "\n".join(map(
                lambda x: f"    {x[0]} => {x[1]}",
                filter(
                    lambda x: x[1].startswith(args.selector),
                    utils.get_signature_and_selector(abi)
                )
            ))

            if output == header:
                print(f"No selector starting with {args.selector} found")
                return
            print(output)
            return

if __name__ == "__main__":
    main()