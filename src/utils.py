from subprocess import Popen, PIPE
from sha3 import keccak_256 as keccak256
import json

BANNED_VYPER_NAMES = (
    "number", "from", "value"
)
SOL_VY_DIFF = {
    "string" : "String[100]",
    "bytes" : "Bytes[100]",
}


def get_abi_solc(filename: str) -> dict:
    """ Function to get the ABI of a Solidity smart contract using solc.
    :param filename: The name of the Solidity file to get the ABI of.
    :return: A dictionary containing the ABI of the Solidity smart contract.
    """

    proc = Popen(
        ["solc", "--abi", filename],
        stdout=PIPE,
        stderr=PIPE,
    )

    stdout, stderr = proc.communicate()

    if stderr:
        raise Exception(f"Compilation failed. See below:\n{stderr}")

    names_and_abis = list(filter(
        lambda x: (
            (x.startswith("[") and x.endswith("]"))
            or x.startswith(7*"=")
        ),
        stdout
        .decode("utf-8")
        .split("\n")
    ))

    abis = {
        names_and_abis[2*idx].strip(7*"=").strip(): json.loads(names_and_abis[2*idx + 1])
        for idx in range(len(names_and_abis)//2)
    }

    return abis

def get_signature_and_selector(abi_dict: dict) -> list[tuple[str, str]]:
    """
    Given an abi dictionary, return a list of tuples of the form (signature, selector)
    :param abi_dict: a dictionary representing an abi
    """

    sigs_and_selectors = []

    for el in abi_dict:
        
        if el["type"] != "function":
            continue

        name = el["name"]
        inputs = ",".join(
            [f"{_input['type']}" for _input in el["inputs"]]
        )

        function_sig = f"{name}({inputs})"

        sig_hash = keccak256(function_sig.encode("utf-8")).hexdigest()
        sigs_and_selectors.append((function_sig, "0x" + sig_hash[:8]))

    return sigs_and_selectors

def make_vyper_interface(contract_abi: list, name: str) -> str:
    """ Given an abi list, return a vyper interface
    :param abi_dict: a dictionary representing an abi
    :param name: the name of the interface
    :return: a string representing the vyper interface
    """

    interface_name = f"interface {name}:\n"

    functions = []

    for el in contract_abi:

        if el["type"] != "function":
            continue

        for _input in el["inputs"]:
            if _input["type"] in SOL_VY_DIFF:
                _input["type"] = SOL_VY_DIFF[_input["type"]]
            if _input["name"] in BANNED_VYPER_NAMES:
                _input["name"] = _input["name"] + "_"

        name = el["name"]
        inputs = ", ".join(
            [f"{_input['name']}: {_input['type']}" for _input in el["inputs"]]
        )

        function_sig = f"{name}({inputs})"

        if len(el["outputs"]) > 0:

            for _output in el["outputs"]:
                if _output["type"] in SOL_VY_DIFF:
                    _output["type"] = SOL_VY_DIFF[_output["type"]]

            if len(el["outputs"]) == 1:
                function_sig += " -> " + el["outputs"][0]["type"]
            else:
                function_sig += "-> (" + ", ".join([_output["type"] for _output in el["outputs"]]) + ")"

        mutability = el["stateMutability"]

        functions.append(
            4*" " + f"def {function_sig}: {mutability}"
        )

    return interface_name + "\n".join(functions)