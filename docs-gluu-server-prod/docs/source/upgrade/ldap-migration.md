# Overview

This documentation demonstrates how to upgrade a Kubernetes setup of Gluu >=4.2 LDAP to 4.5 PostgreSQL.

## Prerequisites

  Assuming Gluu 4.2 is already installed and running, do the following steps:

  1. scale down the OpenDJ replicas to 1 pod.
  1. Backup the persistence volumes as the upgrade process is not reversible.
  1. Backup the existing `values.yaml` used in Gluu 4.2 installation as `values-4.2.yaml`.

  Additional steps are required if using LDAP with multiCluster enabled(for example WEST and EAST regions):

  1. upgrade only in 1 region, e.g. WEST
  1. disable Opendj replication between WEST and EAST
  1. disable traffic to WEST

## How to upgrade and migrate

### Step 1: Upgrading Gluu 4.2 to 4.5 with OpenDJ/LDAP as persistence

1.  Change the ownership of the Opendj filesystem: 

    `kubectl -n <namespace> exec <opendj-pod-name> -- chown -R 1000:root /opt/opendj`


1.  Edit the manifest of the current OpenDJ statefulset:
    `kubectl edit sts <opendj-sts-name> -n <namespace>` 

    Upgrade the image tag to `4.5.5-x` and add a new env variable:

    ```
    containers:
      - image: gluufederation/opendj:4.5.5-1
        env:
          - name: GLUU_LDAP_AUTO_REPLICATE
            value: "false"
    ```

    Save the changes and wait until the opendj pod gets terminated, re-deployed, and running.


1.  Make sure that the completed `gluu-config` and `gluu-persistence` jobs are deleted. 

1.  Create `gluu-upgrade-42.yaml` file:
    ```
    apiVersion: batch/v1
    kind: Job
    metadata:
      name: gluu-upgrade-42
    spec:
      template:
        metadata:
          annotations:
            sidecar.istio.io/inject: "false"                  
        spec:
          restartPolicy: Never
          imagePullSecrets:
            - name: regcred
          volumes: []
          containers:
            - name: upgrade-42
              image: gluufederation/upgrade:4.5.5-1
              volumeMounts: []
              envFrom:
                - configMapRef:
                    name: gluu-config-cm # adjust the name according to your setup
              env: []
              args:
                - --source=4.2
                - --target=4.5    
    ```

1.  Apply the job to upgrade the OpenDJ entries:

    `kubectl -n <namespace> apply -f gluu-upgrade-42.yaml`

1.  Wait until the job is completed succesfully, and then delete the job:

    `kubectl -n <namespace> delete -f gluu-upgrade-42.yaml`


1.  Make sure the cluster functions after the upgrade job.

### Step 2: migrate the OpenDJ entries to Postgres

1.  Export entries for each tree (`o=gluu`, `o=site`, `o=metric`) as `.ldif` file.

    ```
    mkdir -p custom_ldif
    kubectl -n <namespace> exec -ti <opendj-pod> -- /opt/opendj/bin/ldapsearch -D "cn=directory manager" -p 1636 --useSSL -w <ldap-password> --trustAll -b "o=gluu" -s sub objectClass=* > custom_ldif/01_gluu.ldif

    kubectl -n <namespace> exec -ti <opendj-pod> -- /opt/opendj/bin/ldapsearch -D "cn=directory manager" -p 1636 --useSSL -w <ldap-password> --trustAll -b "o=site" -s sub objectClass=* > custom_ldif/02_site.ldif
    
    kubectl -n <namespace> exec -ti <opendj-pod> -- /opt/opendj/bin/ldapsearch -D "cn=directory manager" -p 1636 --useSSL -w <ldap-password> --trustAll -b "o=metric" -s sub objectClass=* > custom_ldif/03_metric.ldif
    ```
    
1.  Create configmaps for each `.ldif` file if each file below 1MB:

    ```
    kubectl -n <namespace> create cm custom-gluu-ldif --from-file=custom_ldif/01_gluu.ldif
    kubectl -n <namespace> create cm custom-site-ldif --from-file=custom_ldif/02_site.ldif
    kubectl -n <namespace> create cm custom-metric-ldif --from-file=custom_ldif/03_metric.ldif
    ```
    
    
1.  Prepare Postgres database for migration (e.g. using Helm chart):

    ```
    kubectl create ns postgres
    helm repo add bitnami https://charts.bitnami.com/bitnami
    helm install postgresql --set auth.rootPassword=<postgres-root-password>,auth.database=gluu,auth.username=gluu,auth.password=<postgres-user-password> bitnami/postgresql -n postgres
    ```
    
    Take notes about the values above as we will need them in next sections.
    
