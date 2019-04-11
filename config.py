

# configuration for accessing solr db
# these values can be overwritten by local_config values
# maximum number of records that can be fetched by bigquery is for now 2000
# this can be overwritten to become smaller but it cannot become larger
EXPORT_SOLRQUERY_URL = "https://api.adsabs.harvard.edu/v1/search/bigquery"
EXPORT_SERVICE_ADSWS_API_TOKEN = 'this is a secret api token!'
EXPORT_SERVICE_MAX_RECORDS_SOLR = 2000

# these are used for linkout links
EXPORT_SERVICE_FROM_BBB_URL = 'https://ui.adsabs.harvard.edu/abs'
EXPORT_SERVICE_RESOLVE_URL = "https://ui.adsabs.harvard.edu/link_gateway"

# added to the end of bibTex
EXPORT_SERVICE_ADS_NOTES = 'Provided by the SAO/NASA Astrophysics Data System'

# Journal Abbreviations used in the ADS BibTeX entries
# From http://adsabs.harvard.edu/abs_doc/aas_macros.html
# Journal name   TeX macro
EXPORT_SERVICE_AASTEX_JOURNAL_MACRO = [
    ['Astronomical Journal',r'\aj'],
    ['Acta Astronomica',r'\actaa'],
    ['Annual Review of Astron and Astrophys',r'\araa'],
    ['Astrophysical Journal',r'\apj'],
    ['Astrophysical Journal, Letters',r'\apjl'],
    ['Astrophysical Journal, Supplement',r'\apjs'],
    ['Applied Optics',r'\ao'],
    ['Astrophysics and Space Science',r'\apss'],
    ['Astronomy and Astrophysics',r'\aap'],
    ['Astronomy and Astrophysics Reviews',r'\aapr'],
    ['Astronomy and Astrophysics, Supplement',r'\aaps'],
    ['Astronomicheskii Zhurnal',r'\azh'],
    ['Bulletin of the AAS',r'\baas'],
    ['Chinese Astronomy and Astrophysics',r'\caa'],
    ['Chinese Journal of Astronomy and Astrophysics',r'\cjaa'],
    ['Icarus',r'\icarus'],
    ['Journal of Cosmology and Astroparticle Physics',r'\jcap'],
    ['Journal of the RAS of Canada',r'\jrasc'],
    ['Memoirs of the RAS',r'\memras'],
    ['Monthly Notices of the RAS',r'\mnras'],
    ['Monthly Notices of the Royal Astronomical Society',r'\mnras'],
    ['New Astronomy',r'\na'],
    ['New Astronomy Review',r'\nar'],
    ['Physical Review A: General Physics',r'\pra'],
    ['Physical Review B: Solid State',r'\prb'],
    ['Physical Review C',r'\prc'],
    ['Physical Review D',r'\prd'],
    ['Physical Review E',r'\pre'],
    ['Physical Review Letters',r'\prl'],
    ['Publications of the Astron. Soc. of Australia',r'\pasa'],
    ['Publications of the ASP',r'\pasp'],
    ['Publications of the ASJ',r'\pasj'],
    ['Revista Mexicana de Astronomia y Astrofisica',r'\rmxaa'],
    ['Quarterly Journal of the RAS',r'\qjras'],
    ['Sky and Telescope',r'\skytel'],
    ['Solar Physics',r'\solphys'],
    ['Soviet Astronomy',r'\sovast'],
    ['Space Science Reviews',r'\ssr'],
    ['Zeitschrift fuer Astrophysik',r'\zap'],
    ['Nature',r'\nat'],
    ['IAU Cirulars',r'\iaucirc'],
    ['Astrophysics Letters',r'\aplett'],
    ['Astrophysics Space Physics Research',r'\apspr'],
    ['Bulletin Astronomical Institute of the Netherlands',r'\bain'],
    ['Fundamental Cosmic Physics',r'\fcp'],
    ['Geochimica Cosmochimica Acta',r'\gca'],
    ['Geophysics Research Letters',r'\grl'],
    ['Journal of Chemical Physics',r'\jcp'],
    ['Journal of Geophysics Research',r'\jgr'],
    ['Journal of Quantitiative Spectroscopy and Radiative Transfer',r'\jqsrt'],
    ['Mem. Societa Astronomica Italiana',r'\memsai'],
    ['Nuclear Physics A',r'\nphysa'],
    ['Physics Reports',r'\physrep'],
    ['Physica Scripta',r'\physscr'],
    ['Planetary Space Science',r'\planss'],
    ['Proceedings of the SPIE',r'\procspie'],
]

# For SoPh format:
# First element is the journal abbreviation to be output,
# second one is the bibstem to which it applies.
EXPORT_SERVICE_SOPH_JOURNAL_ABBREVIATION = {
    'A&A..': 'Astron. Astroph.',
    'ApJ..': 'Astrophys. J.',
    'SoPh.': 'Solar Phys.',
    'GeoRL': 'Geophys. Res. Lett.',
    'JGRA.': 'J.Geophys. Res. A',
    'JGRB.': 'J.Geophys. Res. B',
    'JGRC.': 'J.Geophys. Res. C',
    'JGRD.': 'J.Geophys. Res. D',
    'JGRE.': 'J.Geophys. Res. E',
}


# Testing Bibcode for GET
EXPORT_SERVICE_TEST_BIBCODE_GET = 'TEST..BIBCODE..GET.'