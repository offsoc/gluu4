/*
 * oxEleven is available under the MIT License (2008). See http://opensource.org/licenses/MIT for full text.
 *
 * Copyright (c) 2016, Gluu
 */

package org.gluu.oxeleven.client;

import javax.ws.rs.core.MultivaluedMap;
import javax.ws.rs.core.Response;

import org.json.JSONException;
import org.json.JSONObject;

/**
 * @author Javier Rojas Blum
 * @version March 20, 2017
 */
public abstract class BaseResponse {

    protected int status;
    protected String location;
    protected String entity;
    protected MultivaluedMap<String, Object> headers;

    public BaseResponse(Response clientResponse) {
        if (clientResponse != null) {
            status = clientResponse.getStatus();
            entity = clientResponse.readEntity(String.class);
            headers = clientResponse.getHeaders();
            if (clientResponse.getLocation() != null) {
                location = clientResponse.getLocation().toString();
            }
        }
    }

    public int getStatus() {
        return status;
    }

    public String getLocation() {
        return location;
    }

    public String getEntity() {
        return entity;
    }

    public MultivaluedMap<String, Object> getHeaders() {
        return headers;
    }

    public JSONObject getJSONEntity() {
        if (entity != null) {
            try {
                JSONObject jsonObject = new JSONObject(entity);
                return jsonObject;
            } catch (JSONException e) {
                e.printStackTrace();
            }
        }

        return null;
    }
}
