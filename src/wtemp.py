import os
import re

# start from folder 'dir_path' and get all paths to files with 'with_ext' underneath it
# with_ext should not include '.'
def find_file_paths(dir_path, with_ext):
    assert(os.path.isdir(dir_path))

    file_paths = []

    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.' + with_ext):
                file_paths.append(os.path.join(root, file))

    return file_paths

# return the paths that are included in the given 'file_path' using #include statements
# only "" includes are included not <> includes
def extract_includes(file_path):
    assert(os.path.isfile(file_path))

    include_pattern = re.compile(r'^\s*#include\s*"([^"]+)"')

    includes = []

    try:
        with open(file_path, 'r') as file:
            for line in file:
                match = include_pattern.match(line)
                if match:
                    # we assume that all hpps are inside the include folder
                    # this is wrong both if hpps are put in src
                    # and wrong if they are includes from other libraries
                    # we can rule out #2 with an assert
                    # and we can require that #1 be true and maybe add a function
                    # that verifies that
                    includes.append('include\\' + match.group(1).replace('/', '\\'))

    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return sorted(set(includes))

def expand_includes(large_include_map, file_path):
    assert(os.path.isfile(file_path))

    includes = large_include_map[file_path]

    for include in large_include_map[file_path]:
        includes += expand_includes(large_include_map, include)

    return sorted(set(includes))

# this might have duplicates in the value lists
# lists are sorted and duplicates are removed
def create_large_include_map(hpp_file_paths, cpp_file_paths):
    large_include_map = {}

    for file_path in hpp_file_paths + cpp_file_paths:
        large_include_map[file_path] = extract_includes(file_path)

    return large_include_map

# only has cpps mapped to hpps
# lists are sorted and duplicates are removed
def create_small_include_map(large_include_map, cpp_file_paths):
    small_include_map = {}

    for cpp_file_path in cpp_file_paths:
        small_include_map[cpp_file_path] = expand_includes(large_include_map, cpp_file_path)

    return small_include_map


if __name__ == "__main__":

    hpp_file_paths = find_file_paths('include', 'hpp')
    cpp_file_paths = find_file_paths('src', 'cpp')

    large_include_map = create_large_include_map(hpp_file_paths, cpp_file_paths)
    small_include_map = create_small_include_map(large_include_map, cpp_file_paths)




