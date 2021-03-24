__author__ = 'des451'


#  change <?xml version=\"1.0\" encoding=\"UTF-8\"?><!DOCTYPE metadata SYSTEM \"http://www.fgdc.gov/metadata/fgdc-std-001-1998.dtd\"><metadata>
# TO: <?xml version = '1.0' encoding = 'UTF-8'?><metadata>
def changeFGDCHeader(metadata):

    start = metadata.find("<metadata>")
    met1 = metadata[start:]

    # If you need: <?xml version = "1.0" encoding = "UTF-8"?>
    # met2 = '<?xml version = "1.0" encoding = "UTF-8"?>'

    # If you need: <?xml version = '1.0' encoding = 'UTF-8'?>
    # met2 = "<?xml version = '1.0' encoding = 'UTF-8'?>"

    # If you need <?xml version=\"1.0\" encoding=\"ISO-8859-1\"?><!DOCTYPE metadata SYSTEM \"http://www.fgdc.gov/metadata/fgdc-std-001-1998.dtd\">
    met2 = '<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?><!DOCTYPE metadata SYSTEM \"http://www.fgdc.gov/metadata/fgdc-std-001-1998.dtd\">'

    # Tufts <?xml version=\"1.0\" encoding=\"ISO-8859-1\"?><!DOCTYPE metadata SYSTEM \"http://www.fgdc.gov/metadata/fgdc-std-001-1998.dtd\"><metadata>
    # This is the same as my FGDC1 before it goes into Solr
    met3 = "<?xml version='1.0' encoding='UTF-8'?><!DOCTYPE metadata SYSTEM \"http://www.fgdc.gov/metadata/fgdc-std-001-1998.dtd\">"
    met4 = '<?xml version=\"1.0\" encoding=\"UTF-8\"?><!DOCTYPE metadata SYSTEM \"http://www.fgdc.gov/metadata/fgdc-std-001-1998.dtd\">'

    newFgdcText = met4 + met1

    return newFgdcText
#
# When writing to a file that's used by "curl" the format is a bit different
#
def changeFGDCHeaderForFile(metadata):
    start = metadata.find("<metadata>")
    met1 = metadata[start:].replace("\"","")
    # May need to get rid of all & characters too


    fileFGDCHeader = '<?xml version=\\"1.0\\" encoding=\\"UTF-8\\"?><!DOCTYPE metadata SYSTEM \\"http://www.fgdc.gov/metadata/fgdc-std-001-1998.dtd\\">'
    newFgdcText = fileFGDCHeader + met1

    return newFgdcText

#
# When writing to a file that's used by "curl" the format is a bit different
#
def changeFGDCHeaderForDBMS(metadata):
    start = metadata.find("<metadata>")
    met1 = metadata[start:].replace("\"","")
    fileFGDCHeader = '<?xml version=\"1.0\" encoding=\"UTF-8\"?>'
    newFgdcText = fileFGDCHeader + met1

    return newFgdcText

# Return the year portion of the date
# the FGDC date field is a free format string
# this function does a little to clean it up and creates a UTC date
# solr requires the date to be something like 1995-12-31T23:59:59Z
def createSolrDate(passedDate):
    returnYear = "0001"

    if passedDate == "":
       return ""

    if len(passedDate) >= 6:
        temp = passedDate[2:6]
        if temp.isdigit():
            returnYear = temp

    if len(passedDate) >= 5:
        temp = passedDate[1:5]
        if temp.isdigit():
            returnYear = temp

    if len(passedDate) >= 4:
        temp = passedDate[0:4]
        if temp.isdigit():
            returnYear = temp

    returnValue = returnYear + "-01-01T01:01:01Z"
    return returnValue