# python-assets-tricks
Playing around with Assets - Creating them, publishing... Finding unreferenced assets and moving them between folders

## Prerequisites:
* Contentstack Account.
* Install Python 3 (Developed using Python 3.7.6 on Macbook).
* Install Python package:
  * `pip install requests`

## Define environmental variables
e.g. `variables.env` file:
```
CS_REGION=NA (Either NA or EU)
CS_APIKEY=blt972.....
CS_MANAGEMENTOKEN=cs....

export CS_REGION CS_APIKEY CS_MANAGEMENTOKEN
```
and run `source variables.env` in the terminal.

## Three scripts available
1. Find unused assets - `findUnusedAssets.py`

Fetches all assets and iterated through them finding if any entries are referencing them.

Available methods (Just uncomment chosen method):
 * Just print them out
 * Delete unused asset (Be careful)
 * Write to a CSV report file
 * Update unused asset in Contentstack with a tag

2. Move assets between folders - `moveAssetsBetweenFolders.py`

You can run the script once to see uid's of all folders.
Then define the source and destination uid's in the script - and run again.

3. Bulk create assets and publish them - `bulkCreateAndPublishAssets.py`

Reads files from a folder and attempts to upload all of them to Contentstack and then publish them.
You can specify a folder uid where you want to upload - Set to None if you want to upload to the root folder.
Comment out comment if you don't want to publish asset right after uploading.
