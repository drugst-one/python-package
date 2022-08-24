from . import settings
import requests
import logging

class License:
    printed = False
    accepted = False

license = License()

def print_license():
    license_text = requests.get(
        f'{settings.API}/get_license',
        verify=False).json()["license"]
    logging.info(license_text)
    global license
    license.printed = True
    return

def accept_license():
    global license
    if not license.printed:
        logging.error('License needs to be read first. Call "drugstone.print_license()".')
        return
    license.accepted = True
    logging.info('License accepted.')
    return
