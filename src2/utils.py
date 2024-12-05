import os

## Return paths to all files directly under 'dir_path'.
## Returned paths are relative to 'dir_path'.
def files_in_dir(dir_path):
    item_paths = os.listdir(dir_path)

    file_paths = []

    for item_path in item_paths:
        if os.path.isfile(os.path.join(dir_path, item_path)):
            file_paths.append(item_path)

    return file_paths

## Return paths to all files under 'dir_path' and its subdirectories.
## Returned paths are relative to 'dir_path'.
def files_in_dir_and_subdirs(dir_path):
    file_paths = []

    for root, sub_dir_paths, sub_dir_file_paths in os.walk(dir_path):
        for sub_dir_file_path in sub_dir_file_paths:
            file_paths.append(os.path.relpath(os.path.join(root, sub_dir_file_path), dir_path))

    return file_paths

## Return paths to all directories directly under 'dir_path'.
## Returned paths are relative to 'dir_path'.
def dirs_in_dir(dir_path):
    item_paths = os.listdir(dir_path)

    dir_paths = []

    for item_path in item_paths:
        if os.path.isdir(os.path.join(dir_path, item_path)):
            dir_paths.append(item_path)

    return dir_paths

## Return paths to all directories under 'dir_path' and its subdirectories.
## Returned paths are relative to 'dir_path'.
def dirs_in_dir_and_subdirs(dir_path):
    dir_paths = []

    for root, sub_dir_paths, sub_dir_file_paths in os.walk(dir_path):
        for sub_dir_path in sub_dir_paths:
            dir_paths.append(os.path.relpath(os.path.join(root, sub_dir_path), dir_path))

    return dir_paths