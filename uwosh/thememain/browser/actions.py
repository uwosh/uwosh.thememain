from Products.Five.browser import BrowserView
from Acquisition import aq_inner
from uwosh.thememain.interfaces import ISectionNavigation
from zope.interface import alsoProvides, noLongerProvides

class MakeSectionNavigable(BrowserView):
    
    def __call__(self):
        context = aq_inner(self.context)
        
        if not ISectionNavigation.providedBy(context):
            alsoProvides(context, ISectionNavigation)
            context.reindexObject(idxs=['object_provides'])
        
        self.request.response.redirect(context.absolute_url())
    
class RemoveSectionNavigable(BrowserView):
    
    
    def __call__(self):
        """
        some of this copied from Martin Aspeli in
        collective.flowplayer
        """
        context = aq_inner(self.context)
        
        if ISectionNavigation.providedBy(context):
            noLongerProvides(context, ISectionNavigation)
            context.reindexObject(idxs=['object_provides'])
                
        self.request.response.redirect(context.absolute_url())  