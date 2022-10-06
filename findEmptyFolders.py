'''
Finds folders that are empty. Either print out or delete them.
oskar.eiriksson@contentstack.com
2022-10-06

Note: If there is a folder in the folder this script does not define it as empty. If the nested folder is empty, that is detected as empty, but not the parent folder. 
Deleting the nested folder and running this script again solves that use case.
'''
import time
import cma
import config

'''
Environmental Variables needed:
 - CS_REGION = EU/NA (Europe/North-America)
 - CS_MANAGEMENTOKEN (Stack Management Token)
 - CS_APIKEY (Stack API Key)

What to do with empty folders?
    - 1. Just print them out?
        - Set deleteEmptyFolders to False
    - 2. Do we want to delete empty folders?
        - Set deleteEmptyFolders to True
        - Be careful
'''

assets = cma.getAllAssets(None, None, True) # Getting all assets from Stack, including folders.

deleteEmptyFolders = False # Set to True if you want to Delete the empty folders

parentArr = []
folderArr = []
for asset in assets['assets']:
    if asset['is_dir']:
        folderArr.append(asset)
    if 'parent_uid' in asset:
        folder = asset['parent_uid']
        if folder and folder not in parentArr:
            parentArr.append(folder)

emptyArr = [] 
for folder in folderArr:
    if folder['uid'] not in parentArr:
        emptyArr.append({'name': folder['name'], 'uid': folder['uid']})

config.logging.info('{}Number of empty folders found: {}{}'.format(config.YELLOW, len(emptyArr), config.END))
for folder in emptyArr:
     print('Name: {} - UID: {}'.format(folder['name'], folder['uid']))
     if deleteEmptyFolders:
        cma.deleteFolder(folder['uid'])