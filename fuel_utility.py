''' Gazebo v7.0 to v11.0 Utility for Fuel Models where fuel API is not enabled.

Usage:
  fuel_utility.py download [-q <query>] [(-m MODEL ...)] [-v, --version] [--verbose] [-d <DESTINATION>]

Options:
  -h --help                        Show this screen.
  -m MODEL, --model=MODEL          A list of models to download and include by name.
  -d <DESTINATION>, --destination=DESTINATION  The destination folder to download and extract the models. [default: fuel_models]
  -q <QUERY>, --query=QUERY        The query to run in Ignition Fuel's database. 
  --verbose         Show debug messages
  -v, --version     Get version of application.
'''

import requests
import sys
import json
import logging
import time
from docopt import docopt
import zipfile
import io
from lxml import etree as ET
import os.path

FUEL_URI = 'https://fuel.ignitionrobotics.org/1.0/OpenRobotics/models'
WAIT_BETWEEN_DOWNLOADS_IN_SECONDS = 5

class FuelModelUtility:

    models = []

    def __init__(self):
        logging.info('Starting fuel models..')

    def getModelList(self):
        return self.models

    def appendModelSearchResults(self, page, category):
        url = '%s?q=%s&page=%s' % (FUEL_URI, category, str(page))
        response = requests.get(url)
        modelArray = json.loads(response.text)
        self.models.extend(modelArray)
        page += 1
        if (len(modelArray) >= 20):
            self.appendModelSearchResults(page, category)

    def appendSingleModel(self, model_info):
        
        if ('=' in model_info):
            model_name, model_version = model_info.split('=')
        else:
            model_name = model_info
            model_version = None

        url = '/'.join([FUEL_URI, model_name])
        response = requests.get(url)
        model = json.loads(response.text)

        if (model_version):
            model['version'] = model_version

        self.models.append(model)

    def getByCategory(self, category):
        self.appendModelSearchResults(1, category)

    def getByModel(self, model_info):
        self.appendSingleModel(model_info)

    def createDatabaseFile(self, directory):
        database = ET.Element('database')
        name = ET.SubElement(database, 'name')
        name.text = 'Ignition Fuel Model Database'
        license = ET.SubElement(database, 'license')
        license.text = 'Creative Commons Attribution 3.0 Unported'
        models = ET.SubElement(database, 'models')
        for i, model in enumerate(self.models):
            uri = ET.SubElement(models, 'uri')
            uri.text = model['name']
        self.write_file('%s/database.config' % directory, database)

    def write_file(self, output_filename, root):
        f = open(output_filename, 'wb')
        xml_string = ET.tostring(root,
                                 pretty_print=True,
                                 encoding='utf-8',
                                 xml_declaration=True)
        f.write(xml_string)
        f.close()

    def downloadAndExtractModels(self, directory):
        for model in self.models:
            if os.path.isdir('/'.join([directory, model['name']])):
                logging.info('Model %s already downloaded.', model['name'])
            else:
                logging.info('Downloading %s', model['name'])
                if ('version' in model):
                    model_version = str(model['version'])
                else:
                    model_version = "1"
                url = '/'.join([FUEL_URI,
                                model['name'],
                                model_version,
                                model['name']])
                response = requests.get('%s.zip' % url, stream=True)
                if (response.status_code != 200): 
                    logging.error('Model version does not exist.')
                else:
                    z = zipfile.ZipFile(io.BytesIO(response.content))
                    z.extractall('/'.join([directory, model['name']]))
                time.sleep(WAIT_BETWEEN_DOWNLOADS_IN_SECONDS)
                logging.info('Sleeping for %i second(s) between file downloads.', WAIT_BETWEEN_DOWNLOADS_IN_SECONDS)

if __name__ == '__main__':

    arguments = docopt(__doc__, version='Ignition Fuel CLI Utility V1.0')

    if (arguments['--verbose']):
        logging.basicConfig(level=logging.DEBUG)

    logging.debug('Arguments provided: %s', json.dumps(arguments))
    fuel_util = FuelModelUtility()

    for model in arguments['--model']:
        logging.info('Fetching model %s.', model)
        fuel_util.getByModel(model)

    if (arguments['--query']):
        logging.info('Collecting models from query: %s.', arguments['--query'])
        fuel_util.getByCategory(arguments['--query'])

    logging.debug('Complete model list: %s', fuel_util.getModelList())
    logging.info('Downloading zip files and extracting them into %s directory', arguments['--destination'])
    fuel_util.downloadAndExtractModels(arguments['--destination'])
    logging.info('Creating database file: %s/database.config', arguments['--destination'])
    fuel_util.createDatabaseFile(arguments['--destination'])
    logging.info('All done!')