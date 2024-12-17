import utils

# TODO is there a cleaner way to provide o_changed flag

def link_o(cpp_version: int, shared: bool, static: bool, o_paths, target_path: str) -> None:
    # Create directory to put target in
    utils.create_directory(utils.get_file_directory(target_path))

    command = "g++ -std=c++" + str(cpp_version)

    if shared:
        command += " -shared"
    if static:
        command += " -static"

    command += " -o " + target_path + " " + ' '.join(o_paths)

    utils.run_command(command)

    print("Linked " + target_path)

## 'o_changed' should be set to True if client already knows that a .o was changed or deleted.
## 'o_changed' is also the only way that the function knows if a .o was deleted.
def link(cpp_version: int, shared: bool, static: bool, build_dir_path: str, target_path: str, o_changed = False) -> None:
    # Get current o files
    rel_o_paths = utils.get_files_deep(build_dir_path)
    o_paths = utils.add_paths_list(build_dir_path, rel_o_paths)

    if o_changed or not utils.path_exists(target_path):
        link_o(cpp_version, shared, static, o_paths, target_path)
        return

    target_last_modified_time = utils.get_file_last_modified_time(target_path)

    for o_path in o_paths:
        if utils.get_file_last_modified_time(o_path) > target_last_modified_time:
            link_o(cpp_version, shared, static, o_paths, target_path)
            return