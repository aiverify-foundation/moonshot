#!/bin/bash

# create venv for ci
python3 -m venv ci-venv
source ci-venv/bin/activate

# install dependencies
pip install -r requirements.txt

# license check
echo "Installing pip-licenses..."
pip install pip-licenses
pip-licenses --format markdown --output-file licenses-found.md
pip uninstall pip-licenses prettytable wcwidth -y

# dependency check
echo "Installing pip-audit..."
pip install pip-audit
pip uninstall setuptools -y
set +e
pip-audit --format markdown --desc on -o pip-audit-report.md &> pip-audit-count.txt
exit_code=$?
pip install mdtree

if [ -f pip-audit-report.md ]; then
  echo "Vulnerabilities Found"
  cat pip-audit-report.md
#  fc1=`cat pip-audit-report.md`
#  echo "$fc1"
  mdtree pip-audit-report.md > pip-audit-report.html
else
  touch pip-audit-report.html
fi

if [ -f licenses-found.md ]; then
  copyleftLic=("GPL" "LGPL" "MPL" "AGPL" "EUPL" "CCDL" "EPL" "CC-BY-SA" "OSL" "CPL")
  echo "Copyleft Licenses Found:"
  head -n 2 licenses-found.md
  while IFS= read -r line; do
    for lic in "${copyleftLic[@]}"; do
      if [[ $line == *"$lic"* ]]; then
        echo "$line"
        break
      fi
    done
  done < licenses-found.md
#  fc2=`cat licenses-found.md`
#  echo "$fc2"
  mdtree licenses-found.md > license-report.html
else
  touch license-report.html
fi

# Create badges
pip install anybadge
python3 ci/createBadges.py dependency
python3 ci/createBadges.py license

deactivate
#rm -rf ci-venv

set -e
if [ $exit_code -ne 0 ]; then
  echo "pip-audit failed, exiting..."
  exit $exit_code
fi
