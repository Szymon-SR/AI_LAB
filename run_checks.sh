#!/bin/bash

poetry run black labs
poetry run pylama labs --verbose
isort labs