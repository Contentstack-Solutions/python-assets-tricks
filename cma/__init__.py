'''
Contentstack's Content Management API Python wrapper
https://www.contentstack.com/docs/developers/apis/content-management-api/
oskar.eiriksson@contentstack.com
2020-09-28

Environmental Variables needed:
 - CS_REGION = EU/NA (Europe/North-America)
 - CS_MANAGEMENTOKEN (Stack Management Token)
 - CS_APIKEY (Stack API Key)
'''
import os
from time import sleep
import requests
import config

regionMap = {
    'NA': 'https://api.contentstack.io/',
    'na': 'https://api.contentstack.io/',
    'EU': 'https://eu-api.contentstack.com/',
    'eu': 'https://eu-api.contentstack.com/'
}

try:
    region = regionMap[os.getenv('CS_REGION', None)]
except KeyError:
    config.logging.warning('{}No Region defined - Defaulting to North America.{}'.format(config.YELLOW, config.END))
    region = 'https://api.contentstack.io/'

managementToken = os.getenv('CS_MANAGEMENTOKEN', None)
if not managementToken:
    config.logging.critical('{}Management Token Missing. Nothing will work.{}'.format(config.RED, config.END))

apiKey = os.getenv('CS_APIKEY', None)
if not apiKey:
    config.logging.critical('{}Stack API Key Missing. Nothing will work.{}'.format(config.RED, config.END))

managementTokenHeader = {
        'authorization': managementToken,
        'api_key': apiKey
    }

def logUrl(url):
    '''
    Logging out for debug purposes the constructed URL for any function
    '''
    config.logging.debug('-------')
    config.logging.debug('The CMA URL:')
    config.logging.debug(url)
    config.logging.debug('-------')


def logError(endpointName, name, url, res, msg='creating/updating'):
    config.logging.error('{}Failed {} {} (Name: {}){}'.format(config.RED, msg, endpointName, name, config.END))
    config.logging.error('{}URL: {}{}'.format(config.RED, url, config.END))
    config.logging.error('{}HTTP Status Code: {}{}'.format(config.RED, res.status_code, config.END))
    config.logging.error('{red}Error Message: {txt}{end}'.format(red=config.RED, txt=res.text, end=config.END))
    return None

def iterateURL(url, skip=0):
    return url + '&skip={}'.format(skip)

def typicalGetSimple(url, environment=None):
    '''
    Re-usable function to GET objects that never include more than 100 items
    '''
    if environment:
        url = url + '&environment={}'.format(environment)
    logUrl(url)
    res = requests.get(url, headers=managementTokenHeader)
    if res.status_code in (200, 201):
        config.logging.debug('Result: {}'.format(res.json()))
        return res.json()
    config.logging.error('{red}Export failed.{end}'.format(red=config.RED, end=config.END))
    config.logging.error('{}URL: {}{}'.format(config.RED, url, config.END))
    config.logging.error('{}HTTP Status Code: {}{}'.format(config.RED, res.status_code, config.END))
    config.logging.error('{red}Error Message: {txt}{end}'.format(red=config.RED, txt=res.text, end=config.END))
    return None

def typicalGetIterate(url, dictKey, environment=None):
    '''
    Re-usable function to GET objects that might have more than 100 items in it
    '''
    result = []
    skip = 0
    count = 1 # Just making sure we check at least once. Setting the real count value in while loop
    if environment:
        url = url + '&environment={}'.format(environment)
    config.logging.debug(url)
    originalURL = url
    while skip <= count:
        url = iterateURL(originalURL, skip)
        logUrl(url)
        res = requests.get(url, headers=managementTokenHeader)
        if res.status_code in (200, 201):
            if 'count' in res.json(): # Did get a KeyError once... when there was nothing there.
                count = res.json()['count'] # Setting the real value of count here
            else:
                count = 0
            config.logging.debug('{}Response Now: {} {}'.format(config.YELLOW, res.json(), config.END))
            result = result + res.json()[dictKey]
            config.logging.debug('{}Result as of Now: {} {}'.format(config.YELLOW, result, config.END))
            skip += 100
        else:
            config.logging.error('{red}All {key} Export: Failed getting {key}{end}'.format(red=config.RED, key=dictKey, end=config.END))
            config.logging.error('{}URL: {}{}'.format(config.RED, url, config.END))
            config.logging.error('{}HTTP Status Code: {}{}'.format(config.RED, res.status_code, config.END))
            config.logging.error('{red}Error Message: {txt}{end}'.format(red=config.RED, txt=res.text, end=config.END))
            return None
    if result:
        return {dictKey: result}
    config.logging.debug('No {} results'.format(dictKey))
    return None

