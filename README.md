# Typeform Webhook Processor

## Project Overview

This project is a serverless function designed to process webhooks from Typeform, analyze the responses using the Anthropic API, and store the results in a PostgreSQL database. It's deployed as a DigitalOcean Function.

## Current Setup

- Runtime: Python 3.11
- Deployment: DigitalOcean Functions
- Database: PostgreSQL
- External APIs: Anthropic (for AI-powered analysis)

## Project Structure

```
values-prism/
├── packages/
│   └── typeform-webhook/
│       ├── __main__.py
│       ├── config.py (not in repository)
├── project.yml
|── requirements.txt
└── .gitignore
```

## Current Issues

The main issue we're facing is that the function fails to initialize properly when deployed to DigitalOcean Functions. The error message we're receiving is:

```
Activation Id: 67c64bdeb17644c2864bdeb17604c26a
2024-09-19T01:11:22.293742926Z stderr: Invalid function: No module named 'asyncpg'
```

This error suggests that the `asyncpg` module is not being properly installed or recognized by the DigitalOcean Functions environment.

## Deployment Process

1. Ensure all dependencies are listed in `requirements.txt`.
2. Update `project.yml` if necessary.
3. Deploy using the DigitalOcean CLI:
   ```
   doctl serverless deploy . --verbose
   ```

## Key Files

### __main__.py

This is the main entry point for the function. It handles:
- Webhook data processing
- Database operations
- Interaction with the Anthropic API
- Analysis generation

### requirements.txt

Lists all Python dependencies. Current contents:

```
fastapi==0.68.0
uvicorn==0.15.0
asyncpg==0.25.0
pydantic==1.8.2
anthropic==0.2.8
python-multipart==0.0.5
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
```

### project.yml

Configures the DigitalOcean Function:

```yaml
packages:
  - name: typeform-webhook
    functions:
      - name: __main__
        runtime: 'python:3.11'
        main: '__main__.py'
```

## Troubleshooting Steps Taken

1. Verified that `asyncpg` is listed in `requirements.txt`.
2. Checked that the Python version (3.11) is correctly specified in `project.yml`.
3. Attempted to deploy with the `--clean` flag to ensure a fresh build.

## Objectives

1. Resolve the `asyncpg` import error.
2. Ensure the function deploys and runs successfully on DigitalOcean Functions.
3. Verify that all dependencies are correctly installed in the DigitalOcean Functions environment.
4. Optimize the code for DigitalOcean Functions if necessary.

## Testing

To test the function locally:

1. Set up a local Python 3.11 environment.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the function with mock webhook data.

To test on DigitalOcean after deployment:

1. Use the DigitalOcean Functions console to invoke the function.
2. Check the logs for any error messages.

## Notes

- The `config.py` file contains sensitive information and is not included in the repository.
- Environment variables for database connection and API keys should be set in the DigitalOcean Functions environment.

## Reporting

Please document:
1. All changes made and the rationale behind them.
2. Any new dependencies introduced.
3. Potential long-term implications of the changes.
4. Recommendations for future optimization.

```
