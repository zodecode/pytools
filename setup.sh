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
  python3 -m build -nswx .
}
install(){
  # pip install ./dist/pytools-0.1.dev1+gc2.whl
  pip install "$1"
}
test(){
  python ./pytools/__init__.py -c date
}
[[ $1 == "-h" ]] && shift && usage "$@" && exit 0
[[ $1 == "create_env" ]] && shift && create_env "$@" && exit 0
[[ $1 == "upgrade" ]] && shift && upgrade "$@" && exit 0
[[ $1 == "build" ]] && shift && build "$@" && exit 0
[[ $1 == "install" ]] && shift && install "$@" && exit 0
[[ $1 == "test" ]] && shift && test "$@" && exit 0

echo -e "\nEND\n"
