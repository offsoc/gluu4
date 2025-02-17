# fido2

![Version: 1.8.40](https://img.shields.io/badge/Version-1.8.40-informational?style=flat-square) ![Type: application](https://img.shields.io/badge/Type-application-informational?style=flat-square) ![AppVersion: 4.5.7](https://img.shields.io/badge/AppVersion-4.5.7-informational?style=flat-square)

FIDO 2.0 (FIDO2) is an open authentication standard that enables leveraging common devices to authenticate to online services in both mobile and desktop environments.

**Homepage:** <https://gluu.org/docs/gluu-server/>

## Maintainers

| Name | Email | Url |
| ---- | ------ | --- |
| Mohammad Abudayyeh | <support@gluu.org> | <https://github.com/moabu> |

## Source Code

* <https://gluu.org/docs/gluu-server/>
* <https://github.com/GluuFederation/gluu4/tree/4.5/cloud-native-edition>

## Requirements

Kubernetes: `>=v1.22.0-0`

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| additionalAnnotations | object | `{}` | Additional annotations that will be added across all resources  in the format of {cert-manager.io/issuer: "letsencrypt-prod"}. key app is taken |
| additionalLabels | object | `{}` | Additional labels that will be added across all resources definitions in the format of {mylabel: "myapp"} |
| affinity | object | `{}` | https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/ |
| customScripts | list | `[]` | Add custom scripts that have been mounted to run before the entrypoint. |
| dnsConfig | object | `{}` | Add custom dns config |
| dnsPolicy | string | `""` | Add custom dns policy |
| hpa | object | `{"behavior":{},"enabled":true,"maxReplicas":10,"metrics":[],"minReplicas":1,"targetCPUUtilizationPercentage":50}` | Configure the HorizontalPodAutoscaler |
| hpa.behavior | object | `{}` | Scaling Policies |
| hpa.metrics | list | `[]` | metrics if targetCPUUtilizationPercentage is not set |
| image.pullPolicy | string | `"IfNotPresent"` | Image pullPolicy to use for deploying. |
| image.pullSecrets | list | `[]` | Image Pull Secrets |
| image.repository | string | `"gluufederation/fido2"` | Image  to use for deploying. |
| image.tag | string | `"4.5.7_dev"` | Image  tag to use for deploying. |
| lifecycle | object | `{}` |  |
| livenessProbe | object | `{"exec":{"command":["python3","/app/scripts/healthcheck.py"]},"initialDelaySeconds":25,"periodSeconds":25,"timeoutSeconds":5}` | Configure the liveness healthcheck for the fido2 if needed. |
| nodeSelector | object | `{}` |  |
| readinessProbe | object | `{"exec":{"command":["python3","/app/scripts/healthcheck.py"]},"initialDelaySeconds":30,"periodSeconds":30,"timeoutSeconds":5}` | Configure the readiness healthcheck for the fido2 if needed. |
| replicas | int | `1` | Service replica number. |
| resources | object | `{"limits":{"cpu":"500m","memory":"500Mi"},"requests":{"cpu":"500m","memory":"500Mi"}}` | Resource specs. |
| resources.limits.cpu | string | `"500m"` | CPU limit. |
| resources.limits.memory | string | `"500Mi"` | Memory limit. |
| resources.requests.cpu | string | `"500m"` | CPU request. |
| resources.requests.memory | string | `"500Mi"` | Memory request. |
| service.fido2ServiceName | string | `"fido2"` | Name of the fido2 service. Please keep it as default. |
| service.name | string | `"http-fido2"` | The name of the fido2 port within the fido2 service. Please keep it as default. |
| service.port | int | `8080` | Port of the fido2 service. Please keep it as default. |
| service.sessionAffinity | string | `"None"` | Default set to None If you want to make sure that connections from a particular client are passed to the same Pod each time, you can select the session affinity based on the client's IP addresses by setting this to ClientIP |
| service.sessionAffinityConfig | object | `{"clientIP":{"timeoutSeconds":10800}}` | the maximum session sticky time if sessionAffinity is ClientIP |
| tolerations | list | `[]` | https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/ |
| usrEnvs | object | `{"normal":{},"secret":{}}` | Add custom normal and secret envs to the service |
| usrEnvs.normal | object | `{}` | Add custom normal envs to the service variable1: value1 |
| usrEnvs.secret | object | `{}` | Add custom secret envs to the service variable1: value1 |
| volumeMounts | list | `[]` | Configure any additional volumesMounts that need to be attached to the containers |
| volumes | list | `[]` | Configure any additional volumes that need to be attached to the pod |
