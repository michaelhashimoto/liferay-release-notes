#!/usr/bin/env python

import json
import requests

s = requests.Session()

label = "liferay-fixpack-de-10-7010"

# TODO Don't hardcode fix pack numbers
# Get all fix packs

result = s.get('https://issues.liferay.com/rest/api/2/search?jql=labels=%s' % (label))

full = result.json()

all_issues = {}

for t in full["issues"]:
    key = t["key"]

    issue = {}

    issue["type"] = t["fields"]["issuetype"]["name"]
    issue["summary"] = t["fields"]["summary"]

    components = []

    for c in t["fields"]["components"]:
        components.append(c["name"])

    issue["components"] = components

    all_issues[key] = issue

final_json = json.dumps(all_issues)
print final_json


# Filter for:
# LPS
# LPE
# Label

# Filter out:
# Private issues

# Data:
# Type, Key, Summary, Component

# Features:
# Component clickable links
# Drop down to show older realeases