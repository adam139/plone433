from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from zope.configuration import xmlconfig

class My315okDiaozo960(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)
    
    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import collective.diazotheme.bootstrap
        xmlconfig.file('configure.zcml', collective.diazotheme.bootstrap, context=configurationContext)
    
    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.diazotheme.bootstrap:default')

MY315OK_DIAZO960_FIXTURE = My315okDiaozo960()
MY315OK_DIAZO960_INTEGRATION_TESTING = IntegrationTesting(bases=(MY315OK_DIAZO960_FIXTURE,), name="My315okDiaozo960:Integration")
MY315OK_DIAZO960_FUNCTION_TESTING = FunctionalTesting(bases=(MY315OK_DIAZO960_FIXTURE,), name="My315okDiaozo960:Functional")
