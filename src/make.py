import compile_and_link
import sys # TODO make utils functions instead
import utils

# TODO add commands for getting args and exiting command sequence early
#      possibly instead of raise?
# TODO clean up all raise statements to be written in consistent style
# TODO make consistent order of include_dir and src_dir in places
# TODO verify all paths in wconfig are relative and within project folder
# TODO replace build-src/build-main/... with just a single "build" directory
# TODO should we really refer to the test and main dirs as the src dir sometimes?
# TODO do something to correct paths in json files for the platform
# TODO find some way to move all this repetition into helpers
# TODO possibly combine config and extern into one python object
# TODO print something out when nothing is changed to say nothing needed to change
# TODO we need to trigger a complete rebuild if wconfig or wextern is changed
# TODO should extern be split up by main/src/test? should config not be?

# TODO move
CONFIG = "wconfig.json"
EXTERN = "wextern.json"

def make_src(config: dict, extern: dict) -> None:
    cpp_version = config["c++"]

    include_dir_paths = [config["directories"]["include"]] + extern["include-paths"]
    lib_names = config["dependencies"]["src"]
    lib_dir_paths = extern["lib-paths"]
    src_dir_path = config["directories"]["src"]
    build_dir_path = config["directories"]["build-src"]
    bin_dir_path = config["directories"]["bin"]

    target_name = config["targets"]["src"]
    target_path = utils.add_paths(bin_dir_path, target_name)

    compile_and_link.compile_and_link(cpp_version, True, False, \
                                      src_dir_path, include_dir_paths, lib_names, lib_dir_paths, \
                                      build_dir_path, target_path)

# TODO needs to include the dll from src
def make_main(config: dict, extern: dict) -> None:
    make_src(config, extern)

    cpp_version = config["c++"]

    include_dir_paths = [config["directories"]["include"]] + extern["include-paths"]
    lib_names = config["dependencies"]["src"] + config["dependencies"]["main"]
    lib_dir_paths = [config["directories"]["bin"]] + extern["lib-paths"]
    src_dir_path = config["directories"]["main"]
    build_dir_path = config["directories"]["build-main"]
    bin_dir_path = config["directories"]["bin"]

    target_name = config["targets"]["main"]
    target_path = utils.add_paths(bin_dir_path, target_name)

    compile_and_link.compile_and_link(cpp_version, False, False, \
                                      src_dir_path, include_dir_paths, lib_names, lib_dir_paths, \
                                      build_dir_path, target_path)

# TODO needs to include the dll from src
def make_test(config: dict, extern: dict) -> None:
    make_src(config, extern)

    cpp_version = config["c++"]

    include_dir_paths = [config["directories"]["include"]] + extern["include-paths"]
    lib_names = config["dependencies"]["src"] + config["dependencies"]["test"]
    lib_dir_paths = [config["directories"]["bin"]] + extern["lib-paths"]
    src_dir_path = config["directories"]["test"]
    build_dir_path = config["directories"]["build-test"]
    bin_dir_path = config["directories"]["bin"]

    target_name = "test.exe"
    target_path = utils.add_paths(bin_dir_path, target_name)

    compile_and_link.compile_and_link(cpp_version, False, False, \
                                      src_dir_path, include_dir_paths, lib_names, lib_dir_paths, \
                                      build_dir_path, target_path)

## This is the behavior of wmake.
if __name__ == "__main__":
    target = sys.argv[1]

    # TODO put this in a library
    if not utils.path_exists(CONFIG):
        raise Exception("No config file found.")
    config = utils.read_json_dict(CONFIG)

    # TODO put this in a library
    extern = {"include-paths": []}
    if utils.path_exists(EXTERN):
        extern = utils.read_json_dict(EXTERN)

    if target == "src":
        make_src(config, extern)
    elif target == "main":
        make_main(config, extern)
    elif target == "test":
        make_test(config, extern)
    else:
        raise Exception("Invalid make target " + target)