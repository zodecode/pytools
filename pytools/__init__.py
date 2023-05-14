import sys
import os
# Get the absolute path of the current directory
current_dir = os.path.abspath(os.path.dirname(__file__))
# Append the current directory to the Python path
sys.path.append(current_dir)
from pytools import version
VERSION = version.__version__
def _main():
    """\
    Usage: pytools [options] [FILE ...]

    pytools - system admin tools
    See also https://github.com/zodecode/pytools

    FILE                      resource filename used in script function

    Options:

    -h, --help                show this message
    -c, --cmd                 command name to execute
    -v, --version             show pytools version
    -o FILE, --output FILE    dump output to FILE (default: stdout)
    """
    import getopt
    import sys
    import textwrap

    usage = textwrap.dedent(_main.__doc__)
    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "h1oc:v:s:f:",
            ["help", "output", "cmd", "version"],
        )
    except getopt.GetoptError as e:
        print(e)
        print(usage)
        sys.exit(2)
    outfile = "-"
    cmd = None
    version = "0"
    for opt, value in opts:
        if opt in ["-o", "--output"]:
            outfile = value
        elif opt in ["-c", "--cmd"]:
            cmd = value
        elif opt in ["-v", "--version"]:
            cmd = value

            print(f"version:", VERSION)
            sys.exit(0)
        elif opt in ["-h", "--help"]:
            print(usage)
            sys.exit(0)
    if cmd:
        _run_command(cmd)


def _run_command(cmd):
    print("cmdrun:", cmd)
    if cmd == "date":
        from datetime import datetime
        print("Now: ", datetime.now())


if __name__ == "__main__":
    _main()