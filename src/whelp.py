import sys

# todo: discuss wconfig.json and environment folder layout
# todo: mention that winits will update environment if its out of whack
# todo: mention what conditions underwhich wmake will rebuild everything

def help():
    print('whelp')
    print('\tSee this help text.')
    print('\n')
    print('winitprogram <name>')
    print('\tCreate a new environment for building an executable called <name>.exe')
    print('\n')
    print('winitlibrary <name>')
    print('\tCreate a new environment for building a dynamic library called <name>.dll')
    print('\n')
    print('wmake')
    print('\tBuild executable or library.')
    print('\n')
    print('wrun')
    print('\tRun executable if there is one.')
    print('\n')
    print('wmaketest')
    print('\tBuild test.')
    print('\n')
    print('wruntest')
    print('\tRun test.')
    print('\n')

if __name__ == "__main__":
    if len(sys.argv) > 1:
        sys.exit("Too many arguments.")

    help()