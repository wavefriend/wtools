## This file contains functions for basic file and directory
## operations.

import json
import os

## Return whether there is a file or directory at 'path'.
def path_exists(path: str) -> str:
    return os.path.exists(path)

## Return 'path' but with the appropriate / or \ for the current platform.
def fix_path(path: str) -> str:
    # TODO consider OS other than Windows

    return path.replace("/", "\\")

## Return each path in 'paths' but with the appropriate / or \ for the current platform.
def fix_path_list(paths: list) -> list:
    # TODO consider OS other than Windows

    fixed_paths = []
    for path in paths:
        fixed_paths.append(fix_path(path))

    return fixed_paths

## Join 'root_path' and 'sub_path'.
def add_paths(root_path: str, sub_path: str) -> str:
    return os.path.join(root_path, sub_path)

## Join 'root_path' with each path in 'sub_paths'.
def add_paths_list(root_path: str, sub_paths: list) -> list:
    new_paths = []

    for sub_path in sub_paths:
        new_paths.append(add_paths(root_path, sub_path))

    return new_paths

## Subtract 'root_path' from 'full_path'.
def subtract_paths(full_path: str, root_path: str) -> str:
    return os.path.relpath(full_path, root_path)

## Subtract 'root_path' from each path in 'full_paths'.
def subtract_paths_list(full_paths: list, root_path: str) -> list:
    new_paths = []

    for full_path in full_paths:
        new_paths.append(subtract_paths(full_path, root_path))

    return new_paths

## Returns the extension of 'file_path' with the dot.
def get_file_extension(file_path: str) -> str:
    return os.path.splitext(file_path)[1]

## Return the last time 'file_path' was modified.
def get_file_last_modified_time(file_path: str) -> str:
    return os.path.getmtime(file_path)

## Return paths to all files directly under 'dir_path'.
## Returned paths are relative to 'dir_path'.
## If 'include_exts' is non-empty, only include files with the extensions in 'include_exts'.
## Extensions must be listed as strings with the dot.
def get_files(dir_path: str, include_exts: list = []) -> list:
    item_paths = os.listdir(dir_path)

    file_paths = []

    for item_path in item_paths:
        if os.path.isfile(add_paths(dir_path, item_path)):
            if len(include_exts) == 0 or get_file_extension(item_path) in include_exts:
                file_paths.append(item_path)

    return file_paths

## Return paths to all files under 'dir_path' and its subdirectories.
## Returned paths are relative to 'dir_path'.
## If 'include_exts' is non-empty, only include files with the extensions in 'include_exts'.
## Extensions must be listed as strings with the dot.
def get_files_deep(dir_path: str, include_exts: list = []) -> list:
    file_paths = []

    for root, sub_dir_paths, sub_dir_file_paths in os.walk(dir_path):
        for sub_dir_file_path in sub_dir_file_paths:
            if len(include_exts) == 0 or get_file_extension(sub_dir_file_path) in include_exts:
                file_paths.append(subtract_paths(add_paths(root, sub_dir_file_path), dir_path))

    return file_paths

## Return paths to all directories directly under 'dir_path'.
## Returned paths are relative to 'dir_path'.
def get_dirs(dir_path: str) -> list:
    item_paths = os.listdir(dir_path)

    dir_paths = []

    for item_path in item_paths:
        if os.path.isdir(add_paths(dir_path, item_path)):
            dir_paths.append(item_path)

    return dir_paths

## Return paths to all directories under 'dir_path' and its subdirectories.
## Returned paths are relative to 'dir_path'.
def get_dirs_deep(dir_path: str) -> list:
    dir_paths = []

    for root, sub_dir_paths, sub_dir_file_paths in os.walk(dir_path):
        for sub_dir_path in sub_dir_paths:
            dir_paths.append(subtract_paths(add_paths(root, sub_dir_path), dir_path))

    return dir_paths

## Return the text in 'text_file_path'.
def read_text(text_file_path: str) -> str:
    with open(text_file_path, 'r') as file:
        return file.read()

    raise Exception("Text not found.")

## Write the text to 'text_file_path'.
## Creates file if it doesn't exist.
## Overwrites existing file if it does exist.
def write_text(text_file_path: str, text: str) -> None:
    with open(text_file_path, 'w') as file:
        file.write(text)

## Return the list stored at 'json_file_path'.
## Throws if 'json_file_path' does not contain a list.
def read_json_list(json_file_path: str) -> list:
    with open(json_file_path, 'r') as file:
        data = json.load(file)

        if type(data) == list:
            return data

    raise Exception("Json list not found.")

## Write the list to 'json_file_path'.
## Creates file if it doesn't exist.
## Overwrites existing file if it does exist.
def write_json_list(json_file_path: str, list: list) -> None:
    with open(json_file_path, 'w') as file:
        json.dump(list, file)

## Return the dictionary stored at 'json_file_path'.
## Throws if 'json_file_path' does not contain a dictionary.
def read_json_dict(json_file_path: str) -> dict:
    with open(json_file_path, 'r') as file:
        data = json.load(file)

        if type(data) == dict:
            return data

    raise Exception("Json dictionary not found.")

## Write the dictionary to 'json_file_path'.
## Creates file if it doesn't exist.
## Overwrites existing file if it does exist.
def write_json_dict(json_file_path: str, dict: dict) -> None:
    with open(json_file_path, 'w') as file:
        json.dump(dict, file)