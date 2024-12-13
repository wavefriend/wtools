## This file contains functions and classes for building the
## dependency graph of a C++ project.

import re
import utils

## Matches valid include statements that use quotes.
INCLUDE_PATTERN = r'#include *"([^"]*)"'

class DepGraph:
    pass

# TODO how do we handle the fact that include dir is not the same
#      as the project folder

## Build a dependency graph for the .hpp and .cpp files under
## 'dir_path' and its subfolders.
def build_dep_graph(dir_path: str) -> DepGraph:
    hpp_file_paths = utils.get_files_deep(dir_path, [".hpp"])
    cpp_file_paths = utils.get_files_deep(dir_path, [".cpp"])

    # Make paths usable from the current directory.
    fhfps = utils.add_paths_list(dir_path, hpp_file_paths)
    fcfps = utils.add_paths_list(dir_path, cpp_file_paths)

    hpp_to_hpps: dict = {}
    cpp_to_hpps: dict = {}

    for fhfp in fhfps:
        text = utils.read_text(fhfp)
        hpp_to_hpps[fhfp] = re.findall(INCLUDE_PATTERN, text)

    for fcfp in fcfps:
        text = utils.read_text(fcfp)
        cpp_to_hpps[fcfp] = re.findall(INCLUDE_PATTERN, text)