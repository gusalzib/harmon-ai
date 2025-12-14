# A bunch of potentially useful stuff
## Installing Minikube for local Kubernetes deployment FOR LINUX
### Download Linux binaries
```curl -LO https://github.com/kubernetes/minikube/releases/download/v1.37.0/minikube-linux-amd64```

### Install and remove download stuff(????)
```sudo install minikube-linux-amd64 /usr/local/bin/minikube && rm minikube-linux-amd64```

### Launching minikube with Docker
```minikube start --driver=docker```
### Or to set as default driver
```minikube config set driver docker```

### Installing kubectl, while minikube container is running
```minikube kubectl```

## Useful commands
Applying a configuration:
```
minikube kubectl -- apply -f filename.yaml
```

Some awareness commands:
```
minikube status
minikube kubectl -- get pods
minikube kubectl -- get all
```

Super duper awareness command (after the dump, open file and Ctrl + F "reason"):
```
minikube kubectl -- cluster-info dump > log-dump.txt
```

"Giving an image" to minikube, and checking available images:
```
minikube image load image-name:tag
minikube image ls
```

Get logs for a specific pod:
```
minikube kubectl -- logs -p users-app-deployement-557b5c56fd-wphrj
```

## Image Requirements
**List of valid image tags**
*If you don't use these imagetags with minikube, the images won't be used*
- harmonai-client:latest
- users-proj:latest
    - Requires .env with DB_CONNECTION_STRING
- prediction-proj:latest
- training-proj:latest
    - Requires HarmonAi_storage.json containing Google Application Credentials (ask Viktor)

Should be able to run each image locally with `docker run --rm -p <port>:<port> name:tag`

# Gateway API
Fuck the Gateway API

# "Regular Ingress"
- You must have an Ingress controller to satisfy an Ingress
- Whole-ass minikube-specific nginx guide that is easy to follow: https://v1-33.docs.kubernetes.io/docs/tasks/access-application-cluster/ingress-minikube/

Apply ingress to make life good:
```minikube kubectl -- apply -f deployment/nginx-ingress.yaml```

Confirm all is well. Should show IPv4 address after a minute of applying:
```minikube kubectl -- get ingress```

If running in e.g. WSL2, use this to expose to Windows:
```minikube tunnel```
```URL for browser, example: http://locahost/users/is-db-connected```

If that doesn't work the first time, then:
```sudo minikube tunnel; minikube tunnel```