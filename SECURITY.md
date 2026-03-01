# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability within this library, please send an email to hello@sinkron.id. All security vulnerabilities will be promptly addressed.

## Security Best Practices

### Token Handling

- Never hardcode tokens in source code
- Use environment variables or config files for token storage
- The library automatically saves tokens to `~/.sinkron.json` when using `--save-token`
- Clear tokens when no longer needed

### API Security

- The library uses HTTPS by default for all API connections
- Bearer token authentication is used for protected endpoints
- Tokens are sent in the Authorization header

### Input Validation

- Username validation: 4-25 lowercase alphanumeric characters
- Maximum 25 messages can be deleted at once
- All inputs are validated before sending to API

## Dependency Security

This library depends on:
- `requests` - HTTP library with security features enabled

Report any security concerns to hello@sinkron.id
