import os.path
import arcpy
from arcpy import env

# Dani - Set this to the path of the folder where your JP2's are
# The GeoTiffs will go here too for now but that's easy to change.
env.workspace = "C:/Users/dab5140/Dropbox/Work/Harvard/HGL_Ingest/onDeck/OnSite2011MAPC2"

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

    'G3761_A4_1985_J3.jp2',
    'G3761_Q44_2000_M4.jp2',
    'G3762_H23G45_1995_M4.jp2',
    'G3762_P54G4_1996_P5.jp2',
    'G3763_M5G45_1995_M4.jp2',
    'G3764_B62J3G455_1979_H6.jp2',
    'G3764_B6A1_1980_M4.jp2',
    'G3764_B6G4_1997_M4.jp2',
    'G3764_B6G4_1997_M41.jp2',
    'G3764_B6G4_1997_M42.jp2',
    'G3764_B6G5_1991_M4_SH1.jp2',
    'G3764_B6G5_1991_M4_SH2.jp2',
    'G3764_B6G5_1991_M4_SH3.jp2',
    'G3764_B6G5_1991_M4_SH4.jp2',
    'G3764_B6G5_1991_M4_SH5.jp2',
    'G3764_B6G5_1991_M4_SH6.jp2',
    'G3764_B6G5_1991_M4_SH7.jp2',
    'G3764_B6P1_2000_M4.jp2',
    'G3764_C2E63_1980_C3.jp2',
    'G3764_C2E73_1980_C3.jp2',
    'G3764_C2E73_1983_C3.jp2',
    'G3764_C2F7_1978_C3.jp2',
    'G3764_C2G45_1981_C3.jp2',
    'G3764_C2_1976_C21.jp2',
    'G3764_C32_1967_F6.jp2',
    'G3764_C3G44_1998_M4.jp2',
    'G3764_C3_1972_C3.jp2',
    'G3764_D25_1981_J6.jp2',
    'G3764_G4_1962_G5.jp2',
    'G3764_H26_1979_M3.jp2',
    'G3764_H742G5_1996_M41_1.jp2',
    'G3764_H742G5_1996_M41_2.jp2',
    'G3764_H742G5_1996_M41_3.jp2',
    'G3764_H742G5_1996_M41_4.jp2',
    'G3764_H742G5_1996_M41_5.jp2',
    'G3764_H742_1970_M3.jp2',
    'G3764_I62_1975_J6.jp2',
    'G3764_M23_1872_D2_1979.jp2',
    'G3764_M23_1979_M3.jp2',
    'G3764_M76_1980_G8.jp2',
    'G3764_M84_1989_M5.jp2',
    'G3764_N6G45_1983_E4.jp2',
    'G3764_N777_1982_N6.jp2',
    'G3764_N87_1972_J3.jp2',
    'G3764_N9_1989_N6.jp2',
    'G3764_R3_1973_R4.jp2',
    'G3764_R4_1975_R4.jp2',
    'G3764_R65_1976_P4.jp2',
    'G3764_S2_1963_S3.jp2',
    'G3764_S852_1978_S9_FRONT.jp2',
    'G3764_S852_1980_S9_FRONT.jp2',
    'G3764_W2F7_1977_W3.jp2',
    'G3764_W342_1980_W3.jp2',
    'G3764_W38_1979_W4.jp2',
    'G3764_W86_1978_W6.jp2'

]

# Script starting point
for name in layerList:
    jp2FileName = name
    fullDataPath = env.workspace + "/" + jp2FileName

    if os.path.exists(env.workspace + "/" + name):
        # Get the Well known ID of the JP2 image
        WKIDCode = findProjections(fullDataPath)
        if WKIDCode != 0:
            print("Projecting....")
            # Set the spatial reference to EPSG of JP2K
            sr = arcpy.SpatialReference(WKIDCode)
            print("WKIDCode of " + name + " is: ", WKIDCode)
    else:
        print("[ERROR] File: " + name + " does not exist. Skipping...")



print("Finished")
