# oxpassport

![Version: 4.5.6](https://img.shields.io/badge/Version-4.5.6-informational?style=flat-square) ![Type: application](https://img.shields.io/badge/Type-application-informational?style=flat-square) ![AppVersion: 4.5.6](https://img.shields.io/badge/AppVersion-4.5.6-informational?style=flat-square)

Gluu interface to Passport.js to support social login and inbound identity.

**Homepage:** <https://gluu.org/docs/gluu-server>

## Maintainers

| Name | Email | Url |
| ---- | ------ | --- |
| Mohammad Abudayyeh | <support@gluu.org> | <https://github.com/moabu> |

## Source Code

* <https://github.com/GluuFederation/gluu4/tree/4.5/cloud-native-edition>

## Requirements

Kubernetes: `>=v1.22.0-0`

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| additionalAnnotations | object | `{}` | Additional annotations that will be added across all resources  in the format of {cert-manager.io/issuer: "letsencrypt-prod"}. key app is taken |
| additionalLabels | object | `{}` | Additional labels that will be added across all resources definitions in the format of {mylabel: "myapp"} |
| affinity | object | `{}` |  |
| customScripts | list | `[]` | Add custom scripts that have been mounted to run before the entrypoint. |
| dnsConfig | object | `{}` | Add custom dns config |
| dnsPolicy | string | `""` | Add custom dns policy |
| fullnameOverride | string | `""` |  |
| hpa | object | `{"behavior":{},"enabled":true,"maxReplicas":10,"metrics":[],"minReplicas":1,"targetCPUUtilizationPercentage":50}` | Configure the HorizontalPodAutoscaler |
| hpa.behavior | object | `{}` | Scaling Policies |
| hpa.metrics | list | `[]` | metrics if targetCPUUtilizationPercentage is not set |
| image.pullPolicy | string | `"IfNotPresent"` | Image pullPolicy to use for deploying. |
| image.pullSecrets | list | `[]` | Image Pull Secrets |
| image.repository | string | `"gluufederation/oxpassport"` | Image  to use for deploying. |
| image.tag | string | `"4.5.6-1"` | Image  tag to use for deploying. |
| lifecycle | object | `{}` |  |
| livenessProbe | object | `{"exec":{"command":["python3","/app/scripts/healthcheck.py"]},"failureThreshold":20,"initialDelaySeconds":30,"periodSeconds":30,"timeoutSeconds":5}` | Configure the liveness healthcheck for oxPassport if needed. |
| nameOverride | string | `""` |  |
| nodeSelector | object | `{}` |  |
| readinessProbe | object | `{"exec":{"command":["python3","/app/scripts/healthcheck.py"]},"failureThreshold":20,"initialDelaySeconds":25,"periodSeconds":25,"timeoutSeconds":5}` | Configure the readiness healthcheck for the oxPassport if needed. |
| replicas | int | `1` | Service replica number |
| resources | object | `{"limits":{"cpu":"700m","memory":"900Mi"},"requests":{"cpu":"700m","memory":"900Mi"}}` | Resource specs. |
| resources.limits.cpu | string | `"700m"` | CPU limit. |
| resources.limits.memory | string | `"900Mi"` | Memory limit. |
| resources.requests.cpu | string | `"700m"` | CPU request. |
| resources.requests.memory | string | `"900Mi"` | Memory request. |
| service.name | string | `"http-passport"` | The name of the oxPassport port within the oxPassport service. Please keep it as default. |
| service.oxPassportServiceName | string | `"oxpassport"` | Name of the oxPassport service. Please keep it as default. |
| service.port | int | `8090` | Port of the oxPassport service. Please keep it as default. |
| service.sessionAffinity | string | `"None"` | Default set to None If you want to make sure that connections from a particular client are passed to the same Pod each time, you can select the session affinity based on the client's IP addresses by setting this to ClientIP |
| service.sessionAffinityConfig | object | `{"clientIP":{"timeoutSeconds":10800}}` | the maximum session sticky time if sessionAffinity is ClientIP |
| tolerations | list | `[]` |  |
| tolerations | list | `[]` | https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/ |
| usrEnvs | object | `{"normal":{},"secret":{}}` | Add custom normal and secret envs to the service |
| usrEnvs.normal | object | `{}` | Add custom normal envs to the service variable1: value1 |
| usrEnvs.secret | object | `{}` | Add custom secret envs to the service variable1: value1 |
| volumeMounts | list | `[]` | Configure any additional volumesMounts that need to be attached to the containers |
| volumes | list | `[]` | Configure any additional volumes that need to be attached to the pod |
