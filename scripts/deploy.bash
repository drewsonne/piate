#! /usr/bin/env bash

pip install wheel
python setup.py sdist bdist_wheel

twine upload dist/*

rm -r build dist piate.egg-info
