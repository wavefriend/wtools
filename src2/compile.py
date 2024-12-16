import dep
import utils

def cpp_to_o(src_dir_path: str, build_dir_path: str, cpp_path: str) -> str:
    return utils.replace_file_extension(utils.add_paths(build_dir_path, utils.subtract_paths(cpp_path, src_dir_path)), ".o")

def o_to_cpp(src_dir_path: str, build_dir_path: str, o_path: str) -> str:
    return utils.replace_file_extension(utils.add_paths(src_dir_path, utils.subtract_paths(o_path, build_dir_path)), ".cpp")

## Compile 'cpp_path' to 'o_path' in C++ version 'cpp_version'.
def compile_cpp(cpp_version: int, cpp_path: str, include_dir_paths: list, o_path: str) -> None:
    # Create directory to put .o in
    utils.create_directory(utils.get_file_directory(o_path))

    # Construct the include dir paths string
    include_dir_paths_str = ' '.join(['-I' + include_dir_path for include_dir_path in include_dir_paths])

    # Compile the .cpp file to a .o file
    utils.run_command(f'g++ -std=c++{cpp_version} -c {cpp_path} -o {o_path} {include_dir_paths_str}')

    print("Compiled " + cpp_path + " to " + o_path)

## Returns whether a .o was compiled or removed.
def compile(cpp_version: int, src_dir_path: str, include_dir_paths: list, build_dir_path: str) -> bool:
    o_changed = False

    # Get cpps and cpp last modified times
    dep_graph = dep.DepGraph(src_dir_path, include_dir_paths)
    cpp_paths = dep_graph.get_cpp_paths()
    cpp_last_modified_times = dep_graph.get_cpp_last_modified_times()

    # Get current o files
    rel_o_paths = utils.get_files_deep(build_dir_path)
    o_paths = utils.add_paths_list(build_dir_path, rel_o_paths)

    # Remove unused .o files
    for o_path in o_paths:
        cpp_path = o_to_cpp(src_dir_path, build_dir_path, o_path)

        # Delete .o if it doesn't correspond to a .cpp
        if not cpp_path in cpp_paths:
            utils.delete_path(o_path)
            o_changed = True
            print("Deleted " + o_path)

    # Compile .cpp files
    for cpp_path in cpp_paths:
        o_path = cpp_to_o(src_dir_path, build_dir_path, cpp_path)

        if o_path in o_paths:
            # Compile .cpp if it was modified more recently than the .o
            if cpp_last_modified_times[cpp_path] > utils.get_file_last_modified_time(o_path):
                compile_cpp(cpp_version, cpp_path, include_dir_paths, o_path)
                o_changed = True
        else:
            # Compile .cpp because a .o doesn't exist
            compile_cpp(cpp_version, cpp_path, include_dir_paths, o_path)
            o_changed = True

    return o_changed
