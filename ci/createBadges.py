import json
import os
import re
import sys

import anybadge


def create_badges() -> None:
    # Check if an argument is provided
    if len(sys.argv) > 1:
        badgeToCreate = sys.argv[1]
    else:
        print("No badgeToCreate provided")
        sys.exit()

    covBadgeSvg = "cov-badge.svg"
    testBadgeSvg = "test-badge.svg"
    lintBadgeSvg = "lint-badge.svg"
    depBadgeSvg = "dep-badge.svg"
    licBadgeSvg = "lic-badge.svg"

    # Create coverage badge
    if badgeToCreate == "coverage":
        with open("coverage.json") as jsonFile:
            covJson = json.load(jsonFile)
        covPct = covJson["totals"]["percent_covered"]
        if covPct < 20:
            color = "red"
        elif covPct < 70:
            color = "orange_2"
        else:
            color = "green"
        badge = anybadge.Badge(
            "coverage", str(int(round(covPct))) + "%", default_color=color
        )
        if os.path.exists(covBadgeSvg):
            os.remove(covBadgeSvg)
        badge.write_badge(covBadgeSvg)

    # Create test result badge
    if badgeToCreate == "test":
        with open("test-report.json") as jsonFile:
            testJson = json.load(jsonFile)
        testSummary = testJson["report"]["summary"]
        testPassed = 0 if "passed" not in testSummary else testSummary["passed"]
        testFailed = 0 if "failed" not in testSummary else testSummary["failed"]
        print(str(testPassed) + " " + str(testFailed))
        color = "green" if (testPassed != 0 and testFailed == 0) else "red"
        badge = anybadge.Badge(
            "tests",
            str(testPassed) + " passed, " + str(testFailed) + " failed",
            default_color=color,
        )
        if os.path.exists(testBadgeSvg):
            os.remove(testBadgeSvg)
        badge.write_badge(testBadgeSvg)

    # Create lint (flake8) badge
    if badgeToCreate == "lint":
        with open("flake8-report.txt", "r") as file:
            last_line = None
            for line in file:
                last_line = line.strip()
        color = "green" if (last_line == "0") else "red"
        badge = anybadge.Badge("lint", str(last_line) + " errors", default_color=color)
        if os.path.exists(lintBadgeSvg):
            os.remove(lintBadgeSvg)
        badge.write_badge(lintBadgeSvg)

    # Create dependency check badge
    if badgeToCreate == "dependency":
        numVul = "0"
        with open("pip-audit-count.txt", "r") as file:
            content = file.read()
            if content.find("No known vulnerabilities found") != -1:
                numVul = "0"
            else:
                pattern = r"Found (\d+) known vulnerabilit"
                match = re.search(pattern, content)
                if match:
                    numVul = match.group(1)
                else:
                    numVul = None
        if numVul is not None:
            color = "green" if (numVul == "0") else "red"
            msg = numVul + " vulnerabilities"
        else:
            color = "red"
            msg = "error"
        badge = anybadge.Badge("dependencies", msg, default_color=color)
        if os.path.exists(depBadgeSvg):
            os.remove(depBadgeSvg)
        badge.write_badge(depBadgeSvg)

    # Create license check badge
    if badgeToCreate == "license":
        with open("licenses-found.md", "r") as file:
            content = file.read()
            copyleftLic = [
                "GPL",
                "LGPL",
                "MPL",
                "AGPL",
                "EUPL",
                "CCDL",
                "EPL",
                "CC-BY-SA",
                "OSL",
                "CPL",
            ]
            licFound = []
            for lic in copyleftLic:
                if lic in content:
                    licFound.append(lic)

        numCopyleftLic = len(licFound)
        color = "green" if (numCopyleftLic == 0) else "red"
        badge = anybadge.Badge(
            "licenses", str(numCopyleftLic) + " copyleft", default_color=color
        )
        if os.path.exists(licBadgeSvg):
            os.remove(licBadgeSvg)
        badge.write_badge(licBadgeSvg)


if __name__ == "__main__":  # pragma: no cover
    create_badges()
