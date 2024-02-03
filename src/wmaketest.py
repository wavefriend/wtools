import os
import sys
import private.private as private
import wmake

def maketest(force_rebuild=False):
    private.check_environment()

    config = private.read_config()

    if config["type"] == "library":
        os.chdir("test")
        wmake.make(force_rebuild)
    elif config["type"] == "test":
        wmake.make(force_rebuild)
    else:
        sys.exit("Can only make test in library or test environment.")

if __name__ == "__main__":
    if len(sys.argv) > 2:
        sys.exit("Too many arguments.")

    force_rebuild=False
    if len(sys.argv) == 2:
        if sys.argv[1] == "full":
            force_rebuild = True
        else:
            sys.exit("Invalid argument.")

    maketest(force_rebuild)