def typicalUpdate(body, url, endpointName='', retry=False):
    '''
    Combining identical PUT methods into one
    '''
    logUrl(url)
    res = requests.put(url, headers=managementTokenHeader, json=body)
    if res.status_code in (200, 201):
        config.logging.info('Asset updated')
        return res.json()
    elif (res.status_code == 429) and not retry:
        config.logging.warning('{}We are getting rate limited. Retrying in 2 seconds.{}'.format(config.YELLOW, config.END))
        sleep(2) # We'll retry once in a second if we're getting rate limited.
        return typicalUpdate(body, url, endpointName, True)
    config.logging.error('{}Failed updating {} - {}{}'.format(config.RED, endpointName, str(res.text), config.END))
    return logError(endpointName, '', url, res) # Empty string was name variable


def createAsset(filePath, metaData, filename):
    '''
    Upload Image/Asset
    sample url: https://api.contentstack.io/v3/assets?relative_urls=false
    documentation on endpoint: https://www.contentstack.com/docs/developers/apis/content-management-api/#upload-asset
    '''
    url = '{}v3/assets?relative_urls=false'.format(region)
    contentTypeMeta = metaData['asset']['content_type']
    # header = managementTokenHeader
    # del header['Content-Type']
    with open(filePath, 'rb') as f:
        fileData = f.read()
    files = {"asset[upload]": (filename, fileData, contentTypeMeta)}
    payload = {}
    if 'parent_uid' in metaData['asset']:
        payload["asset[parent_uid]"] = (metaData['asset']['parent_uid'])    
    if 'description' in metaData['asset']:
        payload["asset[description]"] = (metaData['asset']['description'])
    if 'title' in metaData['asset']:
        payload["asset[title]"] = (metaData['asset']['title'])
    if 'tags' in metaData['asset']:
        payload["asset[tags]"] = (metaData['asset']['tags'])
    res = requests.post(url, files=files, data=payload, headers=managementTokenHeader)
    if res.status_code in (200, 201):
        config.logging.info('Asset Uploaded. ({})'.format(filename))
        return res.json()
    return logError('asset', filename, url, res)

def publishAsset(uid, locales, environments):
    '''
    Publishes an asset
    sample url: https://api.contentstack.io/v3/assets/{asset_uid}/publish
    documentation on endpoint: https://www.contentstack.com/docs/developers/apis/content-management-api/#publish-an-asset
    '''
    url = '{}v3/assets/{}/publish'.format(region, uid)
    body = {
        'asset': {
            'locales': locales,
            'environments': environments
        }
    }
    res = requests.post(url, json=body, headers=managementTokenHeader)
    if res.status_code in (200, 201):
        config.logging.info('Asset Published. ({})'.format(uid))
        return res.json()
    return logError('asset', uid, url, res, 'publishing')

def getAllAssets(query=None, environment=None, folders=False):
    '''
    Get All Assets (Content Management API)
    sample url: https://api.contentstack.io/v3/assets?include_folders=true&include_publish_details=true&include_count=true&relative_urls=false&environment={environment}
    '''
    url = '{region}v3/assets?include_publish_details=true&include_count=true&relative_urls=false'.format(region=region)
    if query:
        url = url + query
    if folders:
        url = url + '&include_folders=true'
    return typicalGetIterate(url, 'assets', environment)

