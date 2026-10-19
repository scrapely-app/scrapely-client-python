import logging

# Configure the Scrapely client logger
scrapely_client_logger = logging.getLogger('scrapely_client')
scrapely_client_logger.setLevel(logging.DEBUG)
scrapely_client_logger.addHandler(logging.StreamHandler())
