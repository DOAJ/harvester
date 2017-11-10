# DOAJ Harvester

An external module which harvests metadata from 3rd parties and adds it to the DOAJ via the API

## Installation

Clone the project:

    git clone https://github.com/doaj/harvester.git

get all the submodules

    cd myapp
    git submodule init
    git submodule update

This will initialise and clone the esprit and magnificent octopus libraries

Then get the submodules for Magnificent Octopus

    cd myapp/magnificent-octopus
    git submodule init
    git submodule update

Create your virtualenv and activate it

    virtualenv /path/to/venv
    source /path/tovenv/bin/activate

Install esprit and magnificent octopus (in that order)

    cd myapp/esprit
    pip install -e .
    
    cd myapp/magnificent-octopus
    pip install -e .
    
Create your local config

    cd myapp
    touch local.cfg

Then you can override any config values that you need to

To start the application, you'll also need to install it into the virtualenv just this first time

    cd myapp
    pip install -e .

Then, start your app with

    python service/web.py

If you want to specify your own root config file, you can use

    APP_CONFIG=path/to/rootcfg.py python service/web.py
    
## Running the Harvester

First you need to configure the runner, which means in local.cfg to put the list of accounts
and their API keys in the API_KEYS property:

    API_KEYS = {
        "11112222" : "kjsdhjf98qr82oif293pJUWEF",
        "22223333" : "OIWEFWOIJEFIWLKSDLKFJIOWE"
    }

You also need to set a suitable initial harvest date.  Too far in the past and you'll be wasting time
(and EPMC resources), but too near and you'll miss things you want.  The default has been set to the start
of December 2015 - you will probably want a much longer date than that initially.

    INITIAL_HARVEST_DATE = "2015-12-01T00:00:00Z"

Then you just need to start the harvester with:

    python service/runner.py
    
This will run through each account id in the API_KEYS list, and for each one retrieve the ISSNs from
the DOAJ, then request the articles for each of those ISSNs from EPMC, and fire it over to the DOAJ
(authenticating with that account's API key).

## Rotating the logs

The harvester creates a fair amount of log output, so it's best to rotate and archive old logs using ```logrotate```.
Symlink the config from ```deploy/logrotate/doaj-harvester``` into the logrotate directory at ```/etc/logorotate.d/``` and
it will be picked up on the next cron.daily run of logrotate. E.g:

    ﻿sudo ln -s /full/path/to/deploy/logrotate/doaj-harvester /etc/logrotate.d/doaj-harvester
