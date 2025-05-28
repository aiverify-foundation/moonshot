#!/bin/bash

# create venv for ci
python3 -m venv ci-venv
source ci-venv/bin/activate

pip install --upgrade pip > /dev/null

# install dependencies
pip install -r requirements.txt > /dev/null

# license check
echo "License check..."
pip install pip-licenses > /dev/null
pip-licenses --format markdown --output-file licenses-found.md > /dev/null
pip uninstall pip-licenses prettytable wcwidth -y > /dev/null

# dependency check
echo "Dependency check..."
pip install pip-audit > /dev/null
pip uninstall setuptools -y > /dev/null
set +e
pip-audit --format markdown --desc on -o pip-audit-report.md &> pip-audit-count.txt
exit_code=$?
pip install mdtree > /dev/null

if [ -f pip-audit-report.md ]; then
  echo "============ Vulnerabilities Found ============"
  cat pip-audit-report.md
  mdtree pip-audit-report.md > pip-audit-report.html
else
  touch pip-audit-report.html
fi

if [ -f licenses-found.md ]; then
  strongCopyleftLic=("GPL" "AGPL" "EUPL" "OSL")
  weakCopyleftLic=("LGPL" "MPL" "CCDL" "EPL" "CC-BY-SA" "CPL")

  echo "============ Strong Copyleft Licenses Found ============"
  head -n 2 licenses-found.md
  while IFS= read -r line; do
    # Skip text-unidecode with Artistic Licenses
    if [[ $line == *"text-unidecode"* && $line == *"Artistic License"* ]]; then
      continue
    fi
    for lic in "${strongCopyleftLic[@]}"; do
      if [[ $line == *"$lic"* ]]; then
        echo "$line"
        break
      fi
    done
  done < licenses-found.md

  echo "============ Weak Copyleft Licenses Found ============"
  head -n 2 licenses-found.md
  while IFS= read -r line; do
    # Special case for text-unidecode
    if [[ $line == *"text-unidecode"* && $line == *"Artistic License"* ]]; then
      echo "$line (Reclassified as weak copyleft)"
      continue
    fi
    for lic in "${weakCopyleftLic[@]}"; do
      if [[ $line == *"$lic"* ]]; then
        echo "$line"
        break
      fi
    done
  done < licenses-found.md
  mdtree licenses-found.md > license-report.html
else
  touch license-report.html
fi

deactivate
rm -rf ci-venv

set -e
if [ $exit_code -ne 0 ]; then
#  echo "pip-audit failed, exiting..."
  exit $exit_code
fi