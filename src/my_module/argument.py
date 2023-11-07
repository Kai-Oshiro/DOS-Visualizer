import sys

# Define arguments
def get_args():
    option_dict = {"-f": None} # {option_name: 'default value'}
    arg_dict = {} # {f: '/path/to/conf/file'}

    # Get optional arguments
    for key in option_dict.keys():
        if key in sys.argv:
            idx = sys.argv.index(key)
            value = sys.argv[idx+1] # Get next value of the key (option name)
            if value.startswith("-"):
                raise ValueError(f"{key} doesn't have a value.")
            arg_dict[key[1:]] = value # Remove "-" from option name by key[1:]
            del sys.argv[idx:idx+2]

    # Return args
    return arg_dict
