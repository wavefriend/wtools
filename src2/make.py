import sys # TODO make utils functions instead

def make_src() -> None:
    # TODO
    pass

def make_main() -> None:
    make_src()

    # TODO
    pass

def make_test() -> None:
    make_src()

    # TODO
    pass

## This is the behavior of wmake.
if __name__ == "__main__":
    target = sys.argv[0]

    if target == "src":
        make_src()
    elif target == "main":
        make_main()
    elif target == "test":
        make_test()
    else:
        raise Exception("Invalid make target " + target)