# tkt-knative-demo

Minimal Knative scale-to-zero demo template for testing thinkube deployments.

## What it does

- Starts an HTTP server on port 8080
- Returns a configurable greeting at `/`
- Provides a health endpoint at `/health` with uptime and request count
- Has a `/scale-test` endpoint for load testing autoscaling
- Simulates configurable processing delay per request

## Configurable Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GREETING` | Message returned by the service | `Hello from Knative!` |
| `SIMULATE_WORK_MS` | Milliseconds of simulated work per request | `100` |

## Deployment

Deploy via thinkube-control. The service will:
- Scale to zero when idle (no pods running)
- Scale up on first request (cold start)
- Scale up to 3 pods under load (`maxScale: 3`)
- Handle 5 concurrent requests per pod (`containerConcurrency: 5`)

## Testing scale-to-zero

```bash
# After deploying, wait ~60 seconds for scale-to-zero
kubectl get pods -n knative-demo

# Send a request — should cold-start a pod
curl https://knative-demo.cmxela.com/

# Send parallel requests to test scaling
for i in $(seq 1 20); do
  curl -s https://knative-demo.cmxela.com/scale-test &
done
wait

# Check how many pods were created
kubectl get pods -n knative-demo
```
