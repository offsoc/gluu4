# Email OTP Plugin

## Overview

This plugin allows end-users to receive one-time passcodes to one of their registered e-mail addresses in order to get access to Casa.

!!! Note
    This plugin is only available for Gluu Casa version 4.5.3 or higher

## Requisites

- Gluu Server configured with SMTP
- Custom jython script added to server
- Custom pages added to server
- Plugin onboarded in Casa

### SMTP Configuration

In oxTrust, visit `Configuration` > `Organization configuration` > `SMTP server configuration`. Fill the details that suit your needs best. Ensure to pass the provided "Test Configuration" functionality. 

Key store and algorithm-related fields are pre-populated; these allow delivery of signed e-mails. If you don't want signed e-mails, leave the key store fields empty.

Restart oxauth.

### Custom script

Create a new person authentication script. In oxTrust, visit `Configuration` > `Person authentication scripts` and click on the "add" button. Fill the following:

- name: `email_2fa`
- custom properties
    - name: `otp_length` / value: the number of digits the delivered OTPs will have, e.g. 6
    - name: `otp_lifetime` / value: how long an OTP will be considered valid (in minutes), e.g. 2
- script: use the contents from [here](https://github.com/GluuFederation/casa/raw/master/plugins/email_2fa_core/extras/email_2fa_core.py)
- level: choose a numeric value as per your requirements

Ensure the "Enabled" checkbox is ticked and then submit the form.

### Custom pages

SFTP/SCP the following files to your VM instance (create directories if needed):

|Source|Destination directory (VM)|
|-|-|
|[otp_email.xhtml](https://github.com/GluuFederation/casa/raw/master/plugins/email_2fa_core/extras/otp_email.xhtml)|`/opt/gluu/jetty/oxauth/custom/pages/casa`|
|[otp_email_prompt.xhtml](https://github.com/GluuFederation/casa/raw/master/plugins/email_2fa_core/extras/otp_email_prompt.xhtml)|`/opt/gluu/jetty/oxauth/custom/pages/casa`|
|[oxauth.properties](https://github.com/GluuFederation/casa/raw/master/plugins/email_2fa_core/extras/oxauth.properties)|`/opt/gluu/jetty/oxauth/custom/i18n/`|

### Add the plugin

Use the casa admin dashboard to upload the email plugin:

- Visit casa and navigate to `Administration console` > `Casa Plugins`
- Click on `Add a plugin...` and provide this [jar](https://maven.gluu.org/maven/org/gluu/casa/plugins/email_2fa_core/4.5.5-SNAPSHOT/email_2fa_core-4.5.5-SNAPSHOT-jar-with-dependencies.jar) file if your Gluu Server version is 4.5.4 or higher. If you are in 4.5.3 use this [jar](https://maven.gluu.org/maven/org/gluu/casa/plugins/email_2fa_core/4.5.3.1.Final/email_2fa_core-4.5.3.1.Final-jar-with-dependencies.jar) instead

Alternatively you can copy (SFTP/SCP) the file directly to `/opt/gluu/jetty/casa/plugins`.

If your Gluu version is 4.5.4, please do the following as well:

- Connect to your VM instance (SSH) and `cd` to `/opt/gluu/jetty/casa/webapps`
- Stop casa, e.g. `systemctl stop casa`
- Run `zip -d casa.war WEB-INF/lib/bcutil-jdk18on-1.76.jar`
- Run `mkdir WEB-INF && cd WEB-INF && mkdir lib && cd lib`
- `wget https://repo1.maven.org/maven2/org/bouncycastle/bcutil-jdk18on/1.78.1/bcutil-jdk18on-1.78.1.jar`
- `jar -uf casa.war WEB-INF`
- `rm -rf WEB-INF`
- Start casa

## Associate the new authentication method

Once the plugin was installed (it can take up to one minute), visit the Casa admin dashboard and do the following:

- Click on `Enabled authentication methods`. A table showing a row labelled `email_2fa` should appear
- Tick the row's checkbox and then click on `Save`
- Click on `Back to your credentials`. A new menu item should appear under `2FA credentials` as well as a corresponding widget in the main content area.

## Test

In the main page (user's dashboard) click on `Email 2FA`. If the user already has some e-mails added they should appear listed. In order to add more, simply provide an e-mail and follow the instructions. An OTP code will be sent for validation; note [SMTP](#smtp-configuration) has to be properly setup beforehand.

Back in the main page, ensure to enroll another type of credential. This might require some configurations - check the admin console guide. Finally turn on `Second Factor Authentication` (the big toggle switch in the dashboard) and logout.

Attempt to login again, after entering the username and password combination, the user will have the option to login by entering an OTP delivered to his inbox as a second factor for authentication.
