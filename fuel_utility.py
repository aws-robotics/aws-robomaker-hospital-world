""" Gazebo v7.0 to v11.0 Utility for Fuel Models where fuel API is not enabled.

Usage:
  fuel_utility.py download [-q <query>] [(-m MODEL ...)] [-v, --version] [--verbose] [-d <DESTINATION>]

Options:
  -h --help                        Show this screen.
  -m MODEL, --model=MODEL          A list of models to download and include by name.
  -d <DESTINATION>, --destination=DESTINATION  The destination folder to download and extract the models. [default: fuel_models]
  -q <QUERY>, --query=QUERY        The query to run in Ignition Fuel's database. 
  --verbose         Show debug messages
  -v, --version     Get version of application.
"""

import requests
import sys
import json
import logging
import time
from docopt import docopt
import zipfile
import io
import xml.etree.ElementTree as ET
import xml.dom.minidom
import os.path

FUEL_URI="https://fuel.ignitionrobotics.org/1.0/OpenRobotics/models"
WAIT_BETWEEN_DOWNLOADS_IN_SECONDS=5

class FuelModelUtility: 

    models = []  

    def __init__(self):
        logging.info("Starting fuel models..")

    def getModelList(self):
        return self.models

    def appendModelSearchResults(self, page, category):
        response = requests.get(FUEL_URI+"?q="+category+"&page="+str(page))
        modelArray = json.loads(response.text)
        self.models.extend(modelArray)
        page += 1
        if (len(modelArray)>=20):
            self.appendModelSearchResults(page, category)

    def appendSingleModel(self, model_name):
        response = requests.get(FUEL_URI+"/"+model_name)
        model = json.loads(response.text)
        self.models.append(model)
    
    def getByCategory(self, category):
        self.appendModelSearchResults(1, category)

    def getByModel(self, model_name):
        self.appendSingleModel(model_name)
    
    def getModelUrl(self, model_name, model_version):
        return "/".join([FUEL_URI, model_name, model_version, model_name + ".zip"]) 

    def createDatabaseFile(self, directory):
        database = ET.Element('database')
        name = ET.SubElement(database, 'name')
        name.text = "Ignition Fuel Model Database"
        license = ET.SubElement(database, 'license')
        license.text = "Creative Commons Attribution 3.0 Unported"
        models = ET.SubElement(database, 'models')
        for i, model in enumerate(self.models):
            uri = ET.SubElement(models, 'uri')
            uri.text = model['name']
        database_xml = xml.dom.minidom.parseString(ET.tostring(database)) 
        database_xml = database_xml.toprettyxml()
        out_file = open(directory+"/database.config", "w")
        out_file.write(database_xml)

    def downloadAndExtractModels(self, directory):
        for model in self.models:
            if os.path.isdir(directory+"/"+model['name']):
                logging.info("Model %s already downloaded.", model['name'])
            else:
                logging.info("Downloading %s", model['name'])
                url = self.getModelUrl(model['name'], "2")
                response = requests.get(url, stream=True)
                try:
                    z = zipfile.ZipFile(io.BytesIO(response.content))
                    z.extractall(directory+"/"+model['name'])
                except zipfile.BadZipFile:
                    url = self.getModelUrl(model['name'], "1")
                    response = requests.get(url, stream=True)
                    z = zipfile.ZipFile(io.BytesIO(response.content))
                    z.extractall(directory+"/"+model['name'])

                time.sleep(WAIT_BETWEEN_DOWNLOADS_IN_SECONDS)
                logging.info("Sleeping for %i second(s) between file downloads.", WAIT_BETWEEN_DOWNLOADS_IN_SECONDS)

if __name__ == "__main__":
    arguments = docopt(__doc__, version='Ignition Fuel CLI Utility V1.0')
    if (arguments['--verbose']):
        logging.basicConfig(level=logging.DEBUG)
    
    logging.debug("Arguments provided: %s", json.dumps(arguments))
    fuel_util = FuelModelUtility()
    
    for model in arguments['--model']:
        logging.info("Fetching model %s.", model)
        fuel_util.getByModel(model)

    if (arguments['--query']): 
        logging.info("Collecting models from query: %s.", arguments['--query'])
        fuel_util.getByCategory(arguments['--query'])
    
    logging.debug("Complete model list: %s", fuel_util.getModelList()) 
    logging.info("Downloading zip files and extracting them into %s directory", arguments['--destination'])
    fuel_util.downloadAndExtractModels(arguments['--destination'])
    logging.info("Creating database file: %s/database.config", arguments['--destination'])
    fuel_util.createDatabaseFile(arguments['--destination'])
    logging.info("All done!")
