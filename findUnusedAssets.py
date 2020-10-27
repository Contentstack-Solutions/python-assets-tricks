'''
Finds assets that are not referenced in any entries.
oskar.eiriksson@contentstack.com
2020-10-10
'''
import time
import cma
import config

'''
Environmental Variables needed:
 - CS_REGION = EU/NA (Europe/North-America)
 - CS_MANAGEMENTOKEN (Stack Management Token)
 - CS_APIKEY (Stack API Key)

What to do with empty references?
    - 1. Just print them out?
        - See Method 1
    - 2. Do we want to delete unused assets?
        - See Method 2
        - Delete asset(s) that are not referred within any entries
    - 3. Do we want to create a CSV report with them?
        - See Method 3
    - 4. Do we want to update them with a tag?
        - See Method 4
'''

assets = cma.getAllAssets() # Getting all assets from Stack

'''
Method 1 - Prints them out
'''
for asset in assets['assets']:
    assetReferences = cma.getAssetReferences(asset['uid'])
    if not assetReferences['references']:
        config.logging.info('{bold}{uid}{end} not referenced in any entries. Title: {bold}{title}{end}, URL: {underline}{url}{end}'.format(uid=asset['uid'], title=asset['title'], url=asset['url'], bold=config.BOLD, end=config.END, underline=config.UNDERLINE))

'''
Method 2 - Delete asset - !!!Be careful here!!!
'''
# for asset in assets['assets']:
#     assetReferences = cma.getAssetReferences(asset['uid'])
#     if not assetReferences['references']:
#         cma.deleteAsset(asset['uid'])



'''
Method 3 - Create a CSV Report with a timestamp - Possible to open report with e.g. Excel.
'''
# timeStr = time.strftime("%Y%m%d-%H%M%S") # For report file
# filename = timeStr + '-report.csv'
# reportFile = open(filename, 'a') # report file
# reportFile.write('uid;filename;url\n')
# config.logging.info('Creating a report file: {}'.format(filename))
# for asset in assets['assets']:
#     assetReferences = cma.getAssetReferences(asset['uid'])
#     if not assetReferences['references']:
#         config.logging.info('Unused asset - Adding to CSV Report: {}'.format(asset['title']))
#         reportFile.write(asset['uid'] + ';' + asset['title'] + ';' + asset['url'] + '\n')
# reportFile.close()



'''
Method 4 - Tag unused assets

Updating the asset with the tag "unused" - That tag can then be used to query the asset, e.g. using advanced search in web application
'''
# tag = 'unused' # To update assets with
# for asset in assets['assets']:
#     assetReferences = cma.getAssetReferences(asset['uid'])
#     if not assetReferences['references']: # No References - So we know that no entries reference that asset.
#         if tag not in asset['tags']:
#             asset['tags'].append(tag)
#             cma.updateAsset(asset['uid'], asset) # Updating the asset with the new tag
#         else:
#             config.logging.info('Asset already tagged with unused tag')
