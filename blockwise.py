"""Blockwise Website Downloader."""

import json
import mechanicalsoup
import re


class downloader:
    """Object containing the Browser and the methods to login into Blockwise and Download the website"""
    browser = mechanicalsoup.StatefulBrowser()

    config = None
    website_id = None

    def __init__(self):
        """Constructor. Loads config.json"""

        # Load config.json
        with open('config.json', 'r') as f:
            self.config = json.load(f)

    def login(self):
        """Login the user on the Blockwise site."""

        # Open browser with the login URL
        print("Connecting to: " + self.config["login_url"])
        self.browser.open(self.config["login_url"])

        # Select the login form
        self.browser.select_form('form[action="/login/"]')

        # Fill the login form.
        print("Attempting to login with email address: " +
              self.config["email"])
        self.browser["email"] = self.config["email"]
        self.browser["password"] = self.config["password"]

        # Submit form
        self.browser.submit_selected()

    def open_website_page(self):
        """Opens the website page for the given id"""

        # Construct Website url
        website_url = "https://start.blockwi.se/websites/" + \
            str(self.website_id) + "/pages/"

        # Open Website page
        print("Attempting to open website page with id: " + str(self.website_id))
        self.browser.open(website_url)

    def download_website(self):
        """Downloads the website zip for the given id."""

        print("Attempting to download website with id: " +
              str(self.website_id))

        # Construct download URL
        download_url = "https://start.blockwi.se/websites/" + \
            str(self.website_id) + "/pages/?action=download-confirm"

        # Open download page / popup
        self.browser.open(download_url)

        # Select download form
        self.browser.select_form(
            'form[action="/websites/' + str(self.website_id) + '/pages/?action=download"]')

        # Submit form and download contents
        response = self.browser.submit_selected()

        # Extract filename from response url
        filename = re.search('[^/]+(?=/$|$)', response.url).group(0)

        # Write contents to file
        with open(filename, 'wb') as f:
            f.write(response.content)

        print("Downloaded " + filename)

    def download(self, website_id):

        # Set website id
        self.website_id = website_id

        # Login, open website page and download website zip
        self.login()
        self.open_website_page()
        self.download_website()
