#!/bin/bash

# Note: this script must be run using source

# Default values
REPO="aiverify-foundation/moonshot"
OUTPUT_FILE=".codeql-alerts.json"

# Parse arguments
while [[ "$#" -gt 0 ]]; do
  case $1 in
      -r|--repo) REPO="$2"; shift ;;
      -o|--output) OUTPUT_FILE="$2"; shift ;;
      -h|--help)
          echo "Usage: $0 [-r|--repo <repository>] [-o|--output <output_file>]"
          return 0
          ;;
      *) echo "Unknown parameter passed: $1"; return 1 ;;
  esac
  shift
done

OUTPUT_MESSAGES=""

# Check if gh command is available
if ! command -v gh &> /dev/null
then
  OUTPUT_MESSAGES+="gh command could not be found. Please install GitHub CLI.\n"
  return 1
fi

# Fetch CodeQL alerts
gh api -X GET "repos/$REPO/code-scanning/alerts" > "$OUTPUT_FILE"
if [ $? -ne 0 ]; then
  OUTPUT_MESSAGES+="Failed to fetch CodeQL alerts.\n"
  return 1
fi

# Total alert count
alerts_count=$(jq '. | length' "$OUTPUT_FILE")
OUTPUT_MESSAGES+="Total CodeQL alerts: $alerts_count\n"

# Display alerts by severity if there are any alerts
if [ "$alerts_count" -gt 0 ]; then
  OUTPUT_MESSAGES+="Alerts by severity:\n"
  OUTPUT_MESSAGES+="$(jq -r '.[] | .rule.severity' "$OUTPUT_FILE" | sort | uniq -c)\n"
  rm "$OUTPUT_FILE"
  #echo -e "$OUTPUT_MESSAGES"
  echo "There are CodeQL alerts, please check Security>Code Scanning tab in the repository for more details."
  export CODEQL_SUMMARY="$OUTPUT_MESSAGES"
  return 2
else
  rm "$OUTPUT_FILE"
  echo -e "$OUTPUT_MESSAGES"
  export CODEQL_SUMMARY="$OUTPUT_MESSAGES"
  return 0
fi
