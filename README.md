# fast-api-backend
fastAPI self training

# build image
docker build -t greetings-backend .

# run docker container locally
docker-compose up -d

# Use the minikube docker-env for the current session.
eval $(minikube docker-env)

# Create resources
kubectl apply -f service.yaml
kubectl apply -f deployment.yamls

# Use postman collection to test the app
fastAPIContenerized.postman_collection.json

