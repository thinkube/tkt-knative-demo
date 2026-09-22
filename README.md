# tkt-knative-demo

A Thinkube app template: a minimal Knative service that scales to zero.

## What it does

- Starts an HTTP server on port 8080
- Returns a configurable greeting at `/`
- Provides a health endpoint at `/health` with uptime and request count
- Has a `/scale-test` endpoint for load testing autoscaling
- Simulates configurable processing delay per request
- Answers any other path with HTTP 404

## How it reaches a user

A person deploys it from the Templates page in thinkube-control, part of
[Thinkube](https://github.com/thinkube/thinkube). It needs the Knative
optional component. It is not installed on its own.

thinkube-control also uses it as a test fixture:
`backend/tests/test_knative_service.py` renders a Knative Service from the
container this template declares.

The walkthrough (deploy it, call it while stopped, watch it scale and return
to zero, change the greeting) is on the documentation site:
[Deploy a serverless service](https://thinkube.github.io/thinkube.org/thinkube-docs/playbooks/deploy-a-service-that-scales-to-zero.html).

## Configurable Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GREETING` | Message returned by the service | `Hello from Knative!` |
| `SIMULATE_WORK_MS` | Milliseconds of simulated work per request | `100` |

## Deployment

`thinkube.yaml` deploys it as a Knative service (`type: knative`). The service will:
- Scale to zero when idle (no pods running, `minScale: 0`)
- Scale up on first request (cold start)
- Scale up to 3 pods under load (`maxScale: 3`)
- Handle 5 concurrent requests per pod (`containerConcurrency: 5`)
- Time out a request after 30 seconds (`timeoutSeconds: 30`)

## Working on it

| File | What it is |
|---|---|
| `server.py` | the HTTP server, Python standard library only |
| `Containerfile` | the image, on the platform's `python-base` image |
| `thinkube.yaml` | the Knative deployment and the two variables |
| `manifest.yaml` | the template metadata |

## License

MIT. Code generated from this template is yours: no attribution required, and you may license the app you build however you choose. See [LICENSE](LICENSE).

Copyright Alejandro Martínez Corriá and the Thinkube contributors
