import sys
import filetrack


if __name__ == '__main__':
    args = sys.argv[2:]
    command_name = sys.argv[1]
    command = getattr(filetrack, command_name)
    sys.exit(command(*args))
