#!/bin/bash

poetry run black reversi_minimax
poetry run pylama reversi_minimax
isort reversi_minimax