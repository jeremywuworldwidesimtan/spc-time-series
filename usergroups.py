import json

with open('usergroups.json') as f:
    ug = json.load(f)

for k in ug.keys():
    contact_info = ""
    if len(ug[k]) == 1:
        contact_info = ug[k][0]
    elif len(ug[k]) == 2:
        contact_info = ug[k][0] + " and " + ug[k][1]
    elif len(ug[k]) >= 3:
        for n in range(len(ug[k]) - 2):
            contact_info += f"{ug[k][n]}, "
        contact_info += ug[k][-2] + " and " + ug[k][-1]
    print(contact_info)