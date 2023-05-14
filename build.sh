#!/usr/bin/env bash
# Newer setuptools is needed for proper support of pyproject.toml
upgrade(){
  python3 -m pip install setuptools --upgrade
  python3 -m pip install wheel --upgrade
  python3 -m pip install build setuptools_scm
#  python3 -m pip install pytest numpy pandas
}
build(){
  python3 -m build -nswx .
}
#upgrade "$@"
# This step builds your wheels.
build "$@"
