# Deploying Cardinal on Kubernetes

### Usage
You can run Cardinal on Kubernetes using the YAML specs defined in this directory. The YAML specs defined in this
directory were initially created using [move2kube](https://move2kube.konveyor.io/).

Some of the YAML specs will need configuration prior to deployment. Information like a pull secret (container registry)
will be needed, specifically for fetching Cardinal's container image.

Once you have all of the necessary information configured within the YAML specs, execute the following command
from the source directory to deploy. Please be sure to execute on a Kubernetes node:

```
kubectl apply -f deploy
```

### Questions?
If you have any feedback or difficulties using this deployment, please open an [issue report](https://github.com/cardinal-dev/Cardinal/issues).