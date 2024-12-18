import os
import sys
import json

def check_type(type):
    if not type in ["program", "library", "test"]:
        sys.exit("Invalid environment type.")

def get_ext(type):
    check_type(type)
    if type == "program":
        return ".exe"
    elif type == "library":
        return ".dll"
    elif type == "test":
        return ".exe"

def init_config(type, name, include_paths=[], lib_names=[], lib_paths=[]):
    check_type(type)

    config = {}

    if os.path.exists("wconfig.json"):
        with open("wconfig.json", 'r') as file:
            config = json.load(file)

    if not "type" in config:
        config["type"] = type
    elif config["type"] != type:
        sys.exit("This folder already contains a " + config["type"] + " environment.")

    if not "name" in config:
        config["name"] = name
    elif config["name"] != name:
        sys.exit("The existing environment has a different name.")

    if not "target" in config:
        config["target"] = name + get_ext(type)
    elif config["target"] != name + get_ext(type):
        sys.exit("The existing environment has a different target.")

    if not "c++" in config:
        config["c++"] = 20

    if not "include-paths" in config:
        config["include-paths"] = include_paths
    else:
        for include_path in include_paths:
            if not include_path in config["include-paths"]:
                config["include-paths"].append(include_path)

    if not "lib-names" in config:
        config["lib-names"] = lib_names
    else:
        for lib_name in lib_names:
            if not lib_name in config["lib-names"]:
                config["lib-names"].append(lib_name)

    if not "lib-paths" in config:
        config["lib-paths"] = lib_paths
    else:
        for lib_path in lib_paths:
            if not lib_path in config["lib-paths"]:
                config["lib-paths"].append(lib_path)

    if len(config) > 7:
        sys.exit("Config has extra entries.")

    with open("wconfig.json", 'w') as file:
        json.dump(config, file, indent=4)
        print("wconfig.json for " + name + " created.")

def init_layout(type, name):
    check_type(type)

    for dir_name in ["bin", "build", "include", "src"]:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            print(dir_name + " directory created.")

    if type == "library":
        if not os.path.exists("test"):
            os.makedirs("test")
        os.chdir("test")
        init_environment("test", "test", ["../include"], [name], ["../bin"])

def init_environment(type, name, include_paths=[], lib_names=[], lib_paths=[]):
    init_config(type, name, include_paths, lib_names, lib_paths)
    init_layout(type, name)

def check_config():
    if not os.path.exists("wconfig.json"):
        sys.exit("No config file could be found.")

    config = {}

    with open("wconfig.json", 'r') as file:
        config = json.load(file)

    for key in ["type", "name", "target", "c++", "include-paths", "lib-names", "lib-paths"]:
        if not key in config:
            sys.exit("Config is missing a " + key)

    if len(config) > 7:
        sys.exit("Config has extra entries.")

    check_type(config["type"])

    if not config["target"].startswith(config["name"]):
        sys.exit("Target name does not match environment name.")

    if not config["target"].endswith(get_ext(config["type"])):
        sys.exit("Target extension does not match environment type.")

def check_layout():
    for dir_name in ["bin", "build", "include", "src"]:
        if not os.path.exists(dir_name):
            sys.exit(dir_name + " directory is missing.")

    config = read_config()

    if config["type"] == "library":
        if not os.path.exists("test"):
            sys.exit("test directory is missing.")
        os.chdir("test")
        check_layout()
        os.chdir("../")

def check_environment():
    check_config()
    check_layout()

def read_config():
    check_config()
    with open("wconfig.json", 'r') as file:
        return json.load(file)