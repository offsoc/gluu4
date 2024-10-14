/*
 * Gluu casa admin API
 * Allows to configure Casa programmatically. Note that plugins may also expose endpoints to apply configurations relevant to their topics. Check plugins' docs for more information
 *
 * OpenAPI spec version: 4.3.0
 * 
 *
 * NOTE: This class is auto generated by the swagger code generator program.
 * https://github.com/swagger-api/swagger-codegen.git
 * Do not edit the class manually.
 */


package org.gluu.casa.client.config.model;

import java.util.Objects;
import java.util.Arrays;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonValue;
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import org.gluu.casa.client.config.model.ClientSettings;
import org.gluu.casa.client.config.model.OxdSettings;

/**
 * OxdConfiguration
 */
@javax.annotation.Generated(value = "io.swagger.codegen.languages.JavaClientCodegen", date = "2021-07-18T14:15:05.565Z")
public class OxdConfiguration {
  @JsonProperty("settings")
  private OxdSettings settings = null;

  @JsonProperty("client_details")
  private ClientSettings clientDetails = null;

  public OxdConfiguration settings(OxdSettings settings) {
    this.settings = settings;
    return this;
  }

   /**
   * Get settings
   * @return settings
  **/
  @ApiModelProperty(required = true, value = "")
  public OxdSettings getSettings() {
    return settings;
  }

  public void setSettings(OxdSettings settings) {
    this.settings = settings;
  }

  public OxdConfiguration clientDetails(ClientSettings clientDetails) {
    this.clientDetails = clientDetails;
    return this;
  }

   /**
   * Get clientDetails
   * @return clientDetails
  **/
  @ApiModelProperty(required = true, value = "")
  public ClientSettings getClientDetails() {
    return clientDetails;
  }

  public void setClientDetails(ClientSettings clientDetails) {
    this.clientDetails = clientDetails;
  }


  @Override
  public boolean equals(java.lang.Object o) {
    if (this == o) {
      return true;
    }
    if (o == null || getClass() != o.getClass()) {
      return false;
    }
    OxdConfiguration oxdConfiguration = (OxdConfiguration) o;
    return Objects.equals(this.settings, oxdConfiguration.settings) &&
        Objects.equals(this.clientDetails, oxdConfiguration.clientDetails);
  }

  @Override
  public int hashCode() {
    return Objects.hash(settings, clientDetails);
  }


  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder();
    sb.append("class OxdConfiguration {\n");
    
    sb.append("    settings: ").append(toIndentedString(settings)).append("\n");
    sb.append("    clientDetails: ").append(toIndentedString(clientDetails)).append("\n");
    sb.append("}");
    return sb.toString();
  }

  /**
   * Convert the given object to string with each line indented by 4 spaces
   * (except the first line).
   */
  private String toIndentedString(java.lang.Object o) {
    if (o == null) {
      return "null";
    }
    return o.toString().replace("\n", "\n    ");
  }

}
