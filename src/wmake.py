import os
import sys
import subprocess
import private.private as private

def is_file_more_recent(check_path, control_path):
    try:
        # Get the modification time of each file
        check_mtime = os.path.getmtime(check_path)
        control_mtime = os.path.getmtime(control_path)

        # Compare the modification times
        return check_mtime > control_mtime

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return None

def find_hpp_paths():
    hpp_paths = []
    for root, dirs, files in os.walk("include"):
        for file in files:
            if file.endswith('.hpp'):
                hpp_paths.append(os.path.join(root, file))
    return hpp_paths

def find_cpp_paths():
    cpp_paths = []
    for root, dirs, files in os.walk("src"):
        for file in files:
            if file.endswith('.cpp'):
                cpp_paths.append(os.path.join(root, file))
    return cpp_paths

def find_o_paths():
    o_paths = []
    for root, dirs, files in os.walk("build"):
        for file in files:
            if file.endswith('.o'):
                o_paths.append(os.path.join(root, file))
    return o_paths

def get_o_path(cpp_path):
    # Create the build path structure based on the source file structure
    relative_path = os.path.relpath(os.path.dirname(cpp_path), 'src')
    if relative_path == '.':
        relative_path = ''
    build_path = os.path.join("build", relative_path)

    # Extract the file name
    file_name = os.path.splitext(os.path.basename(cpp_path))[0]

    # Construct the output path for the .o file
    return os.path.join(build_path, file_name + '.o')

def should_compile_all_cpp(hpp_paths, target_path):
    for hpp_path in hpp_paths:
        if is_file_more_recent(hpp_path, target_path):
            return True
    return False

def should_compile_cpp_to_o(cpp_path, o_path):
    # If o_path does not exist compile it
    if not os.path.exists(o_path):
        return True

    # If cpp_path is more recent than o_path compile it
    return is_file_more_recent(cpp_path, o_path)

def compile_cpp_to_o(cpp_path, o_path, include_paths):
    # Create the build path structure for o_path
    build_path = os.path.dirname(o_path)
    os.makedirs(build_path, exist_ok=True)

    # Construct the include paths string
    include_paths_str = ' '.join(['-I' + include_path for include_path in include_paths])

    # Compile the .cpp file to a .o file
    command = f'g++ -c {cpp_path} -o {o_path} {include_paths_str}'
    subprocess.run(command, shell=True, check=True)
    print(f'{cpp_path} compiled to {o_path}.')

def compile_and_link(target, include_paths, lib_names, lib_paths):
    # Get paths to the .cpp files, .hpp files, and target
    cpp_paths = find_cpp_paths()
    hpp_paths = find_hpp_paths()
    target_path = os.path.join('bin', target)

    # Error if there are no .cpp files
    if not cpp_paths:
        sys.exit('No .cpp files found.')

    # Detect if a .hpp file is newer than the target
    should_compile_all = should_compile_all_cpp(hpp_paths, target_path)

    # Compile each .cpp file to a .o file
    o_paths = []
    o_path_compiled = False
    for cpp_path in cpp_paths:
        # Get and record o_path
        o_path = get_o_path(cpp_path)
        o_paths.append(o_path)

        # Compile .cpp file if a .hpp file changed or the .cpp is newer than the .o
        if should_compile_all or should_compile_cpp_to_o(cpp_path, o_path):
            compile_cpp_to_o(cpp_path, o_path, include_paths)
            o_path_compiled = True

    # Tell user which o_paths exist but aren't being used in target
    old_o_paths = find_o_paths()
    for old_o_path in old_o_paths:
        if not old_o_path in o_paths:
            print(f"{old_o_path} is not being used and should be deleted.")

    # Exit if no .o files were changed
    if not o_path_compiled:
        sys.exit('No .o files need to be recompiled so no need to rebuild target.')

    # Construct the o_paths, lib_names, and lib_paths strings
    o_paths_str = ' '.join(o_paths)
    lib_names_str = ' '.join([f'-l{lib_name}' for lib_name in lib_names])
    lib_paths_str = ' '.join([f'-L{lib_path}' for lib_path in lib_paths])

    # Determine if building a DLL or an executable based on the specified file name
    if target.endswith('.dll'):
        # Construct the link command for building a DLL
        command = f'g++ -shared -o {target_path} {o_paths_str} {lib_names_str} {lib_paths_str}'
        subprocess.run(command, shell=True, check=True)
        print(f'DLL built successfully as {target_path}')
    elif target.endswith('.exe'):
        # Construct the link command for building an executable
        command = f'g++ -o {target_path} {o_paths_str} {lib_names_str} {lib_paths_str}'
        subprocess.run(command, shell=True, check=True)
        print(f'Executable built successfully as {target_path}')
    else:
        print('Invalid target extension. Please specify a target with either .dll or .exe extension.')

def make():
    private.check_environment()

    config = private.read_config()

    if not "include" in config["include-paths"]:
        config["include-paths"].append("include")

    compile_and_link(config["target"], config["include-paths"], config["lib-names"], config["lib-paths"])

if __name__ == "__main__":
    if len(sys.argv) > 1:
        sys.exit("Too many arguments.")

    make()