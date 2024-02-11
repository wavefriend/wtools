import sys
import subprocess
import private.private as private

def run():
    private.check_environment()

    config = private.read_config()

    if config["type"] != "program" and config["type"] != "test":
        sys.exit("Only programs and tests can be run.")

    subprocess.run(["bin/" + config["target"]])

if __name__ == "__main__":
    if len(sys.argv) > 1:
        sys.exit("Too many arguments.")

    run()