from setuptools import setup, find_packages

setup(
    name = 'doaj-harvester',
    version = '1.0.0',
    packages = find_packages(),
    install_requires = [
        "octopus==1.0.0",
        "esprit==0.0.2",
        "Flask==0.9",
        "setproctitle==1.1.10",
        "psutil==5.6.6"
    ],
    url = 'http://cottagelabs.com/',
    author = 'Cottage Labs',
    author_email = 'us@cottagelabs.com',
    description = 'External module which harvests metadata from 3rd parties and pushes the data into the DOAJ via its API',
    classifiers = [
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
