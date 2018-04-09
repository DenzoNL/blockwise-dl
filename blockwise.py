"""Blockwise Website Downloader."""

import json
import mechanicalsoup
import os
import re


class downloader:
    """Object containing the Browser and the methods to login into Blockwise and download the website given website"""
    browser = mechanicalsoup.StatefulBrowser()
    config = None
    website_list = []

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

    def download_all(self):
        """Downloads all websites from the configured account."""
        # Fetch website list
        self.fetch_website_list()

        for website in self.website_list:
            self.download(website['id'])

    def fetch_website_list(self):
        """Fetches the list of websites attached to the configured Blockwise account."""
        # Clear list
        self.website_list = []

        # Open websites overview
        self.browser.open(self.config["base_url"] + "websites")

        # Find table and iterate over rows
        for table_row in self.browser.get_current_page().select("table tr"):

            # Fetch cells
            cells = table_row.findAll('td')

            # Iterate over cells
            if(len(cells) > 0):

                # Get website ID
                website_id = table_row['data-id']
                # Get website name
                name = cells[1].text.strip()
                # Get website domain name
                domain = cells[2].text.strip()

                # Build website object
                website = {'id': website_id,
                           'name': name, 'domain': domain}

                # Add website object to list
                self.website_list.append(website)

    def get_website_id_by_domain(self, domain):
        """Returns the website id for a given domain name."""

        # Fetch website list
        self.fetch_website_list()

        # Loop through website list
        for website in self.website_list:
            if(domain == website['domain']):
                return website['id']

    def list_websites(self):
        """Prints a list of websites associated with this account."""

        # Fetch websites
        self.fetch_website_list()

        # Print website data
        for website in self.website_list:
            print("ID: {0} | Domain: {1} | Name: {2}".format(
                website['id'], website['domain'], website['name']))

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
