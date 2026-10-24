# Derived from apify-client-python (docs/02_concepts/code/06_logging_formatter.py), Copyright Apify Technologies s.r.o., Apache License 2.0. Modified by TeraShift GmbH.
import logging

# Create a custom logging formatter. Reference only the properties present
# on every record. Properties attached to some records only, such as
# `status_code`, would raise an error for the records that lack them.
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s - '
    '%(client_method)s - %(attempt)s - %(url)s'
)

handler = logging.StreamHandler()
handler.setFormatter(formatter)

# Configure the Scrapely client logger to use the custom formatter
scrapely_client_logger = logging.getLogger('scrapely_client')
scrapely_client_logger.setLevel(logging.DEBUG)
scrapely_client_logger.addHandler(handler)
