# Sinkron Python Library

Python library and CLI for Sinkron API - Give your agent permanent email addresses through Clawhub.

## Features

- **Full API Support**: Access all Sinkron API endpoints
- **CLI Interface**: Easy-to-use command line tool
- **Configuration Management**: Save tokens and API URLs
- **Input Validation**: Robust validation for all inputs
- **Error Handling**: Detailed error messages
- **Modular Design**: Use as a library or CLI

## Installation

### From source

```bash
cd library
pip install -e .
```

### From PyPI (when published)

```bash
pip install sinkron
```

## Quick Start

### Using CLI

```bash
# Register a new agent
sinkron register --username john --name "John Doe" --save-token

# Check your inbox
sinkron inbox

# Check a specific page
sinkron inbox --page 2

# Search messages
sinkron inbox --search "verification"

# Get a specific message
sinkron message 123

# Check if email exists
sinkron check john@sinkron.id

# Delete messages
sinkron delete-messages --ids 1,2,3

# Delete entire inbox
sinkron delete-inbox

# Get agent info
sinkron agent john

# Config management
sinkron config --show
sinkron config --token YOUR_TOKEN
sinkron config --api-url https://api.sinkron.id
```

### Using as Library

```python
from sinkron import SinkronClient

# Initialize client
client = SinkronClient()

# Register new agent
result = client.register("john", "John Doe")
print(f"Token: {result.token}")

# Set token for authenticated requests
client.token = result.token

# Get inbox
inbox = client.get_inbox(page=1)
print(f"Total messages: {inbox.total}")

# Get specific message
message = client.get_message(123)
print(f"Subject: {message.subject}")

# Check email exists
check = client.check_email("john@sinkron.id")
print(f"Exists: {check.exists}")
```

## Configuration

### Environment Variables

- `SINKRON_API_URL` - API base URL (default: https://api.sinkron.id)
- `SINKRON_TOKEN` - Authentication token

### Config File

The CLI stores configuration in `~/.sinkron.json`:

```json
{
  "api_url": "https://api.sinkron.id",
  "token": "your_token_here"
}
```

### CLI Options

All CLI commands accept these global options:

- `--api-url URL` - Override API URL
- `--token TOKEN` - Override authentication token
- `--version` - Show version

## Local Development

For local development, you can use the Cloudflare Workers local server:

```bash
# Start local development server
cd /home/zororaka/Project/sinkron/be
wrangler dev
```

Then use the local URL in your commands:

```bash
# Register using local server
sinkron register --username john --name "John Doe" --save-token --api-url http://localhost:8787

# Or save the local URL to config
sinkron config --api-url http://localhost:8787
sinkron register --username john --name "John Doe" --save-token
```

### Setting Custom Domain

If you have a custom domain configured:

```bash
sinkron config --api-url https://your-custom-domain.com
```

## API Reference

### Client Methods

| Method | Description | Auth Required |
|--------|-------------|--------------|
| `health_check()` | Check API health | No |
| `register(username, name)` | Register new agent | No |
| `get_agent_info(username)` | Get agent info | Yes |
| `get_inbox(page, search)` | Get inbox messages | Yes |
| `delete_inbox()` | Delete entire inbox | Yes |
| `get_message(id)` | Get message by ID | Yes |
| `delete_messages(ids)` | Delete messages | Yes |
| `check_email(address)` | Check email exists | No |

## CLI Commands

```
sinkron health                              # Check API health
sinkron register --username USER --name NAME # Register new agent
sinkron inbox [--page N] [--search KEYWORD] # Get inbox
sinkron check ADDRESS                       # Check email exists
sinkron message ID                          # Get message
sinkron delete-messages --ids 1,2,3         # Delete messages
sinkron delete-inbox [--force]              # Delete inbox
sinkron agent USERNAME                      # Get agent info
sinkron config --show                       # Show config
sinkron config --token TOKEN                # Set token
sinkron config --clear-token                # Clear token
```

## Error Handling

```python
from sinkron import SinkronClient
from sinkron.exceptions import (
    SinkronError,
    SinkronAuthError,
    SinkronNotFoundError,
    SinkronRateLimitError,
    SinkronValidationError,
)

client = SinkronClient()

try:
    result = client.register("john", "John Doe")
except SinkronValidationError as e:
    print(f"Validation error: {e}")
except SinkronAuthError as e:
    print(f"Auth error: {e}")
except SinkronRateLimitError as e:
    print(f"Rate limited: {e}")
except SinkronError as e:
    print(f"API error: {e}")
```

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black sinkron/

# Lint
flake8 sinkron/
```

## License

MIT License - see LICENSE file for details.

## Links

- Website: https://sinkron.id
- API Documentation: https://docs.sinkron.id
