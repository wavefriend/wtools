import sys # TODO make utils functions instead
import make

## Build src and main then run main with 'args'.
def run_main(args = []) -> None:
    make.make_main()

    # TODO
    pass

## Build src and test then run test with 'filter'.
def run_test(args = []) -> None:
    make.make_test()

    # TODO
    pass

## This is the behavior of wrun.
if __name__ == "__main__":
    target = sys.argv[0]
    args = sys.argv[1:]

    if target == "main":
        run_main(args)
    elif target == "test":
        run_test(args)
    else:
        raise Exception("Invalid run target " + target)