#!/usr/bin/env python

import collections
import json
import operator
import os
import re
import shutil

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

                base_name = re.sub(' >(.*)', '', name)

                if not any(entry == issue for entry in components[base_name]):
                    components[base_name].append(issue)

        components = sorted(components.items(), key=operator.itemgetter(0))
        components = collections.OrderedDict(components)
        final[version] = components

    version += 1

final = sorted(final.items(), key=operator.itemgetter(0), reverse=True)
final = collections.OrderedDict(final)
final_json = json.dumps(final)

old = open('js/main.js', 'r')
old.readline()

new = open('js/main1.js', 'w')
new.write("var data = %s\n" % (final_json))

shutil.copyfileobj(old, new)

old.close()
new.close()

os.remove('js/main.js')
shutil.move('js/main1.js', 'js/main.js')

print("done")