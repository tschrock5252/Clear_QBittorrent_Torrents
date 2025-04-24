#!/usr/bin/env python3
import sys
import json
import requests
import logging
import argparse
import urllib3

# Disable warnings for self-signed certs if --insecure is used
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Credentials (can be moved to env vars or config file)
USERNAME = "Tyler"
PASSWORD = "tschrock52"
DEFAULT_BASEURL = 'https://10.1.0.125:8282/'

# Parse CLI arguments
parser = argparse.ArgumentParser()
parser.add_argument('-b', '--baseurl', default=DEFAULT_BASEURL, help='Base URL to qBittorrent (default: https://10.1.0.125:8443/)')
parser.add_argument('-v', '--verbose', action="store_true", help='Enable verbose logging')
parser.add_argument('-d', '--debug', action="store_true", help='Dry run — no deletion (implies verbose)')
parser.add_argument('--insecure', action="store_true", help='Disable SSL certificate verification (for self-signed certs)')
args = parser.parse_args()

# Configure logging
logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s] %(message)s")
logger = logging.getLogger()
streamHandler = logging.StreamHandler(sys.stdout)
streamHandler.setFormatter(logFormatter)
logger.addHandler(streamHandler)
logger.setLevel(logging.DEBUG if (args.verbose or args.debug) else logging.INFO)

testmode = args.debug
verify_ssl = not args.insecure

# Set up session for persistent login
session = requests.Session()
headers = {'Content-Type': 'application/x-www-form-urlencoded'}

# Step 1: Login
login_url = args.baseurl.rstrip('/') + '/api/v2/auth/login'
login_data = {
    'username': USERNAME,
    'password': PASSWORD
}

try:
    logger.debug(f"Attempting login with SSL verification: {verify_ssl}")
    login_response = session.post(login_url, data=login_data, headers=headers, verify=verify_ssl)
    if login_response.status_code != 200 or 'ok' not in login_response.text.lower():
        logger.error(f'Login failed: {login_response.status_code} - {login_response.text}')
        sys.exit(1)
    logger.debug('Login successful.')
except requests.exceptions.RequestException as err:
    logger.error('Login error: ' + str(err))
    sys.exit(1)

# Step 2: Fetch completed torrents
try:
    info_url = args.baseurl.rstrip('/') + '/api/v2/torrents/info?filter=completed'
    response = session.get(info_url, verify=verify_ssl)
    response.raise_for_status()
    torrents = response.json()

    if not torrents:
        logger.info('No completed torrents found.')
        sys.exit(0)

    for tor in torrents:
        name = tor['name']
        state = tor['state']
        hash_ = tor['hash']
        category = tor.get('category', '')
        logger.info(f"Found completed torrent: {name} [{state}]")

        delete_url = args.baseurl.rstrip('/') + '/api/v2/torrents/delete'
        delete_data = {
            'hashes': hash_,
            'deleteFiles': False
        }

        if not testmode:
            try:
                delete_response = session.post(delete_url, data=delete_data, verify=verify_ssl)
                delete_response.raise_for_status()
                logger.info(f"Deleted torrent: {name}")
            except requests.exceptions.RequestException as err:
                logger.error(f"Failed to delete {name}: {err}")
        else:
            logger.debug(f"[DEBUG] Would delete torrent: {name}")
except requests.exceptions.RequestException as err:
    logger.error('Error fetching torrents: ' + str(err))
    sys.exit(1)

