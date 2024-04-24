import json

with open('read_page.json', 'r') as json_file:
    data = json.load(json_file)

for line in data:
    for page, library in line.items():
        # for title, author in library[0].items():
            print(f'{page} --- {library}')
