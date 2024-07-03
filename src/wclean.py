import os
import sys
import shutil
import private.private as private

def clean():
    private.check_environment()

    shutil.rmtree("bin")
    os.makedirs("bin")

    print("Deleted all files in bin.")

    shutil.rmtree("build")
    os.makedirs("build")

    print("Deleted all files in build.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        sys.exit("Too many arguments.")

    clean()