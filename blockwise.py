"""Blockwise Website Downloader."""

import json
import mechanicalsoup
import os
import re


class downloader:
    """Object containing the Browser and the methods to login into Blockwise and download the website given website"""
    browser = mechanicalsoup.StatefulBrowser()
    config = None

    def __init__(self):
        """Constructor. Loads the config file and logs in the user."""
        self.load_config()
        self.login()

    def download(self, website_id):
        """Downloads the website zip for the given id."""

        print("Attempting to download website with id: " +
              str(website_id))

        # Construct download URL
        download_url = self.config["base_url"] + "websites/" + \
            str(website_id) + "/pages/?action=download-confirm"

        # Open download page / popup
        self.browser.open(download_url)

        # Select download form
        self.browser.select_form(
            'form[action="/websites/' + str(website_id) + '/pages/?action=download"]')

        # Submit form and download contents
        response = self.browser.submit_selected()
        self.save_file(response)

    def list_websites(self):
        """Returns a list of websites associated with this account"""
        print("Listing websites... (NOT IMPLEMENTED YET)")
        return

    def load_config(self):
        """Loads config.json from the same directory as this script."""
        with open('config.json', 'r') as f:
            self.config = json.load(f)

    def login(self):
        """Login the user onto the Blockwise site."""

        # Open browser with the login URL
        self.browser.open(self.config["base_url"] + "login")

        # Select the login form
        self.browser.select_form('form[action="/login/"]')

        # Fill the login form.
        self.browser["email"] = self.config["email"]
        self.browser["password"] = self.config["password"]

        # Submit form
        self.browser.submit_selected()

    def save_file(self, response):
        """Saves the .zip file in the HTTP response locally"""
        # Extract filename from response url
        filename = re.search('[^/]+(?=/$|$)', response.url).group(0)

        # Prepend download folder name to the filename
        filename = self.config["folder"] + filename
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        # Write contents to file
        with open(filename, 'wb') as f:
            f.write(response.content)

        # Print message displaying the absolute filepath for convenience
        print("Downloaded file to " + os.path.abspath(filename))
