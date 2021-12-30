# fast-api-backend
fastAPI self training

# build image
docker build -t greetings-backend .

# run docker container locally
docker-compose up -d

# KUBERNETES

# Use the minikube docker-env for the current session.
eval $(minikube docker-env)

## start default cluster
minikube start

# Create resources
kubectl apply -f service.yaml
kubectl apply -f deployment.yamls

## Enable the load balancer (service) external ip (pending). Separate terminal

minikube tunnel

# Use postman collection to test the app
fastAPIContenerized.postman_collection.json

