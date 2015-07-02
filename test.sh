#!/bin/sh

# script to run all your unit and functional tests

nosetests service/tests/unit/
nosetests service/tests/functional/