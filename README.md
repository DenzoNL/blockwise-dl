# blockwise-dl

`blockwise-dl` downloads websites in .zip format from the Blockwise management portal.

WARNING: This software is not production-ready.

### Dependencies

`blockwise-dl` requires `Python 3` and  `MechanicalSoup`

You can install `Python` from the official website or use your favorite package manager.
You can install `MechanicalSoup` by running the following command:

```console
$ pip install MechanicalSoup
```

### Setup

`blockwise-dl` requires a valid Blockwise account, with credentials entered into `config.json`.
To setup `config.json`, follow these instructions:

```console
$ mv config.example.json config.json
```
Then, open up `config.json` with your favorite text editor and replace the `email` and `password` values with your own credentials.

All done!

### Usage

By passing `-w WEBSITE` as an argument, `blockwise-dl` attempts to deduce the website ID itself from the argument.
`WEBSITE` can currently be a link to the website inside Blockwise's back-end, e.g. `https://start.blockwi.se/websites/<id>/pages/`
or simply the website ID. In the future it will also support deducing ID's by domain name.

```console
usage: blockwise-dl.py [-h] [-w WEBSITE] [--id ID] [--version]

Downloads website .zip files from Blockwise.

optional arguments:
  -h, --help            show this help message and exit
  -w WEBSITE, --website WEBSITE
                        Attempts to figure out the website id from the given
                        argument by itself and download it.
  --id ID               download website using website ID explicity
  --version             show program's version number and exit

```

### TODO:

* Add proper error/exception handling.
* Refactoring
* Add support for downloading sites by domain name rather than website ID.
* Add support for interactively downloading websites, by displaying a menu of websites.

### Disclaimer

I am in no shape or form associated with Blockwise. I can not be held responsible for any consequences resulting from usage of this software.
