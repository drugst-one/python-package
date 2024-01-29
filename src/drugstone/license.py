import requests
import logging
from .scripts.constants.url import api

class license:
    printed = False
    accepted = False

license = license()

def print_license():
    license_text = requests.get(
        f'{api.BASE}get_license',
        verify=False).json()["license"]
    logging.info(license_text)
    global license
    license.printed = True
    return

def accept_license():
    global license
    if not license.printed:
        logging.error('license needs to be read first. Call "drugstone.print_license()".')
        return
    license.accepted = True
    logging.info('license accepted.')
    return
