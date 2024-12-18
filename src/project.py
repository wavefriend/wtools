import utils

# TODO verify all directories in wconfig are relative,
#      independent, and within the project

class SubProject:

    def __init__(self) -> None:
        pass

class Project:

    config = {}
    extern = {}

    def __init__(self, project_dir_path = "") -> None:
        config_path = utils.add_paths(project_dir_path, "wconfig.json")
        extern_path = utils.add_paths(project_dir_path, "wextern.json")

        self.config = utils.read_json_dict(config_path)
        self.extern = utils.read_json_dict(extern_path)