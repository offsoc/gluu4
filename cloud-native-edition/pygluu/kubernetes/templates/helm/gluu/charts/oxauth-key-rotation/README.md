# oxauth-key-rotation

![Version: 1.8.40](https://img.shields.io/badge/Version-1.8.40-informational?style=flat-square) ![Type: application](https://img.shields.io/badge/Type-application-informational?style=flat-square) ![AppVersion: 4.5.7](https://img.shields.io/badge/AppVersion-4.5.7-informational?style=flat-square)

Responsible for regenerating auth-keys per x hours

**Homepage:** <https://gluu.org/docs/gluu-server>

## Maintainers

| Name | Email | Url |
| ---- | ------ | --- |
| Mohammad Abudayyeh | <support@gluu.org> | <https://github.com/moabu> |

## Source Code

* <https://github.com/GluuFederation/docker-certmanager>
* <https://github.com/GluuFederation/gluu4/tree/4.5/cloud-native-edition>

## Requirements

Kubernetes: `>=v1.22.0-0`

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| additionalAnnotations | object | `{}` | Additional annotations that will be added across all resources  in the format of {cert-manager.io/issuer: "letsencrypt-prod"}. key app is taken |
| additionalLabels | object | `{}` | Additional labels that will be added across all resources definitions in the format of {mylabel: "myapp"} |
| affinity | object | `{}` |  |
| cronJobSchedule | string | `""` | Auth server key rotation job schedule. It accepts any Cron syntax supported by Kubernetes. If empty, the schedule will run based on keysLife value. |
| customScripts | list | `[]` | Add custom scripts that have been mounted to run before the entrypoint. |
| dnsConfig | object | `{}` | Add custom dns config |
| dnsPolicy | string | `""` | Add custom dns policy |
| image.pullPolicy | string | `"IfNotPresent"` | Image pullPolicy to use for deploying. |
| image.pullSecrets | list | `[]` | Image Pull Secrets |
| image.repository | string | `"gluufederation/certmanager"` | Image  to use for deploying. |
| image.tag | string | `"4.5.7_dev"` | Image  tag to use for deploying. |
| keysLife | int | `48` | Auth server key rotation keys life in hours. |
| keysPushDelay | int | `0` | Delay (in seconds) before pushing private keys to Auth server |
| keysPushStrategy | string | `"NEWER"` | Set key selection strategy after pushing private keys to Auth server (only takes effect when keysPushDelay value is greater than 0) |
| keysStrategy | string | `"NEWER"` | Set key selection strategy used by Auth server |
| lifecycle | object | `{}` |  |
| nodeSelector | object | `{}` |  |
| resources | object | `{"limits":{"cpu":"300m","memory":"300Mi"},"requests":{"cpu":"300m","memory":"300Mi"}}` | Resource specs. |
| resources.limits.cpu | string | `"300m"` | CPU limit. |
| resources.limits.memory | string | `"300Mi"` | Memory limit. |
| resources.requests.cpu | string | `"300m"` | CPU request. |
| resources.requests.memory | string | `"300Mi"` | Memory request. |
| tolerations | list | `[]` |  |
| usrEnvs | object | `{"normal":{},"secret":{}}` | Add custom normal and secret envs to the service |
| usrEnvs.normal | object | `{}` | Add custom normal envs to the service variable1: value1 |
| usrEnvs.secret | object | `{}` | Add custom secret envs to the service variable1: value1 |
| volumeMounts | list | `[]` | Configure any additional volumesMounts that need to be attached to the containers |
| volumes | list | `[]` | Configure any additional volumes that need to be attached to the pod |
