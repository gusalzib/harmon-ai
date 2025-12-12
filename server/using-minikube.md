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




