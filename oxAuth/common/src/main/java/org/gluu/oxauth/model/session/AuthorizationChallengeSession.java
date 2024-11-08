package org.gluu.oxauth.model.session;

import org.gluu.persist.annotation.*;
import org.gluu.persist.model.base.DeletableEntity;

import java.io.Serializable;
import java.util.Date;

/**
 * @author Yuriy Z
 */
@DataEntry
@ObjectClass(value = "oxAuthzChallSess")
public class AuthorizationChallengeSession extends DeletableEntity implements Serializable {

    @DN
    private String dn;

    @AttributeName(name = "oxId")
    private String id;

    @AttributeName(name = "oxAuthUserDN")
    private String userDn;

    @AttributeName(name = "creationDate")
    private Date creationDate = new Date();

    @AttributeName(name = "oxAuthClientId")
    private String clientId;

    @AttributeName(name = "oxAttributes")
    @JsonObject
    private AuthorizationChallengeSessionAttributes attributes;

    @Expiration
    private int ttl;


    @Override
    public String getDn() {
        return dn;
    }

    @Override
    public void setDn(String dn) {
        this.dn = dn;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getUserDn() {
        return userDn;
    }

    public void setUserDn(String userDn) {
        this.userDn = userDn;
    }

    public Date getCreationDate() {
        return creationDate;
    }

    public void setCreationDate(Date creationDate) {
        this.creationDate = creationDate;
    }

    public String getClientId() {
        return clientId;
    }

    public void setClientId(String clientId) {
        this.clientId = clientId;
    }

    public AuthorizationChallengeSessionAttributes getAttributes() {
        if (attributes == null) attributes = new AuthorizationChallengeSessionAttributes();
        return attributes;
    }

    public void setAttributes(AuthorizationChallengeSessionAttributes attributes) {
        this.attributes = attributes;
    }

    public int getTtl() {
        return ttl;
    }

    public void setTtl(int ttl) {
        this.ttl = ttl;
    }

    @Override
    public String toString() {
        return "AuthorizationChallengeSession{" +
                "dn='" + dn + '\'' +
                ", id='" + id + '\'' +
                ", userDn='" + userDn + '\'' +
                ", creationDate=" + creationDate +
                ", clientId='" + clientId + '\'' +
                ", attributes=" + attributes +
                ", ttl=" + ttl +
                "} " + super.toString();
    }
}
