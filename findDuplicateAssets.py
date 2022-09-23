'''
Finds assets that are duplicated in a stack.
vidar.masson@contentstack.com
2022-09-22

Environmental Variables needed:
 - CS_REGION = EU/NA (Europe/North-America)
 - CS_MANAGEMENTOKEN (Stack Management Token)
 - CS_APIKEY (Stack API Key)
'''
from collections import defaultdict
from types import SimpleNamespace
import pprint

import cma

pp = pprint.PrettyPrinter(indent=4)
l = cma.getAllAssets(folders=True) # Getting all assets from Stack
# l = SimpleNamespace(**l)

sizes =  defaultdict(list) # dict with bytecount ints as keys and list of uids that have that size
items = {} # dict with uids as keys and full item data as values
folders = {}

def get_name(item):
    name = item['name'] if item['is_dir'] else item['title']
    if item['parent_uid']:
        parent_folder_uid = item['parent_uid']
        name = get_name(folders[parent_folder_uid]) + '/' + name
    return name

for item in l['assets']:
    # build up tree
    if item['is_dir']:
        folders[item['uid']] = item
    else:
        sizes[item['file_size']].append(item['uid'])
        items[item['uid']] = item


for key, value in sizes.items():
    if len(value) > 1:
        print('Files of size: ', key)
        for x in value:
            url = items[x]['url']
            path = get_name(items[x])
            fn = items[x]['filename']
            print(fn, path, url)
        print()


