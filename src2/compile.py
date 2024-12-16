import dep
import utils

def cpp_to_o(src_dir_path: str, build_dir_path: str, cpp_path: str) -> str:
    return utils.replace_file_extension(utils.add_paths(build_dir_path, utils.subtract_paths(cpp_path, src_dir_path)), ".o")

def o_to_cpp(src_dir_path: str, build_dir_path: str, o_path: str) -> str:
    return utils.replace_file_extension(utils.add_paths(src_dir_path, utils.subtract_paths(o_path, build_dir_path)), ".cpp")

def compile_cpp(cpp_path: str, o_path: str) -> None:
    # Create the build path structure for o_path
    #build_path = os.path.dirname(o_path) # TODO make a utils function for this
    #os.makedirs(build_path, exist_ok=True) # TODO make a utils function for this

    # Construct the include paths string
    #include_paths_str = ' '.join(['-I' + include_path for include_path in include_paths])

    # Compile the .cpp file to a .o file
    #command = f'g++ -std=c++{cpp_version} -c {cpp_path} -o {o_path} {include_paths_str}'
    #subprocess.run(command, shell=True, check=True) # TODO make a utils function for this
    #print(f'{cpp_path} compiled to {o_path}.')

    print("Compiled " + cpp_path + " to " + o_path)

## Returns whether a .o was compiled or removed.
def compile(src_dir_path: str, include_dir_paths: list, build_dir_path: str) -> bool:
    o_changed = False

    # Get info
    dep_graph = dep.DepGraph(src_dir_path, include_dir_paths)
    cpp_paths = dep_graph.get_cpp_paths()
    cpp_last_modified_times = dep_graph.get_cpp_last_modified_times()
    o_paths = utils.get_files_deep(build_dir_path)

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
                compile_cpp(cpp_path, o_path)
                o_changed = True
        else:
            # Compile .cpp because a .o doesn't exist
            compile_cpp(cpp_path, o_path)
            o_changed = True

    return o_changed
