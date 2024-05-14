#!/bin/bash
# Clear old information
rm -r .pytest_cache htmlcov

# Run unit test
bash ci/run-test.sh