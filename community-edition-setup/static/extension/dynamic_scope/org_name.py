# oxAuth is available under the MIT License (2008). See http://opensource.org/licenses/MIT for full text.
# Copyright (c) 2016, Gluu
#
# Author: Yuriy Movchan
#

from org.gluu.model.custom.script.type.scope import DynamicScopeType
from org.gluu.oxauth.service.common import UserService
from org.gluu.util import StringHelper, ArrayHelper
from java.util import Arrays, ArrayList

import java

class DynamicScope(DynamicScopeType):
    def __init__(self, currentTimeMillis):
        self.currentTimeMillis = currentTimeMillis

    def init(self, customScript, configurationAttributes):
        print "Dynamic scope. Initialization"

        print "Dynamic scope. Initialized successfully"

        return True   

    def destroy(self, configurationAttributes):
        print "Dynamic scope. Destroy"
        print "Dynamic scope. Destroyed successfully"
        return True   

    # Update Json Web token before signing/encrypring it
    #   dynamicScopeContext is org.gluu.oxauth.service.external.context.DynamicScopeExternalContext
    #   configurationAttributes is java.util.Map<String, SimpleCustomProperty>
    def update(self, dynamicScopeContext, configurationAttributes):
        print "Dynamic scope. Update method"

        dynamicScopes = dynamicScopeContext.getDynamicScopes()
        authorizationGrant = dynamicScopeContext.getAuthorizationGrant()
        user = dynamicScopeContext.getUser()
        jsonWebResponse = dynamicScopeContext.getJsonWebResponse()
        claims = jsonWebResponse.getClaims()

        # Add organization name if there is scope = org_name
        claims.setClaim("org_name", "Gluu, Inc.")

        return True

    def getSupportedClaims(self, configurationAttributes):
        return Arrays.asList("org_name")

    def getApiVersion(self):
        return 11
