# python-assets-tricks
Playing around with Assets - Finding unreferenced assets and moving them between folders

## Prerequisites:
* Contentstack Account.
* Install Python 3 (Developed using Python 3.7.6 on Macbook).
* Install Python package:
  * `pip install requests`

## Define environmental variables
e.g. `variables.env` file:
```
CS_REGION=NA
CS_APIKEY=blt972.....
CS_MANAGEMENTOKEN=cs....

export CS_REGION CS_APIKEY CS_MANAGEMENTOKEN
```
and run `source variables.env` in the terminal.

## Two scripts available
1. Find unused assets - `findUnusedAssets.py`

Fetches all assets and iterated through them finding if any entries are referencing them.

Available methods (Just uncomment chosen method):
 * Just print them out
 * Delete unused asset (Be careful)
 * Write to a CSV report file
 * Update unused asset in Contentstack with a tag
 
2. Move Assets between folders - `moveAssetsBetweenFolders.py`

You can run the script once to see uid's of all folders.
Then define the source and destination uid's in the script - and run again.
