#!/bin/bash

poetry export -f requirements.txt --only main,prod --output ../requirements.txt