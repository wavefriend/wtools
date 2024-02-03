import os
import sys
import subprocess
import private.private as private

# todo: we need to delete unused .o files
# todo: we should only relink if a .o file is newer than the target

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

def find_cpp_files(dir='.'):
    cpp_files = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith('.cpp'):
                cpp_files.append(os.path.join(root, file))
    return cpp_files

def compile_cpp_to_o(cpp_file, include_dirs, output_dir, force_rebuild=False):
    # Create the build directory structure based on the source file structure
    relative_path = os.path.relpath(os.path.dirname(cpp_file), 'src')
    build_directory = os.path.join(output_dir, relative_path)
    os.makedirs(build_directory, exist_ok=True)

    # Extract the file name
    file_name = os.path.splitext(os.path.basename(cpp_file))[0]

    # Construct the output path for the .o file
    output_path = os.path.join(build_directory, file_name + '.o')

    # Try to speed up build time
    if not force_rebuild:
        # Skip compilation if .cpp was not edited more recently than .o
        if not is_file_more_recent(cpp_file, output_path):
            return output_path
        # todo: check if hpp files were edited more recently than .o

    # Construct the include directories string
    includes_str = ' '.join(['-I' + include_dir for include_dir in include_dirs])

    # Compile the source file to a .o file
    command = f'g++ -c {cpp_file} -o {output_path} {includes_str}'
    subprocess.run(command, shell=True, check=True)
    print(f'{cpp_file} compiled to {output_path}.')

    return output_path

def compile_and_link(target, cpp_files, include_dirs, lib_names, lib_paths, force_rebuild=False):
    # Create a list to store the paths of compiled .o files
    object_files = []

    # Compile each .cpp file to a .o file
    for cpp_file in cpp_files:
        object_files.append(compile_cpp_to_o(cpp_file, include_dirs, "build", force_rebuild))

    # Determine if building a DLL or an executable based on the specified file name
    if target.endswith('.dll'):
        # Construct the link command for building a DLL
        object_files_str = ' '.join(object_files)
        lib_names_str = ' '.join([f'-l{lib_name}' for lib_name in lib_names])
        lib_paths_str = ' '.join([f'-L{lib_path}' for lib_path in lib_paths])
        output_path = os.path.join('bin', target)
        command = f'g++ -shared -o {output_path} {object_files_str} {lib_names_str} {lib_paths_str}'
        subprocess.run(command, shell=True, check=True)
        print(f'DLL built successfully as {output_path}')
    elif target.endswith('.exe'):
        # Construct the link command for building an executable
        object_files_str = ' '.join(object_files)
        lib_names_str = ' '.join([f'-l{lib_name}' for lib_name in lib_names])
        lib_paths_str = ' '.join([f'-L{lib_path}' for lib_path in lib_paths])
        output_path = os.path.join('bin', target)
        command = f'g++ -o {output_path} {object_files_str} {lib_names_str} {lib_paths_str}'
        subprocess.run(command, shell=True, check=True)
        print(f'Executable built successfully as {output_path}')
    else:
        print('Invalid file extension. Please specify a file name with either .dll or .exe extension.')

def make(force_rebuild=False):
    private.check_environment()

    config = private.read_config()

    config["include-paths"].append("include")

    cpp_files = find_cpp_files("src")
    if not cpp_files:
        sys.exit('No CPP files found.')

    compile_and_link(config["target"], cpp_files, config["include-paths"], config["lib-names"], config["lib-paths"], force_rebuild)

if __name__ == "__main__":
    if len(sys.argv) > 2:
        sys.exit("Too many arguments.")

    force_rebuild=False
    if len(sys.argv) == 2:
        if sys.argv[1] == "full":
            force_rebuild = True
        else:
            sys.exit("Invalid argument.")

    make(force_rebuild)