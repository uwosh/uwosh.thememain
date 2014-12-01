from uwosh.core.utils import *
from uwosh.thememain import dependencies
from uwosh.thememain.interfaces import ISectionNavigation

def setupVarious(context):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('uwosh.thememain.txt') is None:
        return