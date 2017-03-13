import urllib2

FILENAMES = ['TTM_NREL03_May2015', 'TTM_NRELvector_Jun2012', 'TTM01b_ADVbottom_NREL01_June2014',
             'TTM01_ADVtop_NREL02_June2014', 'TTM01_ADVbottom_NREL01_June2014']
URLS = ['https://mhkdr.openei.org/files/51/TTM_NREL03_May2015.VEC',
        'https://mhkdr.openei.org/files/49/AdmiraltyInlet_June2012.VEC',
        'https://mhkdr.openei.org/files/50/ttm01b_ADVbottom_NREL01_June2014.VEC',
        'https://mhkdr.openei.org/files/50/ttm01_ADVtop_NREL02_June2014.VEC',
        'https://mhkdr.openei.org/files/50/ttm01_ADVbottom_NREL01_June2014.VEC']


def download(filename, url):
    """Downloads the '.VEC' file from the internet"""
    response = urllib2.urlopen(url)
    with open('./data_cache/' + filename + '.VEC', 'wb') as f:
        f.write(response.read())

for item in zip(FILENAMES, URLS):
    print 'Starting download'
    download(item[0], item[1])
    print 'File successfully downloaded'

