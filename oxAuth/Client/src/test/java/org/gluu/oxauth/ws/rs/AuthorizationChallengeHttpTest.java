package org.gluu.oxauth.ws.rs;

import com.google.common.collect.Lists;
import org.gluu.oxauth.BaseTest;
import org.gluu.oxauth.client.*;
import org.gluu.oxauth.model.common.*;
import org.gluu.oxauth.model.register.ApplicationType;
import org.gluu.oxauth.model.util.StringUtils;
import org.testng.annotations.Parameters;
import org.testng.annotations.Test;

import java.util.Arrays;
import java.util.List;
import java.util.UUID;

import static org.testng.AssertJUnit.*;

/**
 * @author Yuriy Z
 */
public class AuthorizationChallengeHttpTest extends BaseTest {

    /**
     * Test for the complete Authorization Challenge Flow.
     */
    @Parameters({"userId", "userSecret", "redirectUris", "redirectUri"})
    @Test
    public void authorizationChallengeFlow(
            final String userId, final String userSecret, final String redirectUris, final String redirectUri) throws Exception {
        showTitle("authorizationChallengeFlow");

        List<ResponseType> responseTypes = Arrays.asList(
                ResponseType.CODE,
                ResponseType.ID_TOKEN);
        List<GrantType> grantTypes = Arrays.asList(GrantType.AUTHORIZATION_CODE, GrantType.REFRESH_TOKEN);
        List<String> scopes = Arrays.asList("openid", "profile", "address", "email", "phone", "user_name", "authorization_challenge");

        // 1. Register client
        RegisterResponse registerResponse = registerClient(redirectUris, responseTypes, grantTypes, scopes);
        String clientId = registerResponse.getClientId();
        String clientSecret = registerResponse.getClientSecret();

        // 2. Request authorization code at Authorization Challenge Endpoint
        String nonce = UUID.randomUUID().toString();
        String state = UUID.randomUUID().toString();

        AuthorizationRequest authorizationRequest = new AuthorizationRequest(null);
        authorizationRequest.setClientId(clientId);
        authorizationRequest.setAcrValues(Lists.newArrayList());
        authorizationRequest.setScopes(scopes);
        authorizationRequest.setNonce(nonce);
        authorizationRequest.setState(state);
        authorizationRequest.addCustomParameter("username", userId);
        authorizationRequest.addCustomParameter("otp", userSecret);
        authorizationRequest.setAuthorizationMethod(AuthorizationMethod.FORM_ENCODED_BODY_PARAMETER);

        AuthorizeClient authorizeClient = new AuthorizeClient(authorizationChallengeEndpoint);
        authorizeClient.setRequest(authorizationRequest);

        AuthorizationResponse authorizationResponse = authorizeClient.exec();
        showClient(authorizeClient);
        assertNotNull(authorizationResponse);
        String authorizationCode = authorizationResponse.getCode();
        assertNotNull(authorizationCode);
        System.out.println(String.format("Successfully obtained authorization code %s at Authorization Challenge Endpoint", authorizationCode));

        // 3. Request access token using the authorization code.
        TokenRequest tokenRequest = new TokenRequest(GrantType.AUTHORIZATION_CODE);
        tokenRequest.setCode(authorizationCode);
        tokenRequest.setRedirectUri(redirectUri);
        tokenRequest.setAuthUsername(clientId);
        tokenRequest.setAuthPassword(clientSecret);
        tokenRequest.setAuthenticationMethod(AuthenticationMethod.CLIENT_SECRET_BASIC);

        TokenClient tokenClient1 = newTokenClient(tokenRequest);
        tokenClient1.setRequest(tokenRequest);

        TokenResponse tokenResponse1 = tokenClient1.exec();
        showClient(tokenClient1);

        assertNotNull(tokenResponse1);
        assertNotNull(tokenResponse1.getIdToken());
        assertNotNull(tokenResponse1.getAccessToken());

        String accessToken = tokenResponse1.getAccessToken();

        // 6. Request user info
        UserInfoClient userInfoClient = new UserInfoClient(userInfoEndpoint);
        userInfoClient.setExecutor(clientEngine(true));
        UserInfoResponse userInfoResponse = userInfoClient.execUserInfo(accessToken);
        showClient(userInfoClient);

        assertNotNull(userInfoResponse);
    }

    /**
     * Test for the complete Authorization Challenge Flow.
     */
    @Parameters({"userSecret", "redirectUris", "redirectUri"})
    @Test
    public void authorizationChallengeFlow_withInvalidUsername_shouldGetError(
            final String userSecret, final String redirectUris, final String redirectUri) {
        showTitle("authorizationChallengeFlow");
        String userId = "invalidUser";

        List<ResponseType> responseTypes = Arrays.asList(
                ResponseType.CODE,
                ResponseType.ID_TOKEN);
        List<GrantType> grantTypes = Arrays.asList(GrantType.AUTHORIZATION_CODE, GrantType.REFRESH_TOKEN);
        List<String> scopes = Arrays.asList("openid", "profile", "address", "email", "phone", "user_name");

        // 1. Register client
        RegisterResponse registerResponse = registerClient(redirectUris, responseTypes, grantTypes, scopes);
        String clientId = registerResponse.getClientId();

        // 2. Request authorization code at Authorization Challenge Endpoint
        String nonce = UUID.randomUUID().toString();
        String state = UUID.randomUUID().toString();

        AuthorizationRequest authorizationRequest = new AuthorizationRequest(null);
        authorizationRequest.setClientId(clientId);
        authorizationRequest.setAcrValues(Lists.newArrayList());
        authorizationRequest.setScopes(scopes);
        authorizationRequest.setNonce(nonce);
        authorizationRequest.setState(state);
        authorizationRequest.addCustomParameter("username", userId);
        authorizationRequest.addCustomParameter("password", userSecret);
        authorizationRequest.setAuthorizationMethod(AuthorizationMethod.FORM_ENCODED_BODY_PARAMETER);

        AuthorizeClient authorizeClient = new AuthorizeClient(authorizationChallengeEndpoint);
        authorizeClient.setRequest(authorizationRequest);

        AuthorizationResponse authorizationResponse = authorizeClient.exec();
        showClient(authorizeClient);

        assertNotNull(authorizationResponse);
        assertNull(authorizationResponse.getCode());
        assertEquals(authorizationResponse.getErrorTypeString(), "username_invalid");
    }

    public RegisterResponse registerClient(final String redirectUris, List<ResponseType> responseTypes, List<GrantType> grantTypes, List<String> scopes) {
        RegisterRequest registerRequest = new RegisterRequest(ApplicationType.WEB, "test app",
                StringUtils.spaceSeparatedToList(redirectUris));
        registerRequest.setResponseTypes(responseTypes);
        registerRequest.setScope(scopes);
        registerRequest.setGrantTypes(grantTypes);
        registerRequest.setSubjectType(SubjectType.PUBLIC);
        RegisterClient registerClient = newRegisterClient(registerRequest);

        RegisterResponse registerResponse = registerClient.exec();
        showClient(registerClient);

        assertNotNull(registerResponse);
        return registerResponse;
    }
}