1.  Migrating entries from `.ldif` files may take a while, hence we will be migrating them offline using a separate k8s job.

    1.  Create a `sql_password` file to store the password for Postgres user and save it into a secret:

        ```
        kubectl -n <namespace> create secret generic offline-sql-pass --from-file=sql_password
        ```
    
    1.  Create `offline-persistence-load.yaml`:
    
        ```yaml
        apiVersion: batch/v1
        kind: Job
        metadata:
          name: offline-persistence-load
        spec:
          template:
            metadata:
              annotations:
                sidecar.istio.io/inject: "false"                  
            spec:
              restartPolicy: Never
              imagePullSecrets:
                - name: regcred
              volumes:
                - name: custom-gluu-ldif
                  configMap:
                    name: custom-gluu-ldif
                - name: custom-site-ldif
                  configMap:
                    name: custom-site-ldif
                - name: custom-metric-ldif
                  configMap:
                    name: custom-metric-ldif
                - name: sql-pass
                  secret:
                    secretName: offline-sql-pass # adjust the value according to your setup
              containers:
                - name: offline-persistence-load
                  image: gluufederation/persistence:4.5.5-1
                  volumeMounts:
                    - name: custom-gluu-ldif
                      mountPath: /app/custom_ldif/01_gluu.ldif
                      subPath: 01_gluu.ldif
                    - name: custom-site-ldif
                      mountPath: /app/custom_ldif/02_site.ldif
                      subPath: 02_site.ldif
                    - name: custom-metric-ldif
                      mountPath: /app/custom_ldif/03_metric.ldif
                      subPath: 03_metric.ldif
                    - name: sql-pass
                      mountPath: "/etc/gluu/conf/sql_password"
                      subPath: sql_password
                  envFrom:
                    - configMapRef:
                        name: gluu-config-cm # adjust the name according to your setup
                  env:
                    - name: GLUU_PERSISTENCE_IMPORT_BUILTIN_LDIF
                      value: "false" # [DONT CHANGE] skip builtin LDIF files generated by the image container
                    - name: GLUU_PERSISTENCE_TYPE
                      value: "sql" # [DONT CHANGE]
                    - name: GLUU_SQL_DB_DIALECT
                      value: "pgsql" # [DONT CHANGE]
                    - name: GLUU_SQL_DB_NAME
                      value: "gluu" # adjust according to your setup
                    - name: GLUU_SQL_DB_HOST
                      value: "postgresql.postgres.svc.cluster.local" # adjust according to your setup
                    - name: GLUU_SQL_DB_PORT
                      value: "5432" # adjust according to your setup
                    - name: GLUU_SQL_DB_USER
                      value: "gluu" # adjust according to your setup
                    - name: GLUU_SQL_DB_SCHEMA
                      value: "public" # [default value] adjust according to your setup
        ```
    
    If the ldif file is larger then 1MB:

    1.  Create a file named `mycustomldif.sh` which basically  contains instructions to pull the ldif file:

        ```
           #!/bin/sh
           # This script will pull the ldif file from a remote location
           # and place it in the correct location for the Persistence job to use it
           mkdir -p /app/custom_ldif 
           wget -O /app/custom_ldif/01_gluu.ldif https://<ldif-file-location/01_gluu.ldif
        ```

    1.  Create a configmap:
        `kubectl -n <namespace> create cm my-custom-ldif --from-file=mycustomldif.sh`

    1.  Edit the job yaml to mount the configmap:
       
        ```
          volumes:
            - name: my-custom-ldif
              configMap:
                defaultMode: 493
                name: my-custom-ldif    
          containers: 
            - name: offline-persistence-load
              command:
              - tini
              - -g
              - --
              - /bin/sh
              - -c
              - |
                /tmp/mycustomldif.sh
                /app/scripts/entrypoint.sh
              image: gluufederation/persistence:4.5.5-1
              volumeMounts:
                - name: my-custom-ldif
                  mountPath: /tmp/mycustomldif.sh
                  subPath: mycustomldif.sh
        ```       
    
  1.  Deploy the job:

      ```
      kubectl -n <namespace> apply -f offline-persistence-load.yaml
      ```
    
  1.  Make sure there's no error while running the job before proceeding to the next step. If there's no error, the job and secret can be deleted safely:

      ```
      kubectl -n <namespace> delete secret offline-sql-pass
      kubectl -n <namespace> delete job offline-persistence-load
      ```
        
### Step 3: switching from OpenDJ to Postgres


1.  Get new `values.yaml` for Gluu 4.5 installation.

1.  Compare `values-4.2.yaml` with the new `values.yaml`, and then modify `values.yaml`

1.  Switch the persistence from Opendj to Postgres by adding the following to the existing `values.yaml`:

    ```yaml
    global:
      gluuPersistenceType: sql
      upgrade:
        enabled: false
      opendj:
        enabled: false  
    config:
      configmap:
        cnSqlDbName: gluu # adjust according to your setup
        cnSqlDbPort: 5432 # adjust according to your setup
        cnSqlDbDialect: pgsql
        cnSqlDbHost: postgresql.postgres.svc # adjust according to your setup
        cnSqlDbUser: gluu # adjust according to your setup
        cnSqlDbTimezone: UTC
        cnSqldbUserPassword: <postgres-user-password> # adjust according to your setup
    ```
    
1.  Run `helm upgrade <gluu-release-name> gluu/gluu -n <namespace> -f values.yaml`.

1.  Make sure the cluster is functioning after the migration.

## Known Issues

1.  Since 4.2 uses the deprecated `v1beta1` API version. When upgrading, you'll receive the following error: 
    `ensure CRDs are installed first, resource mapping not found for name: "gluu-nginx-ingress-casa" namespace: "" from "": no matches for kind "Ingress" in version "networking.k8s.io/v1beta1`.

    You can follow [this](https://helm.sh/docs/topics/kubernetes_apis/#updating-api-versions-of-a-release-manifest) to resolve this Ingress API version incompatibility error. 
    
    You can resolve it using the `mapkubeapis` helm plugin by running the following: 
    
    `helm mapkubeapis <gluu-release-name> -n <namespace>`.


1.  During the upgrade from >=4.2 to 4.5, if you didn't delete the jobs as instructed, the helm command throws the following message:

    ```
    Error: UPGRADE FAILED: cannot patch "gluu-config" with kind Job: Job.batch "gluu-config" is invalid: spec.template: 
    Invalid value: core.PodTemplateSpec{ObjectMeta:v1.ObjectMeta{Name:"config-job", GenerateName:"", Namespace:""
    ```

    The upgrade itself is running though.

    If you faced this, you should switch `global.upgrade.enabled: false` and rerun the `helm upgrade` command again, so that it’s registered with the helm lifecycle that the upgrade was successful.
    
1.  Interception scripts are not upgraded automatically. They need to be upgraded manually.
