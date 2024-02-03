import sys
import private.private as private

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Too few arguments.")
    elif len(sys.argv) > 2:
        sys.exit("Too many arguments.")

    private.init_environment("library", sys.argv[1])