# AWS Lambda Workshop

Run a Python script that processes and exports data from external sources to a Google Sheet on AWS [Lambda](https://aws.amazon.com/lambda/), deployed via AWS [ECR](https://aws.amazon.com/ecr/).


## Workshop prerequisites
- [Python](https://www.python.org) installed on local machine
- [Poetry](https://github.com/python-poetry/poetry) installed on local machine (e.g. via [pip](https://pypi.org/project/pip/))
- [docker desktop](https://docs.docker.com/desktop/) installed on local machine
- Google Cloud access to create service account
- AWS command line with access to to ECR and Lambda

## Workshop Steps

1. Initialize new package
```shell
mkdir lambda-workshop
cd lambda-workshop
poetry init
git init
```

2. Create/copy lambda_function.py, modules/sheet.py, modules/finance.py and .gitginore

3. Create [Google Cloud](https://console.cloud.google.com/) project and service account, generate and download key as JSON file, add file to root folder as google_account.json

4. Create Google Sheet and add edit permission for service account

5. Update the SYMBOL and SHEET_ID environment variables

6. Add dependencies via Poetry
```shell
poetry add yahooquery pandas google-api-python-client
```

7. Test script locally
```shell
poetry run python -c "import lambda_function as lam; lam.lambda_handler()"
```

8. Create/copy Dockerfile

9. Create AWS [ECR](https://eu-west-1.console.aws.amazon.com/ecr/repositories?region=eu-west-1) repository

10. Create AWS [Lambda](https://eu-west-1.console.aws.amazon.com/lambda/home?region=eu-west-1#/functions) function with "lambda-test" execution role and 5 minutes timeout

11. Follow deployment steps below

## App Readme

### Setup

Create virtual environment and install dependencies with Poetry
```shell
poetry install
```

### Run locally

```shell
poetry run python -c "import lambda_function as lam; lam.lambda_handler()"
```

### Deployment (Docker)

1. Authenticate with ECR through AWS CLI
```shell
aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin 880172922216.dkr.ecr.eu-west-1.amazonaws.com
```

2. Build docker image
```shell
docker build -t lambda-workshop . --platform linux/amd64
```

3. Tag image
```shell
docker tag lambda-workshop:latest 880172922216.dkr.ecr.eu-west-1.amazonaws.com/lambda-workshop:latest
```

4. Push image
```shell
docker push 880172922216.dkr.ecr.eu-west-1.amazonaws.com/lambda-workshop:latest
```

5. Update lambda function
```shell
aws lambda update-function-code --region eu-west-1 --function-name lambda-workshop --image-uri 880172922216.dkr.ecr.eu-west-1.amazonaws.com/lambda-workshop:latest
```

6. Set lambda environment variables (from locally sourced environment)
```shell
aws lambda update-function-configuration --region eu-west-1 --function-name lambda-workshop --environment "Variables={SYMBOL=$SYMBOL,SHEET_ID=$SHEET_ID}"
```

7. (Optional) Schedule cron job to trigger function execution
