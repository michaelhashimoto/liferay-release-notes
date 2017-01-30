#!/usr/bin/env python

import collections
import json
import operator

try:
    import urllib.request as urlrequest
except ImportError:
    import urllib as urlrequest

available = True
version = 1

final = {}

while available:
    url = 'https://issues.liferay.com/rest/api/2/search?jql=labels=liferay-fixpack-de-%s-7010' % (version)
    result = urlrequest.urlopen(url)
    result_json = json.loads(result.read())

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

        components = sorted(components.items(), key=operator.itemgetter(0))
        components = collections.OrderedDict(components)
        final[version] = components

    version += 1

final = sorted(final.items(), key=operator.itemgetter(0), reverse=True)
final = collections.OrderedDict(final)
final_json = json.dumps(final)

with open('output.json', 'w') as outfile:
    json.dump(final, outfile)