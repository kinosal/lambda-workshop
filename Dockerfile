FROM public.ecr.aws/lambda/python:3.9

COPY lambda_function.py ${LAMBDA_TASK_ROOT}
COPY google_account.json ${LAMBDA_TASK_ROOT}
COPY pyproject.toml ${LAMBDA_TASK_ROOT}
COPY poetry.lock ${LAMBDA_TASK_ROOT}
COPY modules ${LAMBDA_TASK_ROOT}/modules

RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev --no-root

CMD [ "lambda_function.lambda_handler" ]
