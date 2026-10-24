# Derived from apify-client-python (docs/02_concepts/code/06_logging_config.py), Copyright Apify Technologies s.r.o., Apache License 2.0. Modified by TeraShift GmbH.
import logging

# Configure the Scrapely client logger
scrapely_client_logger = logging.getLogger('scrapely_client')
scrapely_client_logger.setLevel(logging.DEBUG)
scrapely_client_logger.addHandler(logging.StreamHandler())
