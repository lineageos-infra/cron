from lib import rest

projects = [x for x in rest.get("/projects/?p=PROJECT").keys()]
projects.extend([x for x in rest.get("/projects/?p=OEM").keys()])
groups = rest.get("/groups/")
filtered_groups = [x for x in groups.keys() if any([x.startswith("OEM"), x.startswith("PROJECT")])]

parent_id = groups['Head Developers']['id']

for group in filtered_groups:
    _id = groups[group]['id']
    if groups[group]['owner'] != 'Head Developers':
        print(f'{group} isn\'t owned by Head Developers, fixing')
        rest.put('/groups/{}/owner'.format(_id), {'owner': parent_id})
