from __future__ import print_function
import pysolr

# Setup a Solr instance. The timeout is optional.
solr = pysolr.Solr('http://pelham.lib.harvard.edu:8983/solr/ogp/', timeout=10)

aName = 'HARVARD.SDE.USGS15MA_ABINGTON_1893'
results = solr.search("LayerId:" + '"' + aName + '"')

# Loop over the results.
for result in results:
    print("The LayerDisplayName is '{0}'.".format(result['LayerDisplayName']))