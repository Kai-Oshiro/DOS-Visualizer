import sys

# Define args
def get_args():
    options = {"-f": True} # "True" requires an argument
    args = {"f": None} # "args" define default value

    # Get optional args
    for key in options.keys():
        if key in sys.argv:
            idx = sys.argv.index(key)
            if options[key]:
                value = sys.argv[idx+1]
                if value.startswith("-"):
                    raise ValueError(f"option {key} must have a value.")
                args[key[1:]] = value
                del sys.argv[idx:idx+2]
            else:
                args[key[1:]] = True
                del sys.argv[idx]

    # Get positional args
    for idx, arg in enumerate(sys.argv):
        args[idx] = arg

    # Return args
    return args
