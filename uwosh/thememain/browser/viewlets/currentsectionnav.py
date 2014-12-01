from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from Products.CMFCore.utils import getToolByName
from plone.app.layout.navigation.navtree import buildFolderTree
from Acquisition import aq_inner, aq_base, aq_parent
from Products.CMFPlone import utils
from uwosh.thememain.interfaces import ISectionNavigation

class CurrentSectionNav(ViewletBase):
    render = ViewPageTemplateFile('currentsectionnav_viewlet.pt')

    def update(self):
        """
        only grab second level of links.  For instance, if you are in the root,
        do not show this, but if you are in a folder inside the root, show this.
        
        Examples,
        
        root/future students
            -will show and future students will be base
        root/future students/undergraduate/file
            -same as earlier
        root/
            -will not show
        
        """
        super(CurrentSectionNav, self).update()
        
        site = self.portal_state.portal()
        context = aq_inner(self.context)
        utils = getToolByName(context, 'plone_utils')
        self.shoulddisplay = True
        
        if utils.isDefaultPage(context, self.request) or not utils.isStructuralFolder(context):
            context = aq_parent(context)
          
        if not ISectionNavigation.providedBy(context):
            self.shoulddisplay = False
            return
          
        context_path = context.getPhysicalPath()
        site_path = site.getPhysicalPath()
        nav_path = context_path[0:len(site_path)+1]
        selected_item_path = context_path[0:len(site_path)+2]
        
        #need this for the title of the nav
        self.nav_context = site.unrestrictedTraverse('/'.join(nav_path))
        #need this to find the current item
        self.selected_item = site.unrestrictedTraverse('/'.join(selected_item_path))
        
        self.portal_tabs = buildFolderTree(
            context, 
            obj=context, 
            query={
                'query' : '/'.join(nav_path),
                'navtree' : 1,
                'navtree_start' : 1,
                'path': '/'.join(nav_path)
            }
        )

        # need to make this all one call right here for some reason,
        # otherwise it can't figure out the absolute_url
        self.nav_context_url = site.unrestrictedTraverse('/'.join(nav_path)).absolute_url()
        
        
        
