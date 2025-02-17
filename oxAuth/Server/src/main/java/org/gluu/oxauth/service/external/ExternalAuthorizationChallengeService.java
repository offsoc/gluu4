package org.gluu.oxauth.service.external;

import org.gluu.model.custom.script.CustomScriptType;
import org.gluu.model.custom.script.conf.CustomScriptConfiguration;
import org.gluu.model.custom.script.type.authzchallenge.AuthorizationChallengeType;
import org.gluu.oxauth.model.authorize.AuthorizeErrorResponseType;
import org.gluu.oxauth.model.common.ExecutionContext;
import org.gluu.oxauth.model.configuration.AppConfiguration;
import org.gluu.oxauth.model.error.ErrorResponseFactory;
import org.gluu.oxauth.service.external.context.ExternalScriptContext;
import org.gluu.service.custom.script.ExternalScriptService;

import javax.enterprise.context.ApplicationScoped;
import javax.inject.Inject;
import javax.ws.rs.WebApplicationException;
import javax.ws.rs.core.Response;
import java.util.List;

/**
 * @author Yuriy Z
 */
@ApplicationScoped
public class ExternalAuthorizationChallengeService extends ExternalScriptService {

    @Inject
    private transient AppConfiguration appConfiguration;

    @Inject
    private transient ErrorResponseFactory errorResponseFactory;

    public ExternalAuthorizationChallengeService() {
        super(CustomScriptType.AUTHORIZATION_CHALLENGE);
    }

    public boolean externalAuthorize(ExecutionContext executionContext) {
        final List<String> acrValues = executionContext.getAuthzRequest().getAcrValuesList();
        final CustomScriptConfiguration script = identifyScript(acrValues);
        if (script == null) {
            String msg = String.format("Unable to identify script by acr_values %s.", acrValues);
            log.debug(msg);
            throw new WebApplicationException(errorResponseFactory
                    .newErrorResponse(Response.Status.BAD_REQUEST)
                    .entity(errorResponseFactory.getErrorAsJson(AuthorizeErrorResponseType.INVALID_REQUEST, executionContext.getAuthzRequest().getState(), msg))
                    .build());
        }

        log.trace("Executing python 'authorize' method, script name: {}, clientId: {}, scope: {}, authorizationChallengeSession: {}",
                script.getName(), executionContext.getAuthzRequest().getClientId(), executionContext.getAuthzRequest().getScope(), executionContext.getAuthzRequest().getAuthorizationChallengeSession());

        executionContext.setScript(script);

        boolean result = false;
        try {
            AuthorizationChallengeType authorizationChallengeType = (AuthorizationChallengeType) script.getExternalType();
            final ExternalScriptContext scriptContext = new ExternalScriptContext(executionContext);
            result = authorizationChallengeType.authorize(scriptContext);

            scriptContext.throwWebApplicationExceptionIfSet();
        } catch (WebApplicationException e) {
            if (log.isTraceEnabled()) {
                log.trace("WebApplicationException from script", e);
            }
            throw e;
        } catch (Exception ex) {
            log.error(ex.getMessage(), ex);
            saveScriptError(script.getCustomScript(), ex);
        }

        log.trace("Finished 'authorize' method, script name: {}, clientId: {}, result: {}", script.getName(), executionContext.getAuthzRequest().getClientId(), result);

        return result;
    }

    public CustomScriptConfiguration identifyScript(List<String> acrValues) {
        log.trace("Identifying script, acr_values: {}", acrValues);

        if (acrValues == null || acrValues.isEmpty()) {
            log.trace("No acr_values, return default script");
            return getCustomScriptConfigurationByName(appConfiguration.getAuthorizationChallengeDefaultAcr());
        }

        for (String acr : acrValues) {
            final CustomScriptConfiguration script = getCustomScriptConfigurationByName(acr);
            if (script != null) {
                log.trace("Found script {} by acr {}", script.getInum(), acr);
                return script;
            }
        }

        log.trace("Unable to find script by acr_values {}", acrValues);
        return getCustomScriptConfigurationByName(appConfiguration.getAuthorizationChallengeDefaultAcr());
    }
}
