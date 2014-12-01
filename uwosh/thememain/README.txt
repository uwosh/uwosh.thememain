Introduction
============
This package pretty much organizes and extends the uwosh.themebase package.
Some of the thing it does,
    - adds plone theme
    - organizes viewlets of uwosh.themebase
    - adds "gray bar" navigation viewlet CurrentSectionNav
    - adds action on Folder and Large Plone Folder types to enable/disable gray bar nav
    - the nav bar will only show links from the 2nd level on to the 3rd level, but
        it can be enabled at any level
    
Compatibility
=============
Requires Plone 3.0 or higher and requires uwosh.themebase, uwosh.core, uwosh.requirements, 
and uwosh.default

Tests
========
Here is where I'll describe how it works and show how it works...

Before running this doctest, a site structure is generated so we can test how this works
take a look at tests/base.py for site_stucture to see how it looks

First off, let's navigate to one of the folders and see how it looks
Since by default the skins do not show the site structure and I'm too lazy
to make the portlet do it, just navigation straight to something...
    >>> browser.open('http://nohost/plone/future-students')
    
    >>> "Create Nav" in browser.contents
    True
    >>> "Remove Nav" in browser.contents
    True
    
Now that we know the buttons were created correctly,
let's test it!

Create the navigation
    >>> browser.getLink("Create Nav").click()
    >>> """<div id="currentSectionNav">""" in browser.contents
    True
    
Remove the navigation
    >>> browser.getLink("Remove Nav").click()
    >>> """<div id="currentSectionNav">""" in browser.contents
    False
    
Now, let's turn it back on and make sure it renders it correctly
    >>> browser.getLink("Create Nav").click()
    >>> """<li id="portaltab-undergraduate""" in browser.contents
    True
    >>> """<li id="portaltab-graduate""" in browser.contents
    True
    >>> """<li id="portaltab-transfer-students""" in browser.contents
    True
    >>> """<li id="portaltab-international-students""" in browser.contents
    True
    >>> """<li id="portaltab-continuing-education""" in browser.contents
    True
    >>> """<li id="portaltab-adult-non-traditional""" in browser.contents
    True
    
Also make sure it adds a higher level link back
    >>> """<h1>future-students</h1>""" in browser.contents
    True
    
    >>> link = browser.getLink("future-students")
    >>> link.url
    'http://nohost/plone/future-students'
    
Now if we traverse down another level, the section nav
should no longer be showing.  So we then have to enable it.

    >>> browser.getLink("undergraduate").click()    
    >>> """<div id="currentSectionNav">""" in browser.contents
    False
    
enable it
    >>> browser.getLink("Create Nav").click()
    
now it should be showing with all the sweet links
    
    >>> """<div id="currentSectionNav">""" in browser.contents
    True
    >>> """<li id="portaltab-undergraduate""" in browser.contents
    True
    >>> """<li id="portaltab-graduate""" in browser.contents
    True
    >>> """<li id="portaltab-transfer-students""" in browser.contents
    True
    >>> """<li id="portaltab-international-students""" in browser.contents
    True
    >>> """<li id="portaltab-continuing-education""" in browser.contents
    True
    >>> """<li id="portaltab-adult-non-traditional""" in browser.contents
    True

Also make sure it still adds a higher level link back
    >>> """<h1>future-students</h1>""" in browser.contents
    True

    >>> link = browser.getLink("future-students")
    >>> link.url
    'http://nohost/plone/future-students'

Alright, we still should test another level down.  Never know what'll happen.
One problem is that I disabled the nav viewlet so you can't get a link to the
next object down.  No worries, just call the url manaully.
You also will need to enable the section nav first.

    >>> browser.open("http://nohost/plone/future-students/undergraduate/academic")
    >>> """<div id="currentSectionNav">""" in browser.contents
    False
    
enable it
    >>> browser.getLink("Create Nav").click()
    
now it should be showing with all the sweet links
    
    >>> """<div id="currentSectionNav">""" in browser.contents
    True
    >>> """<li id="portaltab-undergraduate""" in browser.contents
    True
    >>> """<li id="portaltab-graduate""" in browser.contents
    True
    >>> """<li id="portaltab-transfer-students""" in browser.contents
    True
    >>> """<li id="portaltab-international-students""" in browser.contents
    True
    >>> """<li id="portaltab-continuing-education""" in browser.contents
    True
    >>> """<li id="portaltab-adult-non-traditional""" in browser.contents
    True

Also make sure it still adds a higher level link back
    >>> """<h1>future-students</h1>""" in browser.contents
    True

    >>> link = browser.getLink("future-students")
    >>> link.url
    'http://nohost/plone/future-students'

Alright, so far so good, but let's test this even more.
If you exclude some from navigation, does it remove them from the gray bar?
    >>> self.portal['future-students']['undergraduate'].setExcludeFromNav(True)
    >>> self.portal['future-students']['undergraduate'].reindexObject()
    >>> browser.open(browser.url)
    
    >>> """<li id="portaltab-undergraduate""" in browser.contents
    False
    
Awesome, it does remove it from the gray bar. Re-enable that one now.
    >>> self.portal['future-students']['undergraduate'].setExcludeFromNav(False)
    >>> self.portal['future-students']['undergraduate'].reindexObject()
    >>> browser.open(browser.url)
    
    >>> """<li id="portaltab-undergraduate""" in browser.contents
    True
    
    