import sys
import subprocess
import private.private as private

def run(args=[]):
    private.check_environment()

    config = private.read_config()

    if config["type"] != "program" and config["type"] != "test":
        sys.exit("Only programs and tests can be run.")

    subprocess.run(["bin/" + config["target"]] + args)

if __name__ == "__main__":
    run(sys.argv[1:len(sys.argv)])