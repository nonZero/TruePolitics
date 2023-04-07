import csv
from datetime import datetime
import re
import json
from pprint import pp

# This script is WIP and is not guaranteed to work

# Load mks.json
with open('./statements/data/mks.json', 'r') as f:
    mks = json.load(f)

# Get the list of names from mks
names = [mk['name'] for mk in mks]

# Load and parse gold.jsonl
with open('output.jsonl', 'r') as f:
    data = [json.loads(line) for line in f]

# Remove objects without '\n\n' in the text field
data = [obj for obj in data if '\n\n' in obj['text']]

# Split the text field by '\n\n' and save in parsed_text
for obj in data:
    obj['parsed_text'] = obj['text'].split('\n\n')

def has_consecutive_chars(str1, str2):
    return any(str1[i:i+4] in str2 for i in range(len(str1)-3))

def find_max_consecutive_chars(arr, str2):
    max_count = 0
    max_str = None

    for s in arr:
        count = 0
        for i in range(len(s)-3):
            if s[i:i+4] in str2:
                count += 1
        if count > max_count:
            max_count = count
            max_str = s

    return max_str

def get_mk_name(str):
    try:
        return next(name for name in names if any(any(subname == substr for substr in str.split()) for subname in name.split()))
    except:
        return 'fuck you'

# Filter out objects whose parsed_text field doesn't contain a name from mks
data = [obj for obj in data if any("עובדות" in text for text in obj['parsed_text'])]


# Convert each object in data to the new structure
for obj in data:
    obj['reviewed_by'] = 'בודקים'
    obj['content'] = obj['parsed_text'][0]
    obj['date'] = datetime.strptime(obj['created_at'], '%Y-%m-%dT%H:%M:%S%z').date()
    urlParse = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+/[^\s]+', obj['text'])
    obj['url'] = urlParse[-1] if len(urlParse) > 0 else ''
    if (len(urlParse) > 0):
        obj['url'] = urlParse[-1]
    else:
        obj['url'] = ""
    obj['review'] = '\n\n'.join([x.replace(obj['url'], '') for x in obj['parsed_text'][1:]])
    obj['review_date'] = obj['date']
    obj['review_url'] = obj['url']
    # We need to add logic to add person field here

    del obj['parsed_text']
    del obj['text']
    del obj['id']
    del obj['created_at']



open('output.json', 'w').write(json.dumps(data, ensure_ascii=False, indent=4, sort_keys=True, default=str))

with open('result.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['reviewed_by', 'person', 'content', 'date', 'url', 'review', 'review_date', 'review_url'])
    writer.writeheader()
    for obj in data:
        writer.writerow(obj)