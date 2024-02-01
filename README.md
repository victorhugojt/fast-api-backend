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

## Open Telemetry

### Jaeger (traces backend)

```sh
    docker run --rm --name jaeger \
      -e COLLECTOR_ZIPKIN_HOST_PORT=:9411 \
      -e COLLECTOR_OTLP_ENABLED=true \
      -p 6831:6831/udp \
      -p 6832:6832/udp \
      -p 5778:5778 \
      -p 16686:16686 \
      -p 4317:4317 \
      -p 4318:4318 \
      -p 14250:14250 \
      -p 14268:14268 \
      -p 14269:14269 \
      -p 9411:9411 \
      jaegertracing/all-in-one:1.49
```

4317, 4318 ports are the default for open telemetry


UI ===> http://localhost:16686


  ##### Running Locally for Dev with Otel

```sh 
opentelemetry-instrument --traces_exporter console, otlp --metrics_exporter none --exporter_otlp_endpoint http://localhost:4317 --service_name greeting-service uvicorn app.main:app
```

# Docs run example

```sh
opentelemetry-instrument \
    --traces_exporter console,otlp \
    --metrics_exporter none \
    --service_name your-service-name \
    --exporter_otlp_endpoint 0.0.0.0:4317 \
    python myapp.py
```
  

