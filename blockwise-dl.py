"""Blockwise Website Downloader.

Example usage:

    $ python blockwise-dl.py <website-id>

Outputs:

    <username>_<website-name>_<datetime>.zip

"""

import blockwise
import sys

# Instantiate Downloader object
downloader = blockwise.downloader()

# Attempt to Download website
try:
    downloader.download(sys.argv[1])

# Throw error of sys.argv[1] is out of range.
except IndexError:
    print("Error: No website ID specified.")
