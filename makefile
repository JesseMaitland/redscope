#!/bin/bash

#############################################################
#              Commands for Python environment              #
#############################################################

init:
	if [[ -d ./venv ]]; then rm -rf venv; fi \
	&& python3.6 -m venv venv \
	&& . venv/bin/activate \
	&& pip install --upgrade pip setuptools wheel \
	&& pip install -r requirements.txt

dev_req:
	rm -f requirements.txt \
	&& . venv/bin/activate \
	&& pip freeze > requirements.txt

update:
	. venv/bin/activate \
	&& pip install --upgrade pip setuptools wheel


#############################################################
#              Commands for testing                         #
#############################################################


lint:
	. venv/bin/activate \
	&& python -m flake8 ./redscope ./tests

unit_test:
	. venv/bin/activate \
	&& python -m unittest discover -v tests/unit

qa:
	make unit_test
	make lint


#############################################################
#              Build and Distribution                       #
#############################################################

build:
	. venv/bin/activate \
	&& python setup.py sdist bdist_wheel

deploy:
  ifdef version
		./bin/release --version $(version)
  else
	  ./bin/release
  endif
