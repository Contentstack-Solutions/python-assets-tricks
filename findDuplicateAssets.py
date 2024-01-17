'''
Finds assets that are duplicated in a stack.
vidar.masson@contentstack.com
2022-09-22

------Update 2024-01-17------
oskar.eiriksson@contentstack.com
Optionally also prints out the entries that reference the assets.
------Update 2024-01-17------

Environmental Variables needed:
 - CS_REGION = EU/NA (Europe/North-America)
 - CS_MANAGEMENTOKEN (Stack Management Token)
 - CS_APIKEY (Stack API Key)
'''
from collections import defaultdict
import pprint

import cma

pp = pprint.PrettyPrinter(indent=4)
l = cma.getAllAssets(folders=True)

findReferences = True # If set to True it will execute slower as it will check all entries for references to the asset and print out

sizes =  defaultdict(list) # dict with bytecount ints as keys and list of uids that have that size
assetmap = {} # dict with uids as keys and full item data as values
folders = {}

def get_name(item):
    name = item['name'] if item['is_dir'] else item['title']
    try:
        if item['parent_uid']:
            parent_folder_uid = item['parent_uid']
            name = get_name(folders[parent_folder_uid]) + '/' + name
    except KeyError:
        print('No parent specified:', item['uid'])
    return name

def findAssetReferences(uid):
    references = cma.getAssetReferences(uid)
    refStr = ''
    for entry in references['references']:
        refStr += '\n Content Type: ' + entry['content_type_uid'] + ', Entry UID: ' + entry['entry_uid'] + ', Locale: ' + entry['locale']
    return refStr


for item in l['assets']:
    if item['is_dir']:
        folders[item['uid']] = item
    else:
        sizes[item['file_size']].append(item['uid'])
        assetmap[item['uid']] = item


for key, value in sizes.items():
    if len(value) > 1:
        print('Files of size: ', key)
        print('=================================')
        for x in value:
            url = assetmap[x]['url']
            path = get_name(assetmap[x])
            fn = assetmap[x]['filename']
            if findReferences:
                references = findAssetReferences(assetmap[x]['uid'])
        
            print('Path    :', path)
            print('Full URL:', url)
            print('Filename:', fn)
            if findReferences:
                print('Referenced in entries:', references)
            print()
        print('=================================')
        print()
        print()

