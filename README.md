# Housing Prices App
Interview task - API endpoint for House price ML inference

## Setup

* `docker-compose up` - build image and run API

Run tests via: `docker-compose exec app uv run pytest`

## Usage

API accessible at: [http://localhost:8000/](http://localhost:8000/)

API docs here: [http://localhost:8000/docs/](http://localhost:8000/docs/)

## Endpoints

* GET `/health`: Health check
* POST `/predict-price`: Get house price
    * Authentication: Bearer Token, default value: `abc`
    * Example JSON payload: 
```json
{
  "longitude": -122.64,
  "latitude": 38.01,
  "housing_median_age": 36.0,
  "total_rooms": 1336.0,
  "total_bedrooms": 258.0,
  "population": 678.0,
  "households": 249.0,
  "median_income": 5.5789,
  "ocean_proximity": "NEAR OCEAN"
}
```

## Development

### Run without Docker

* Create `.env` file with `AUTH_TOKEN` variable.
* Create venv: `uv sync`
* Run API: `uv run housing_prices/app.py`
* Run tests: `uv run pytest`

### Environment variables

Defined in `docker-compose.yml` with these default values:

```ini
AUTH_TOKEN=abc
ENVIRONMENT=local
MODEL_NAME=model.joblib
RATE_LIMIT_PER_MINUTE=10
```

* `AUTH_TOKEN`: Bearer token for authentication
* `ENVIRONMENT`: `local` for pretty printing, `production` for JSON logs
* `MODEL_NAME`: File name from [/models](./models/) folder
* `RATE_LIMIT_PER_MINUTE`: Global rate limiter for requests per minute

You can set `WEB_CONCURRENCY=<N>` to spawn more server workers. 
But in that case the rate limit won't work properly.
This can be fixed by using [Redis backend](https://slowapi.readthedocs.io/en/latest/examples/#use-redis-as-backend-for-the-limiter) for the limiter.

### Requirements

We use [uv](https://docs.astral.sh/uv/) package manager to handle dependencies.

* `uv sync` - create venv
* `uv add <package>` - add new package
* `docker-compose build --no-cache` - recreate the image

### Pre-commit

We use [pre-commit](https://pre-commit.com/) to check and format code.

* `pre-commit install` - install hooks defined in [.pre-commit-config.yaml](./.pre-commit-config.yaml)
* When you commit, your code will be checked by linter and then formatted (by [ruff](https://docs.astral.sh/ruff/)). 
* Ruff settings are located in [pyproject.toml](./pyproject.toml).
* You can also run the hooks manually for all files with `pre-commit run --all-files` or for one file with `pre-commit run --files path/to/file.py`.
* To skip pre-commit, either use `git commit -m 'message' --no-verify` or remove hooks completely via `pre-commit uninstall`.
* **Github CI** contains the pre-commit check (runs for new PR). Example PR with fail [here](https://github.com/jontesek/housing-price-app/pull/2).
