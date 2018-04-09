"""Blockwise Website Downloader.

Example usage:

    $ python blockwise-dl.py <website-id>

Outputs:

    <username>_<website-name>_<datetime>.zip

"""

import argparse
import blockwise
import re
import sys


# Create parser
parser = argparse.ArgumentParser(
    description="Downloads website .zip files from Blockwise.")

parser.add_argument(
    "-w", "--website", help="Attempts to deduce the website id from the given argument by itself and download it.",
)
# Add id argument
parser.add_argument(
    "--id", help="download website using website ID explicity", type=int)

# Add list argument
parser.add_argument(
    "-l", "--list", help="list websites available for download.", action="store_true")

parser.add_argument('--version', action='version', version='%(prog)s 0.1')

# Display help if no arguments are given.
# TODO: Display interactive menu if no arguments are given.
if(len(sys.argv) < 2):
    parser.print_help()
    sys.exit(0)

# Parse arguments and initialize downloader
args = parser.parse_args()
downloader = blockwise.downloader()

# Attempt to deduce website id from given argument
if(args.website):

    # Init website id
    website_id = None

    # If the argument is a digit, assume it is an id
    if(args.website.isdigit()):
        website_id = args.website

    # Else, assume it is a blockwise link and extract the website id from it
    else:
        website_id = re.search(
            r'^(https://)?(start\.)?(blockwi\.se/websites/)(\d+)(/pages)', args.website).group(4)

    # Download website
    downloader.download(website_id)

# Download website by ID if --id is set
if(args.id):
    downloader.download(args.id)

# List websites if set
if(args.list):
    downloader.list_websites()
