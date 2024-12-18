import sys # TODO make utils functions instead
import make
import utils

# TODO move
CONFIG = "wconfig.json"
EXTERN = "wextern.json"

## Build src and main then run main with 'args'.
def run_main(config: dict, extern: dict, args = []) -> None:
    make.make_main(config, extern)

    bin_dir_path = config["directories"]["bin"]

    target_name = config["targets"]["main"]
    target_path = utils.add_paths(bin_dir_path, target_name)

    utils.run_command(target_path)

## Build src and test then run test with 'filter'.
def run_test(config: dict, extern: dict, args = []) -> None:
    make.make_test(config, extern)

    bin_dir_path = config["directories"]["bin"]

    target_name = "test.exe"
    target_path = utils.add_paths(bin_dir_path, target_name)

    utils.run_command(target_path)

## This is the behavior of wrun.
if __name__ == "__main__":
    target = sys.argv[1]
    args = sys.argv[2:]

    # TODO put this in a library
    if not utils.path_exists(CONFIG):
        raise Exception("No config file found.")
    config = utils.read_json_dict(CONFIG)

    # TODO put this in a library
    extern = {"include-paths": []}
    if utils.path_exists(EXTERN):
        extern = utils.read_json_dict(EXTERN)

    if target == "main":
        run_main(config, extern, args)
    elif target == "test":
        run_test(config, extern, args)
    else:
        raise Exception("Invalid run target " + target)