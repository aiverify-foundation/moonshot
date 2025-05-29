#!/bin/bash

# Function to read coverage data
read_coverage() {
  covPct=$(jq '.totals.percent_covered' coverage.json)
  covPctRounded=$(printf "%.0f" "$covPct")
  message="Coverage percentage: $covPctRounded"
  echo "$message"
  export COVERAGE_SUMMARY="$message"
  if (( covPctRounded < 70 )); then
    return 1
  else
    return 0
  fi
}

# Function to read test data
read_test() {
  testJson=$(jq '.report.summary' test-report.json)
  testPassed=$(echo "$testJson" | jq '.passed // 0')
  testFailed=$(echo "$testJson" | jq '.failed // 0')
  message="Unit tests passed: $testPassed, failed: $testFailed"
  echo "$message"
  export UNITTEST_SUMMARY="$message"
  if [ "$testFailed" -ne 0 ]; then
    return 1
  else
    return 0
  fi
}

# Function to read lint data
read_lint() {
  last_line=$(tail -n 1 flake8-report.txt)
  message="Lint errors: $last_line"
  echo "$message"
  export LINT_SUMMARY="$message"
  if [ "$last_line" -ne 0 ]; then
    return 1
  else
    return 0
  fi
}

# Function to read dependency data
read_dependency() {
  content=$(<pip-audit-count.txt)
  if [[ $content == *"No known vulnerabilities found"* ]]; then
    numVul=0
  else
    numVul=$(grep -oP 'Found \K\d+' pip-audit-count.txt)
  fi
  message="Dependency vulnerabilities found: $numVul"
  echo "$message"
  export DEPENDENCY_SUMMARY="$message"
  if [ "$numVul" -ne 0 ]; then
    return 1
  else
    return 0
  fi
}

# Function to read license data
read_license() {
  strongCopyleftLic=("GPL" "AGPL" "EUPL" "OSL" "CPL")
  weakCopyleftLic=("LGPL" "MPL" "CCDL" "EPL" "CC-BY-SA")
  numStrongCopyleftLic=0
  numWeakCopyleftLic=0

  if [ -f licenses-found.md ]; then
    while IFS= read -r line; do
      # Check for strong copyleft licenses
      for lic in "${strongCopyleftLic[@]}"; do
        if [[ $line == *"$lic"* ]]; then
          ((numStrongCopyleftLic++))
          break
        fi
      done

      # Check for weak copyleft licenses
      for lic in "${weakCopyleftLic[@]}"; do
        if [[ $line == *"$lic"* ]]; then
          ((numWeakCopyleftLic++))
          break
        fi
      done
    done < licenses-found.md
  fi

  message="Strong copyleft licenses found: $numStrongCopyleftLic, Weak copyleft licenses found: $numWeakCopyleftLic"
  export LICENSE_SUMMARY="$message"
  echo "$message"

  # Return 1 if strong copyleft licenses are found, otherwise return 0
  if [ "$numStrongCopyleftLic" -ne 0 ]; then
    return 1
  else
    return 0
  fi
}

# Main function to determine which summary to generate
gen_summary() {
  if [[ $# -eq 0 ]]; then
    echo "No summaryToGen provided"
    exit 1
  fi

  summaryToGen=$1

  case $summaryToGen in
    "coverage")
      read_coverage
      ;;
    "test")
      read_test
      ;;
    "lint")
      read_lint
      ;;
    "dependency")
      read_dependency
      ;;
    "license")
      read_license
      ;;
    *)
      echo "Unknown summary type: $summaryToGen"
      exit 1
      ;;
  esac
}

# Execute the main function
gen_summary "$@"