def _main():
    """\
    Usage: pytools [options] [FILE ...]

    pytools - system admin tools
    See also https://github.com/zodecode/pytools

    FILE                      resource filename used in script function

    Options:

    -h, --help                show this message
    -c, --cmd                 command name to execute
    -o FILE, --output FILE    dump output to FILE (default: stdout)
    """
    import getopt
    import sys
    import textwrap

    usage = textwrap.dedent(_main.__doc__)
    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "h1o:s:F:A:f:",
            ["help", "output"],
        )
    except getopt.GetoptError as e:
        print(e)
        print(usage)
        sys.exit(2)
    outfile = "-"
    cmd = ""
    for opt, value in opts:
        if opt in ["-o", "--output"]:
            outfile = value
        elif opt in ["-c", "--cmd"]:
            cmd = value
        elif opt in ["-h", "--help"]:
            print(usage)
            sys.exit(0)
    if cmd:
        _run_command(cmd)


def _run_command(cmd):
    print("ls -la + ", cmd)


if __name__ == "__main__":
    _main()