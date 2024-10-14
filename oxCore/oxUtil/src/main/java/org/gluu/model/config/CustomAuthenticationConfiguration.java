/*
 * oxCore is available under the MIT License (2008). See http://opensource.org/licenses/MIT for full text.
 *
 * Copyright (c) 2014, Gluu
 */

package org.gluu.model.config;

import java.util.ArrayList;
import java.util.List;

import javax.persistence.Transient;

import org.gluu.model.AuthenticationScriptUsageType;
import org.gluu.model.SimpleCustomProperty;

/**
 * Custom authentication configuration
 *
 * @author Yuriy Movchan Date: 04/08/2012
 */
public class CustomAuthenticationConfiguration {

    private String name;
    private int level;
    private int priority;
    private boolean enabled;
    private int version;

    private AuthenticationScriptUsageType usageType;

    private List<SimpleCustomProperty> customAuthenticationAttributes;
    private String customAuthenticationScript;

    @Transient
    private transient String dn;

    @Transient
    private transient String inum;

    public CustomAuthenticationConfiguration() {
        this.customAuthenticationAttributes = new ArrayList<SimpleCustomProperty>();
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getLevel() {
        return level;
    }

    public void setLevel(int level) {
        this.level = level;
    }

    public int getPriority() {
        return priority;
    }

    public void setPriority(int priority) {
        this.priority = priority;
    }

    public boolean isEnabled() {
        return enabled;
    }

    public void setEnabled(boolean enabled) {
        this.enabled = enabled;
    }

    public int getVersion() {
        return version;
    }

    public void setVersion(int version) {
        this.version = version;
    }

    public AuthenticationScriptUsageType getUsageType() {
        return usageType;
    }

    public void setUsageType(AuthenticationScriptUsageType usageType) {
        this.usageType = usageType;
    }

    public List<SimpleCustomProperty> getCustomAuthenticationAttributes() {
        return customAuthenticationAttributes;
    }

    public void setCustomAuthenticationAttributes(List<SimpleCustomProperty> customAuthenticationAttributes) {
        this.customAuthenticationAttributes = customAuthenticationAttributes;
    }

    public String getCustomAuthenticationScript() {
        return customAuthenticationScript;
    }

    public void setCustomAuthenticationScript(String customAuthenticationScript) {
        this.customAuthenticationScript = customAuthenticationScript;
    }

    public String getDn() {
        return dn;
    }

    public void setDn(String dn) {
        this.dn = dn;
    }

    public String getInum() {
        return inum;
    }

    public void setInum(String inum) {
        this.inum = inum;
    }

}
