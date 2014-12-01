"""Test setup for integration and functional tests.

When we import PloneTestCase and then call setupPloneSite(), all of
Plone's products are loaded, and a Plone site will be created. This
happens at module level, which makes it faster to run each test, but
slows down test runner startup.
"""

from Products.Five import zcml
from Products.Five import fiveconfigure

from Testing import ZopeTestCase as ztc

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

# When ZopeTestCase configures Zope, it will *not* auto-load products
# in Products/. Instead, we have to use a statement such as:
#   ztc.installProduct('SimpleAttachment')
# This does *not* apply to products in eggs and Python packages (i.e.
# not in the Products.*) namespace. For that, see below.
# All of Plone's products are already set up by PloneTestCase.

ztc.installProduct('uwosh.thememain')

@onsetup
def setup_product():
    """Set up the package and its dependencies.

    The @onsetup decorator causes the execution of this body to be
    deferred until the setup of the Plone site testing layer. We could
    have created our own layer, but this is the easiest way for Plone
    integration tests.
    """

    # Load the ZCML configuration for the example.tests package.
    # This can of course use <include /> to include other packages.

    fiveconfigure.debug_mode = True
    import uwosh.themebase
    zcml.load_config('configure.zcml', uwosh.thememain)
    fiveconfigure.debug_mode = False

# The order here is important: We first call the (deferred) function
# which installs the products we need for this product. Then, we let
# PloneTestCase set up this product on installation.

setup_product()
ptc.setupPloneSite(products=['uwosh.thememain'])

#this is what we would like to generate so we can test it out.
site_structure = {
    'future-students' : {
        'undergraduate' : {
            'academic' : {},
            'admissions': {},
            'costs-and-financial-aid': {},
            'scholarships': {},
            'health-and-wellness': {},
            'athletics': {},
            'compus-life' : {},
            'student-organizations': {}
        },
        'graduate': {},
        'adult-non-traditional': {},
        'transfer-students': {},
        'international-students': {},
        'continuing-education': {}
    }
}

def import_site_structure(root, structure):
    
    for key, value in structure.items():
        root.invokeFactory(type_name="Folder", id=key)
        setattr(root[key], 'title', key)
        import_site_structure(root[key], value)
    

class TestCase(ptc.PloneTestCase):
    """We use this base class for all the tests in this package. If
    necessary, we can put common utility or setup code in here. This
    applies to unit test cases.
    """

class FunctionalTestCase(ptc.FunctionalTestCase):
    """We use this class for functional integration tests that use
    doctest syntax. Again, we can put basic common utility or setup
    code in here.
    """

    def afterSetUp(self):
        roles = ('Member', 'Contributor')
        self.portal.portal_membership.addMember('contributor',
                                                'secret',
                                                roles, [])
        self.setRoles(['Manager'])
        
        self.portal.use_uwosh_home_url = False
        
        #remove portlets
        from zope.component import getUtility, getMultiAdapter
        from plone.portlets.interfaces import IPortletManager
        from plone.portlets.interfaces import IPortletAssignmentMapping
        
        left_column = getUtility(IPortletManager, name=u"plone.leftcolumn")
        left_assignable = getMultiAdapter((self.portal, left_column), IPortletAssignmentMapping)
        for name in left_assignable.keys():
            del left_assignable[name]
        
        right_column = getUtility(IPortletManager, name=u"plone.rightcolumn")
        right_assignable = getMultiAdapter((self.portal, right_column), IPortletAssignmentMapping)
        for name in right_assignable.keys():
            del right_assignable[name]
        
        import_site_structure(self.portal, site_structure)

from Products.Five.testbrowser import Browser
browser = Browser()
from Products.PloneTestCase.setup import portal_owner, default_password
browser.addHeader('Authorization', 'Basic %s:%s' % (portal_owner, default_password))