def getSingleAsset(uid):
    '''
    Get a Single Asset (Content Management API)
    sample url: https://api.contentstack.io/v3/assets/{asset_uid}?include_path=true&include publish_details=true&relative_urls=false
    '''
    url = '{region}v3/assets/{uid}?include_path=true&include publish_details=true&relative_urls=false'.format(region=region, uid=uid)
    return typicalGetSimple(url)

def getAssetReferences(uid):
    '''
    Get Asset references (Content Management API)
    Not really documented - But documentation is available for entries: https://www.contentstack.com/docs/developers/apis/content-management-api/#get-references-of-an-entry
    Works the same way for assets.
    sample url: https://api.contentstack.io/v3/assets/{asset_uid}/references
    '''
    url = '{region}v3/assets/{uid}/references'.format(region=region, uid=uid)
    return typicalGetSimple(url)

def updateAsset(uid, body):
    '''
    Update Asset
    sample url: https://api.contentstack.io/v3/assets/{asset_uid}
    '''
    url = '{region}v3/assets/{uid}'.format(region=region, uid=uid)
    body = {'asset': body}
    return typicalUpdate(body, url, 'asset')

def updateFolder(uid, body):
    '''
    Update Folder
    sample url: https://api.contentstack.io/v3/assets/folders/{folder_uid}
    '''
    url = '{region}v3/assets/folders/{uid}'.format(region=region, uid=uid)
    body = {'asset': body}
    return typicalUpdate(body, url, 'asset')

def deleteFolder(uid, retry=False):
    '''
    Delete a Folder - !!!Be careful here!!!
    sample url: https://api.contentstack.io/v3/assets/folders/{folder_uid}
    '''
    url = '{region}v3/assets/folders/{uid}'.format(region=region, uid=uid)
    res = requests.delete(url, headers=managementTokenHeader)
    if res.status_code in (200, 201):
        config.logging.info('Folder {} deleted'.format(uid))
        return res.json()
    elif (res.status_code == 429) and not retry:
        config.logging.warning('{}We are getting rate limited. Retrying in 2 seconds.{}'.format(config.YELLOW, config.END))
        sleep(2) # We'll retry once in a second if we're getting rate limited.
        return deleteFolder(uid, True)
    config.logging.error('{}Failed deleting folder - {}{}'.format(config.RED, str(res.text), config.END))
    return logError('folder', '', url, res) # Empty string was name variable

def deleteAsset(uid, retry=False):
    '''
    Delete an Asset - !!!Be careful here!!!
    sample url: https://api.contentstack.io/v3/assets/{asset_uid}
    '''
    url = '{region}v3/assets/{uid}'.format(region=region, uid=uid)
    res = requests.delete(url, headers=managementTokenHeader)
    if res.status_code in (200, 201):
        config.logging.info('Asset {} deleted'.format(uid))
        return res.json()
    elif (res.status_code == 429) and not retry:
        config.logging.warning('{}We are getting rate limited. Retrying in 2 seconds.{}'.format(config.YELLOW, config.END))
        sleep(2) # We'll retry once in a second if we're getting rate limited.
        return deleteAsset(uid, True)
    config.logging.error('{}Failed deleting asset - {}{}'.format(config.RED, str(res.text), config.END))
    return logError('asset', '', url, res) # Empty string was name variable


def getAllFolders():
    '''
    Get all Folders
    sample url: https://api.contentstack.io/v3/assets?query={"is_dir": true}&include_count=true
    '''
    url = '{region}v3/assets?query={{"is_dir": true}}&include_count=true'.format(region=region)
    return typicalGetIterate(url, 'assets')


def getAllLanguages(apiKey, token, region):
    '''
    Gets all languages
    sample url: https://api.contentstack.io/v3/locales?include_count={boolean_value}
    '''
    url = '{region}v3/locales?include_count=true'.format(region=region)
    return typicalGetIterate(url, 'locales')

def getAllEnvironments(apiKey, token, region):
    '''
    Gets all environments
    sample url: https://api.contentstack.io/v3/environments?include_count={boolean_value}&asc={field_uid}&desc={field_uid}
    '''
    url = '{region}v3/environments?include_count=true'.format(region=region)
    return typicalGetIterate(url, 'environments')
