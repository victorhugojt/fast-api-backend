```sh
virtualenv venv
virtualenv -p '/Library/Frameworks/Python.framework/Versions/3.10/bin/python3.10' python-3.10
```

##### Mac
```sh
source python-3.10/bin/activate
```

##### Running Locally for Dev

```sh
uvicorn app.main:app --reload
```

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

