import cma
import config

folders = cma.getAllFolders()


config.logging.info('{}Listing out all folder names and uids - Can be used to identify from what folder to what folder you want to move assets{}'.format(config.BOLD, config.END))
for folder in folders['assets']:
    config.logging.info('Name: {} - uid: {}'.format(folder['name'], folder['uid']))


sourceFolderUid = 'bltcbf66fcb8b9b3d6a' # Find these UIDs using the folder for loop above
destinationFolderUid = 'blt1c572f715be4f01e'

query = '&query={{"parent_uid": "{}"}}'.format(sourceFolderUid)
assets = cma.getAllAssets(query)
for asset in assets['assets']:
    asset['parent_uid'] = destinationFolderUid
    if asset['is_dir']:
        cma.updateFolder(asset['uid'], asset) # If the asset is a folder, not a file, we need a little bit different function
    else:
        cma.updateAsset(asset['uid'], asset) # If asset is file
