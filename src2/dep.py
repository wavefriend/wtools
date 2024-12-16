## This file contains functions and classes for building the
## dependency graph of a C++ project.

import re
import utils

# TODO need to handle included cpps

class DepGraph:

    src_dir_path: str

    ## We search for hpp file locations in the order of the entries in this list.
    include_dir_paths: list

    ## Maps hpps and cpps to their includes.
    up: dict = {}

    ## Maps hpps to the hpps and cpps that include them.
    down: dict = {}

    def __init__(self, src_dir_path: str, include_dir_paths: list) -> None:
        self.src_dir_path = src_dir_path
        self.include_dir_paths = include_dir_paths

        # Get cpp paths in a usable format
        rel_cpp_paths = utils.get_files_deep(src_dir_path, [".cpp"])
        cpp_paths = utils.add_paths_list(src_dir_path, rel_cpp_paths)

        # Add cpp paths
        for cpp_path in cpp_paths:
            self._add_cpp(cpp_path)

    def _add_cpp(self, cpp_path: str) -> None:
        included_hpp_paths = self._get_included_hpp_paths(cpp_path)

        self.up[cpp_path] = included_hpp_paths

        for included_hpp_path in included_hpp_paths:
            self._add_hpp(included_hpp_path)

    def _add_hpp(self, hpp_path: str) -> None:
        included_hpp_paths = self._get_included_hpp_paths(hpp_path)

        self.up[hpp_path] = included_hpp_paths

        for included_hpp_path in included_hpp_paths:
            self._add_hpp(included_hpp_path)

    ## Look at 'file_path' and find all paths referenced in #include statements.
    ## The actual real paths corresponding to the shortened paths written in the
    ## #include statements are what are returned.
    def _get_included_hpp_paths(self, file_path: str) -> list:
        text = utils.read_text(file_path)

        # Matches valid include statements that use quotes.
        INCLUDE_PATTERN = r'#include *"([^"]*)"'

        rel_hpp_paths = utils.fix_path_list(re.findall(INCLUDE_PATTERN, text))

        hpp_paths = []

        for rel_hpp_path in rel_hpp_paths:
            found_match = False

            for include_dir_path in self.include_dir_paths:
                hpp_path = utils.add_paths(include_dir_path, rel_hpp_path)

                if utils.path_exists(hpp_path):
                    hpp_paths.append(hpp_path)
                    found_match = True
                    break

            if not found_match:
                raise Exception("Could not find the location of " + rel_hpp_path)

        return hpp_paths

    ## Returns a map of cpp paths to the last times they or one of the hpp paths
    ## they depend on were modified.
    def get_cpp_last_modified_times() -> dict:
        return {}

    def __str__(self) -> str:
        result = ""

        result += "up:\n"
        for key, values in self.up.items():
            result += str(key) + ": " + str(values) + "\n"

        result += "\ndown:\n"
        for key, values in self.down.items():
            result += str(key) + ": " + str(values) + "\n"

        return result
