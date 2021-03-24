__author__ = 'des451'

import re
import pysolr
import HGLUtils

#
# This script adds an OGP2 compliant Solr record to a local instance of Solr (testing) or to the PRD on pelham
# It also generates an FGDC.xml file that's used to import into Oracle to support data download and layer tracking
#

Name = 'G8460_1891_S8'   # This needs to come from the LayerId
ExternalLayerId = 1430       # This needs to come from the Database - PUBID

# Path to specify where the FGDC.xml input file is stored
inputPath = 'C:/Users/dab5140/Desktop/HGL_Ingest/moveToServer/'
# Path to specify where the output file (for the DBMS) should go
outDbmsFilePath = 'C:/Users/dab5140/Desktop/HGL_Ingest/moveToServer/new_xml/'

# End input parameters


# Full path to FGDC file
inFgdcFile = inputPath+Name+'.xml'

# Some FGDC files have line breaks, some do not. Get rid of them if they are there
with open(inFgdcFile) as fin:
    rawMetadata = ''.join(e.strip('\n') for e in  fin)

fin.close()

# Format the input file's header
metadata = HGLUtils.changeFGDCHeader(rawMetadata)
# metadataToParse = re.sub(r"\> + \<", "><", metadata)
# print("Formatted FGDC text: ", metadata)

#
# Set LayerDisplayName from first <title>
#
start = metadata.find("<title>")
end = metadata.find("</title>")
title = metadata[start+7:end]
# LayerDisplayName = 'AGIS Northern Georgia, ca. 1864 (Raster Image)' # This needs to come from the FGDC
LayerDisplayName = title
print('The Title for data set ' + Name + ' is: ' + title)

Access = 'Public'                                                   # This needs to come from the Database
DataType = 'Paper Map'                                              # This needs to come from the FGDC
WorkspaceName = 'cite'
LayerId = 'HARVARD.SDE2.'+ Name

#
# Set the Geoserver Location field based on the DataType of the layer getting published
#
# "DataType": "Polygon", 'Point', 'Line'
vectorLoc = '{"wms": ["http://hgl.harvard.edu:8190/geoserver/wms"],"wfs": "http://hgl.harvard.edu:8190/geoserver/wfs"}'
# "DataType": "Paper Map",'Scanned Map', 'Raster'
rasterLoc = '{"wms": ["http://hgl.harvard.edu:8190/geoserver/wms"],"wcs": "http://hgl.harvard.edu:8190/geoserver/wcs","download": "http://hgl.harvard.edu:8080/HGL/HGLOpenDelivery"}'

# Going to need Access check soon where the open port is 8190 and restricted is 8090
vectorLocForFile = '{\\\"wms\\": [\\"http://hgl.harvard.edu:8190/geoserver/wms\\"],\\"wfs\\": \\"http://hgl.harvard.edu:8190/geoserver/wfs\\"}'
rasterLocForFile = '{\\\"wms\\": [\\"http://hgl.harvard.edu:8190/geoserver/wms\\"],\\"wcs": \\"http://hgl.harvard.edu:8190/geoserver/wcs\\",\\"download\\": \\"http://hgl.harvard.edu:8080/HGL/HGLOpenDelivery\\"}'

if DataType == "Paper Map" or DataType == "Scanned Map" or DataType == "Raster":
    fileLocation = rasterLocForFile
    solrLocation = rasterLoc
else:
    fileLocation = vectorLocForFile
    solrLocation = vectorLoc

#
# ContentDate is tricky. Could come from 2 different places: <caldate> or <begdate>
#  <caldate> can have 1+ occurances.
#  Has to be formatted
#
# SRC 1:    <timeinfo><sngdate><caldate>1890</caldate></sngdate></timeinfo>
contentDateStr = ''
contentDate = re.findall(r'<sngdate><caldate>(.*?)</caldate></sngdate>',metadata)

for i in contentDate:
    if i != "":
        contentDateStr += i
        break

solrContentDateStr = HGLUtils.createSolrDate(contentDateStr)

