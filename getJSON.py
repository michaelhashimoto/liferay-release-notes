#!/usr/bin/env python

import json
import requests
import collections

s = requests.Session()

available = True
version = 1

final = {}

while available:
    result = s.get('https://issues.liferay.com/rest/api/2/search?jql=labels=liferay-fixpack-de-%s-7010' % (str(version)))

    result_json = result.json()

    if result_json["total"] == 0:
        if version != 4:
            available = False

    if available:
        all_issues = {}

        components = collections.defaultdict(list)

        for t in result_json["issues"]:
            key = t["key"]

            issue = {}
            details = {}

            details["type"] = t["fields"]["issuetype"]["name"]
            details["summary"] = t["fields"]["summary"]
            details["url"] = "https://issues.liferay.com/browse/%s" % (key)

            issue[key] = details

            for c in t["fields"]["components"]:
                name = c["name"]

                components[name].append(issue)

        final['liferay-fixpack-de-%s-7010' % (str(version))] = components

    version += 1

final_json = json.dumps(final)
print final_json