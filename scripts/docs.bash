#! /usr/bin/env bash

rm -rf docs
pdoc --html piate
mv html/piate/ docs/
rm -rf html