#
# Abstract
#
abstractStr = ''
abstract = re.findall(r'abstract>(.*?)</abstract',metadata)

for i in abstract:
    abstractStr += i

#
# Bounding coordinates
#
start = metadata.find("<westbc>")
end = metadata.find("</westbc>")
westbc = metadata[start+8:end]

start = metadata.find("<eastbc>")
end = metadata.find("</eastbc>")
eastbc = metadata[start+8:end]

start = metadata.find("<northbc>")
end = metadata.find("</northbc>")
northbc = metadata[start+9:end]

start = metadata.find("<southbc>")
end = metadata.find("</southbc>")
southbc = metadata[start+9:end]

centerX = (float(eastbc) + float(westbc)) / 2
centerY = (float(northbc) + float(southbc)) / 2
halfWidth = abs(float(eastbc) - float(westbc)) / 2
halfHeight = abs(float(northbc) - float(southbc)) / 2
area = (halfHeight * 2.) * (halfWidth * 2)

#
# Get the <themekey> elements
#
allThemeKeys = ''
themeKeys = re.findall(r'themekey>(.*?)</themekey',metadata)

for i in themeKeys:
    allThemeKeys += ' '
    allThemeKeys += i.replace(',','')

#
# Get the <placekey> elements
#
allPlaceKeys = ''
placeKeys = re.findall(r'placekey>(.*?)</placekey',metadata)

for i in placeKeys:
    allPlaceKeys += ' '
    allPlaceKeys += i.replace(',','')

#
# Publisher from <publish> -- First occurance in FGDC
#
publisherStr = ''
publisher = re.findall(r'<publish>(.*?)</publish>',metadata)
publisherStr = publisher[0]

#
# Originator from <cntorg>, first occurance in FGDC
#
originatorStr = ''
originator = re.findall(r'<cntorgp><cntorg>(.*?)</cntorg></cntorgp>',metadata)
originatorStr = originator[0]

GeoReferenced = True

# Specify local or PRD destination
#solr = pysolr.Solr('http://localhost:8983/solr/ogp/', timeout=10)
solr = pysolr.Solr('http://pelham.lib.harvard.edu:8983/solr/ogp/', timeout=10)

# If the record already exists, delete it...
        #   This is not added correctly
        # "ExternalLayerId": '\"'+str(ExternalLayerId)+'\"', = "ExternalLayerId": "\"939\"",

solr.add([
      {
        "LayerId": LayerId,
        "Name": Name,
        "CollectionId": "initial collection",
        "ExternalLayerId": str(ExternalLayerId), # = "ExternalLayerId": "939",
        "Institution": "Harvard",
        "Access": Access,
        "DataType": DataType,
        "Availability": "online",
        "LayerDisplayName": LayerDisplayName,
        "Publisher": publisherStr,
        "Originator": originatorStr,
        "ThemeKeywords": allThemeKeys,
        "PlaceKeywords": allPlaceKeys,
        "GeoReferenced": "true",
        "Abstract": abstractStr,
        "Location": solrLocation,
        "MaxY": northbc,
        "MinY": southbc,
        "MaxX": eastbc,
        "MinX": westbc,
        "CenterX": centerX,
        "CenterY": centerY,
        "HalfWidth": halfWidth,
        "HalfHeight": halfHeight,
        "Area": area,
        "FgdcText": metadata,
        "WorkspaceName": WorkspaceName,
        "Institution": "Harvard",
        "Availability": "online",
        "GeoReferenced": "true",
        "ContentDate": solrContentDateStr
      }
    ])

solr.commit()
# You can optimize the index when it gets fragmented, for better speed.
# solr.optimize()

# Create the FGDC file to import into Oracle -- removes: <!DOCTYPE metadata SYSTEM.... in header
met4DBMS = HGLUtils.changeFGDCHeaderForDBMS(metadata)
fdb = open(outDbmsFilePath+Name+'-DB.xml', 'w')
fdb.write(met4DBMS)
fdb.close()

print("End...")
