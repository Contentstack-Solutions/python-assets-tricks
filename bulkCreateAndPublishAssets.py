'''
Bulk create and publish Assets - See comments below for different possibilies.
oskar.eiriksson@contentstack.com
2020-01-04
'''
import os
import mimetypes
import cma
import config

folder = '/tmp/tmpImages/' # Path to folder with all assets that you want to import. Must end with a '/'.
locales = ['en-us'] # An array of languages - Used if you want to publish asset, can publish to more than one.
environments = ['development'] # An array of environments - Used if you want to publish asset, can publish to more than one.
parentFolder = 'bltc4b32745b2a66d24' # UID of parent folder being something like this: 'bltcbf66fcb8b9b3d6a' - Set to None if you want to import to root folder.

checkIfDuplicate = True # If set to True - the script checks if a file with the same name exists in the same folder in the DAM - If it exists, it skips uploading.
publishAsset = True # If set to True we also attempt to publish the asset to defined environment(s)

def findDuplicate(f, parentFolder):
    '''
    Function that looks if file with the same name exists already
    '''
    f = f.replace(' ', '_')
    if parentFolder:
        a = cma.getAllAssets('&query={"$and":[{"title": "' + f +'"},{"parent_uid": "' + parentFolder + '"}]}')
    else:
        a = cma.getAllAssets('&query={"$and":[{"title": "' + f +'"},{"parent_uid": null}]}')
    
    if a:
        return True 
    return False

'''
Uncomment this (comment other part of code below that while running) to see uids and names of all folders - if you want to define a folder to bulk import to.
'''
# allFolders = cma.getAllFolders()
# for folder in allFolders['assets']:
#     print(folder['uid'], folder['name'])

'''
Bulk create below - Remember to comment out below if you're only running the script to see the folders in your stack.
'''

metaData = {
    'asset': {
        'parent_uid': parentFolder
        }
}

for f in os.listdir(folder):
    metaData['asset']['content_type'] = mimetypes.guess_type(f)[0]
    filePath = folder + f
    isDuplicate = False
    if checkIfDuplicate: # Checking if file with same name exists in the same folder in Contentstack
        isDuplicate = findDuplicate(f, parentFolder)
    if isDuplicate:
        config.logging.info('Skipping file "{}" - File with same name in same folder already present in Contentstack.'.format(f))
    else:
        newAsset = cma.createAsset(filePath, metaData, f)
        '''
        Publishing Asset below if configured above
        '''
        if publishAsset and newAsset:
            uid = newAsset['asset']['uid']
            cma.publishAsset(uid, locales, environments)

