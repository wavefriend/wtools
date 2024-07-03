import os
import sys
import private.private as private
import wclean

def cleantest():
    private.check_environment()

    config = private.read_config()

    if config["type"] == "library":
        os.chdir("test")
        wclean.clean()
    elif config["type"] == "test":
        wclean.clean()
    else:
        sys.exit("Can only clean test in library or test environment.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        sys.exit("Too many arguments.")

    cleantest()