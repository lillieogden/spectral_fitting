from __future__ import print_function
import urllib2
from os.path import isfile

FILENAMES = ['TTM_NREL03_May2015',
             'TTM_NRELvector_Jun2012',
             'TTM01b_ADVbottom_NREL01_June2014',
             'TTM01_ADVtop_NREL02_June2014',
             'TTM01_ADVbottom_NREL01_June2014']

base_url = 'https://mhkdr.openei.org/files/'

URLS = ['51/TTM_NREL03_May2015.VEC',
        '49/AdmiraltyInlet_June2012.VEC',
        '50/ttm01b_ADVbottom_NREL01_June2014.VEC',
        '50/ttm01_ADVtop_NREL02_June2014.VEC',
        '50/ttm01_ADVbottom_NREL01_June2014.VEC']


def download(filename, url):
    """Downloads the '.VEC' file from the internet"""
    response = urllib2.urlopen(url)
    full_filename = './data_cache/' + filename + '.VEC'
    if not isfile(full_filename):
        print("Downloading file {}...".format(filename), end='')
        with open(full_filename, 'wb') as f:
            f.write(response.read())
        print("success.")
    else:
        print("File, '{}', already exists.".format(filename))

for item in zip(FILENAMES, URLS):
    download(item[0], base_url + item[1])
