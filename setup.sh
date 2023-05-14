#!/usr/bin/env bash
usage(){
cat <<EOF
${B}
${Y}   setup      ${S}
${Y}   --------   ${S}
${L}   create_env ${S} (1) create venv and activate
${L}   upgrade    ${S} (2) upgrade venv and install dependencies
${L}   build      ${S} (3) build
${L}   install    ${S} (4) install
${L}   test       ${S} (5) test script wheel
EOF
}
create_env(){
  python3 -m venv venv
  source venv/bin/activate
  pip install setuptools -U
  pip install setuptools-scm
}
upgrade(){
  python3 -m pip install setuptools --upgrade
  python3 -m pip install wheel --upgrade
  python3 -m pip install build setuptools_scm
}
build(){
  # -n or --no-clean: Skips the clean-up step, which means previously built files are not removed before building the package.
  # -s or --sdist: Builds a source distribution (a .tar.gz or .zip file containing the project's source code).
  # -w or --wheel: Builds a wheel distribution (a .whl file containing pre-compiled binary modules).
  # -x or --no-isolation: Disables the isolation of builds by using the system-installed versions of build dependencies if available.
  # .: Specifies the current directory as the location of the project to be built.
  # python3 -m build -nswx .
  python3 -m build -wx .
  ls -lh dist/
}
install(){
  # pip install ./dist/pytools-0.1.dev1+gc2.whl
  [[ $# -lt 1 ]] && echo "missing .whl file" && exit 1
  pip install "$1"
}
test(){
  python ./pytools/__init__.py version
}
[[ $1 == "-h" ]] && shift && usage "$@" && exit 0
[[ $1 == "create_env" ]] && shift && create_env "$@" && exit 0
[[ $1 == "upgrade" ]] && shift && upgrade "$@" && exit 0
[[ $1 == "build" ]] && shift && build "$@" && exit 0
[[ $1 == "install" ]] && shift && install "$@" && exit 0
[[ $1 == "test" ]] && shift && test "$@" && exit 0

echo -e "\nEND\n"
