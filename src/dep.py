## This file contains functions and classes for building the
## dependency graph of a C++ project.

import re
import utils

# TODO need to handle included cpps
# TODO stop the dep search when you find a time before a certain threshold
#      instead of just finding the most recent time

class DepGraph:

    src_dir_path: str

    ## We search for hpp file locations in the order of the entries in this list.
    include_dir_paths: list

    cpp_paths: list

    ## Maps hpps and cpps to their includes.
    up: dict = {}

    ## Maps hpps to the hpps and cpps that include them.
    down: dict = {}

    def __init__(self, src_dir_path: str, include_dir_paths: list) -> None:
        self.src_dir_path = src_dir_path
        self.include_dir_paths = include_dir_paths

        # Get cpp paths in a usable format
        rel_cpp_paths = utils.get_files_deep(src_dir_path, [".cpp"])
        self.cpp_paths = utils.add_paths_list(src_dir_path, rel_cpp_paths)

        # Add cpp paths
        for cpp_path in self.cpp_paths:
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

    ## Returns the most recent time 'cpp_path' or one of the hpp paths it depends on
    ## were modified.
    def _get_cpp_last_modified_time(self, cpp_path: str) -> float:
        last_modified_time = utils.get_file_last_modified_time(cpp_path)

        for included_hpp_path in self.up[cpp_path]:
            time = self._get_hpp_last_modified_time(included_hpp_path)

            if time > last_modified_time:
                last_modified_time = time

        return last_modified_time

    ## Returns the most recent time 'hpp_path' or one of the hpp paths it depends on
    ## were modified.
    def _get_hpp_last_modified_time(self, hpp_path: str) -> float:
        last_modified_time = utils.get_file_last_modified_time(hpp_path)

        for included_hpp_path in self.up[hpp_path]:
            time = self._get_hpp_last_modified_time(included_hpp_path)

            if time > last_modified_time:
                last_modified_time = time

        return last_modified_time

    def get_cpp_paths(self) -> list:
        return self.cpp_paths

    ## Returns a map of cpp paths to the most recent times they or one of the hpp paths
    ## they depend on were modified.
    def get_cpp_last_modified_times(self) -> dict:
        last_modified_times = {}

        for cpp_path in self.cpp_paths:
            last_modified_times[cpp_path] = self._get_cpp_last_modified_time(cpp_path)

        return last_modified_times

    def __str__(self) -> str:
        result = ""

        result += "up:\n"
        for key, values in self.up.items():
            result += str(key) + ": " + str(values) + "\n"

        result += "\ndown:\n"
        for key, values in self.down.items():
            result += str(key) + ": " + str(values) + "\n"

        return result
