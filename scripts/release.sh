#!/bin/bash

source $(dirname $0)/common.sh

ghr $(version) $(dirname $0)/../dist
