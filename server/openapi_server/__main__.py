#!/usr/bin/env python3

import connexion
import logging
from configparser import ConfigParser
from hubmap_commons.hm_auth import AuthHelper

from openapi_server import encoder

neo4jManager = Neo4jManager()
logger = logging.getLogger('connexion.app')

# Initialize AuthHelper class and ensure singleton
try:
    if AuthHelper.isInitialized() == False:
        config = ConfigParser()
        config.read('openapi_server/resources/app.properties')
        neo4j_config = config['globus']
        # [globus]
        # APP_CLIENT_ID = 'a UUID'
        # APP_CLIENT_SECRET = 'a secret'
        app_client_id = neo4j_config.get('APP_CLIENT_ID')
        app_client_secret = neo4j_config.get('APP_CLIENT_SECRET')

        auth_helper_instance = AuthHelper.create(app_client_id, app_client_secret)
        logger.info("Initialized AuthHelper class successfully :)")
    else:
        auth_helper_instance = AuthHelper.instance()
except Exception:
    msg = "Failed to initialize the AuthHelper class"
    # Log the full stack trace, prepend a line with our message
    logger.exception(msg)


def main():
    app = connexion.App(__name__, specification_dir='./openapi/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('openapi.yaml',
                arguments={'title': 'Ontology API'},
                pythonic_params=True)
    logger.info("API added successfully")
    app.run(port=8080)


if __name__ == '__main__':
    main()
