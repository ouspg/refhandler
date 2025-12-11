#! /usr/bin/env bash
py -3.12 -m venv venv
source venv/bin/activate
pip install -r backend/requirements-dev.txt