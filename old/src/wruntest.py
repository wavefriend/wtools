import os
import sys
import private.private as private
import wrun

def runtest(args=[]):
    private.check_environment()

    config = private.read_config()

    if config["type"] == "library":
        os.chdir("test")
        wrun.run(args)
    elif config["type"] == "test":
        wrun.run(args)
    else:
        sys.exit("Can only run test in library or test environment.")

if __name__ == "__main__":
    runtest(sys.argv[1:len(sys.argv)])