from config import URL
from datadiff import diff
from lib import rest, send_slack


projects = [x for x in rest.get("/projects/?p=PROJECT").keys()]
projects.extend([x for x in rest.get("/projects/?p=OEM").keys()])
groups = rest.get("/groups/")
modified = []
for project in projects:
    group_data = groups.get(project, None)
    if not group_data:
        print(f"Missing group for {project} - creating")
        rest.put(f"/groups/{project}")
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
        'refs/heads/lineage-18.0': { 'permissions': {
            'create': {
                'rules': {group: {
                    'action': 'ALLOW',
                    'force': False
                }}
            }
        }},
        'refs/heads/lineage-18.1': { 'permissions': {
            'create': {
                'rules': {group: {
                    'action': 'ALLOW',
                    'force': False
                }}
            }
        }},
    }
    perms = rest.get(f"/projects/{project}/access")['local']
    if new == perms:
        continue
    else:
        remove = {
            "remove": {"refs/heads/*": {}}
        }
        if perms:
            remove = rest.post(f"/projects/{project}/access", j={'remove': perms})
        add = rest.post(f"/projects/{project}/access", j={"add": new})
        print(f"Reset {project}")
        modified.append(project)

if modified:
    send_slack(f"Reset project permissions on {', '.join(modified)}")
