import json

data = dict()

distractions = dict()
distractions["conversation"] = 1.5
distractions["spacing out"] = 1.2
distractions["youtube"] = 1.5
distractions["instagram"] = 1.2
distractions["messenger"] = 1.0
distractions["texting"] = 5.1

data["focused"] = 3.5
data["distracted"] = distractions
data["light"] = 1
data["noise"] = 0.5

output = json.dumps(data)
pretty_output = json.dumps(data, indent=4)

print(output)
print(pretty_output)