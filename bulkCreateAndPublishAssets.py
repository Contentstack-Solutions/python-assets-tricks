'''
Bulk create and publish Assets - See comments below.
oskar.eiriksson@contentstack.com
2020-01-04
'''
import os
import cma
import mimetypes

folder = '/tmp/tmpImages/' # Path to folder with all assets that you want to import. Must end with a '/'.
locales = ['en-us'] # An array of languages - Used if you want to publish asset, can publish to more than one.
environments = ['development'] # An array of environments - Used if you want to publish asset, can publish to more than one.
parentFolder = None # UID of parent folder being something like this: 'bltcbf66fcb8b9b3d6a' - Set to None if you want to import to root folder.

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
    newAsset = cma.createAsset(filePath, metaData, f)
#     '''
#     Publishing Asset below - Comment out if you only want to create it, not publish
#     '''
#     if newAsset:
#         uid = newAsset['asset']['uid']
#         cma.publishAsset(uid, locales, environments)

