import os
import sys
import private.private as private
import wmake

def maketest():
    private.check_environment()

    config = private.read_config()

    if config["type"] == "library":
        os.chdir("test")
        wmake.make()
    elif config["type"] == "test":
        wmake.make()
    else:
        sys.exit("Can only make test in library or test environment.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        sys.exit("Too many arguments.")

    maketest()