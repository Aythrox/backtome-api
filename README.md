# Backtome API

This repository contains the backend API for **Backtome**, built with Serverless Framework, Python 3.12, and AWS DynamoDB using a Feature-Driven MVC Architecture.

## Prerequisites

- **Node.js** (v18 or v20 recommended)
- **Python 3.12** (Ensure `python3.12` is available in your PATH)
- **AWS CLI** configured (`aws configure`)

## 1. Setup Python Virtual Environment

Before deploying or running locally, it is best practice to set up a Python virtual environment to manage dependencies.

```bash
# 1. Navigate to the API directory
cd backtome-api

# 2. Create a virtual environment using Python 3.12
python3.12 -m venv .venv

# 3. Activate the virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
# .venv\Scripts\activate

# 4. Install the Python dependencies
pip install -r requirements.txt
```

## 2. Install Node Dependencies (Serverless Plugins)

This project relies on the Serverless Framework and the `serverless-python-requirements` plugin to bundle your Python dependencies cleanly.

```bash
# Install the Node packages
npm install
```

## 3. Deploying

We have configured `package.json` scripts to easily deploy the API to different environments using our local version of Serverless Framework v3.

### Deploy to Development
```bash
npm run deploy:dev
```

### Deploy to Production
```bash
npm run deploy:prod
```

If you ever need to remove the stack entirely from AWS:
```bash
npx serverless@3 remove --stage dev
```

## Troubleshooting

### Pyenv: `python3.12: command not found`
If you are using `pyenv` to manage Python versions and encounter a "command not found" error when creating your virtual environment (even though `3.12.x` is installed), you need to set the local Python version for this directory so `pyenv` knows which executable to run.

```bash
# Set the local python version (replace 3.12.9 with your installed 3.12.x version)
pyenv local 3.12.9

# Now 'python' will automatically point to the correct version!
python -m venv .venv
```
