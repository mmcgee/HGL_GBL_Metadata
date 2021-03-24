import os.path
import arcpy
from arcpy import env

# Dani - Set this to the path of the folder where your JP2's are
# The GeoTiffs will go here too for now but that's easy to change.
env.workspace = "C:\Users\azd289\Harvard University\HGL Library - Documents\General\HGL_Ingest\onDeck\begin_july2"


# Get the projection code of an image file on disk
def findProjections(aLayer):

    # Describe the image
    desc = arcpy.Describe(aLayer)
    dataType = desc.dataType

    if dataType != "RasterDataset":
        print("[WARNING] Incorrect data type found for: " + aLayer + " Skipping...")
        return 0

    WKIDCode = 1
    GCSCode = desc.spatialReference.GCSCode
    PCSCode = desc.spatialReference.PCSCode
    WKIDCode = PCSCode

    if PCSCode == 0:
        WKIDCode = GCSCode

    if WKIDCode == 54001:
        print("[WARNING] Incorrect projection code (54001) found for LAYER: " + aLayer + " Skipping it...")
        return 0

    return WKIDCode

# Dani - Put the name(s) of the file(s) that are in env.workspace that you want to project here.
# Use a comma after each file name except for the last. If there is only one file, than no comma
# is needed.
layerList = [
    # use this format for file names: 'file1.jp2',


    'G3701_A9_1881_R3_VF.jp2'


]

# Script starting point
for name in layerList:
    jp2FileName = name
    fullDataPath = env.workspace + "/" + jp2FileName

    # New file name for GeoTiff
    geoTiffFileName = jp2FileName[0:jp2FileName.find('.jp2')]
    newFilePath = env.workspace + "/" + geoTiffFileName + "_orig.tif"

    if os.path.exists(env.workspace + "/" + name):
        # Get the Well known ID of the JP2 image
        WKIDCode = findProjections(fullDataPath)
        if WKIDCode != 0:
            print("Projecting....")
            # Set the spatial reference to EPSG of JP2K
            sr = arcpy.SpatialReference(WKIDCode)
            print("WKIDCode of " + name + " is: ", WKIDCode)
            arcpy.ProjectRaster_management(fullDataPath, newFilePath, sr)
    else:
        print("[ERROR] File: " + name + " does not exist. Skipping...")



print("Finished converting...")
