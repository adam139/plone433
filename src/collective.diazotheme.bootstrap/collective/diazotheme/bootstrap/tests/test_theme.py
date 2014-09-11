import unittest2 as unittest
import transaction

from collective.diazotheme.bootstrap.testing import MY315OK_DIAZO960_INTEGRATION_TESTING
from collective.diazotheme.bootstrap.testing import MY315OK_DIAZO960_FUNCTION_TESTING

from plone.testing.z2 import Browser
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD

from zope.component import getUtility
from Products.CMFCore.utils import getToolByName

from plone.registry.interfaces import IRegistry
from plone.app.theming.interfaces import IThemeSettings

class TestSetup(unittest.TestCase):
    
    layer = MY315OK_DIAZO960_INTEGRATION_TESTING
    
#    def test_css_registry_configured(self):
#        portal = self.layer['portal']
#        cssRegistry = getToolByName(portal, 'portal_css')
#        self.assertTrue("++theme++collective.diazotheme.bootstrap/css/grid.css" 
#                in cssRegistry.getResourceIds()
#            )
#        self.assertTrue("++theme++collective.diazotheme.bootstrap/css/theme.css"
#                in cssRegistry.getResourceIds()
#            )
    
    def test_theme_configured(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IThemeSettings)
        self.assertEqual(settings.enabled, True)
        self.assertEqual(settings.rules, 
                "/++theme++collective.diazotheme.bootstrap/rules.xml"
            )
        self.assertEqual(settings.absolutePrefix,
                "/++theme++collective.diazotheme.bootstrap"
            )

class TestRendering(unittest.TestCase):
    
    layer = MY315OK_DIAZO960_FUNCTION_TESTING
    
    def test_render_plone_page(self):
        app = self.layer['app']
        portal = self.layer['portal']
        
        transaction.commit()
        
        browser = Browser(app)
        #open('/tmp/test.html','w').write(browser.contents)    
        browser.open(portal.absolute_url())
        self.assertTrue('<div id="site-scripts">' in browser.contents)

#    def test_manage_portlets_page(self):
#        app = self.layer['app']
#        portal = self.layer['portal']
#        
#        transaction.commit()
#        
#        browser = Browser(app)
#        browser.addHeader('Authorization', 'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD,))
#        
#        browser.open(portal.absolute_url() + '/@@manage-portlets')
#        
#        self.assertFalse('<h2 class="myportlets" i18n:translate="" >Manage mylogo portalheader Portlets</h2>' in browser.contents)        
    
                
    def test_render_zmi_page(self):
        app = self.layer['app']
        portal = self.layer['portal']
        
        transaction.commit()
        
        browser = Browser(app)
        browser.addHeader('Authorization', 'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD,))
        
        browser.open(portal.absolute_url() + '/manage_main')
        
        self.assertFalse('<body class="plonesite">' in browser.contents)
