# -*- coding: utf8 -*-

from collective.diazotheme.bootstrap import logger 

#def install(portal, reinstall=False):
#    # Not needed if you don't need to run different profile conditionally
#    setup_tool = portal.portal_setup
#    setup_tool.runAllImportStepsFromProfile('profile-example.gs:default')
#    logger.info("Installed")



def uninstall(portal, reinstall=False):
    if not reinstall:
        setup_tool = portal.portal_setup
        setup_tool.runAllImportStepsFromProfile('profile-collective.diazotheme.bootstrap:uninstall')

        logger.info("Uninstall done")
