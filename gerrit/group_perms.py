import json

import requests
from requests.auth import HTTPBasicAuth
from config import USERNAME, PASSWORD, URL
from datadiff import diff


class rest:
    auth = HTTPBasicAuth(USERNAME, PASSWORD)

    @classmethod
    def get(cls, url):
        req = requests.get("https://review.lineageos.org/a{}".format(url), auth=cls.auth)
        if req.status_code == 200:
            raw = req.text[5:]
            return json.loads(raw)

    @classmethod
    def post(cls, url, j):
        req = requests.post("https://review.lineageos.org/a{}".format(url), auth=cls.auth, json=j)
        if req.status_code == 500:
            print("Error applying {}: {}".format(url, req.text))

projects = [x for x in rest.get("/projects/?p=PROJECT").keys()]
projects.extend([x for x in rest.get("/projects/?p=OEM").keys()])
groups = rest.get("/groups/")
for project in projects:
    group_data = groups.get(project, None)
    if not group_data:
        print("Missing group for {} - creating".format(project))
        rest.put("/groups/{}".format(project))
        continue
    group = str(group_data["id"])
    new = {
        'refs/heads/*': { 'permissions': {
            'label-Code-Review': {
                'rules': { group: {
                    'action': 'ALLOW',
                    'force': False,
                    'max': 2,
                    'min': -2,
              }},
              'label': 'Code-Review'
            },
           'label-Verified': {
               'rules': { group: {
                   'action': 'ALLOW',
                   'force': False,
                   'max': 1,
                   'min': -1,
             }},
             'label': 'Verified'
           },
            'submit': {
                'rules': { group: {
                    'action': 'ALLOW',
                    'force': False
                }}
            },
            'forgeAuthor': {
                'rules': { group: {
                    'action': 'ALLOW',
                    'force': False
                }}
            },
            'push': {
                'rules': { group: {
                    'action': 'ALLOW',
                    'force': False
                }}
            },
            'forgeCommitter': {
                'rules': { group: {
                    'action': 'ALLOW',
                    'force': False
                }}
            },
            'abandon': {
                'rules': {group: {
                    'action': 'ALLOW',
                    'force': False
                }}
            },
            'editTopicName': {
                'rules': {group: {
                    'action': 'ALLOW',
                    'force': False
                }}
            },
        }},
        'refs/heads/staging/*': { 'permissions': {
            'create': {
                'rules': {group: {
                    'action': 'ALLOW',
                    'force': False
                }}
            },
        }},
        'refs/heads/backup/*': { 'permissions': {
            'create': {
                'rules': {group: {
                    'action': 'ALLOW',
                    'force': False
                }}
            }
        }},
        'refs/heads/cm-14.1': { 'permissions': {
            'create': {
                'rules': {group: {
                    'action': 'ALLOW',
                    'force': False
                }}
            }
        }},
        'refs/heads/lineage-15.1': { 'permissions': {
            'create': {
                'rules': {group: {
                    'action': 'ALLOW',
                    'force': False
                }}
            }
        }},
        'refs/heads/lineage-16.0': { 'permissions': {
            'create': {
                'rules': {group: {
                    'action': 'ALLOW',
                    'force': False
                }}
            }
        }},
        'refs/heads/lineage-17.1': { 'permissions': {
            'create': {
                'rules': {group: {
                    'action': 'ALLOW',
                    'force': False
                }}
            }
        }},

    }
    perms = rest.get("/projects/{}/access".format(project))['local']
    if new == perms:
        print("No Changes - {}".format(project))
    else:
        remove = {
            "remove": {"refs/heads/*": {}}
        }
        if perms:
            remove = rest.post("/projects/{}/access".format(project), j={'remove': perms})
        add = rest.post("/projects/{}/access".format(project), j={"add": new})
        print("Reset {}".format(project))
