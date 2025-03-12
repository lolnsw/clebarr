# Clebarr

A FastAPI-based Plex Media Server management application.

## Configuration

1. Copy the template configuration file:
```bash
cp config/config.template.yaml config/config.yaml
```

2. Edit `config/config.yaml` to set your Plex server URL.

3. Set up environment variables:

Copy the environment template file:
```bash
cp .env.template .env
```

Edit `.env` and set your configuration:
```bash
# Required
PLEX_TOKEN="your-plex-token-here"  # Your Plex authentication token

# Optional (can also be set in config.yaml)
PLEX_SERVER_URL="http://localhost:32400"  # Your Plex server URL
ENV="development"  # development, production, testing
LOG_LEVEL="INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

You can also set these as system environment variables:
```bash
export PLEX_TOKEN="your-plex-token-here"
export PLEX_SERVER_URL="http://localhost:32400"
```

Note: Never commit your actual Plex token, `.env` file, or `config/config.yaml` to version control!

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| PLEX_TOKEN | Yes | - | Your Plex authentication token |
| PLEX_SERVER_URL | No | From config.yaml | URL of your Plex server |
| ENV | No | development | Application environment |
| LOG_LEVEL | No | From config.yaml | Logging level |

## Development

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the development server:
```bash
uvicorn app.main:app --reload
```

## Testing

Run tests with:
```bash
python -m pytest tests/
```

The test suite uses a separate configuration file at `tests/config/config.yaml`.

## API Documentation

Once the server is running, you can access:
- Interactive API docs (Swagger UI): http://localhost:8000/docs
- Alternative API docs (ReDoc): http://localhost:8000/redoc 