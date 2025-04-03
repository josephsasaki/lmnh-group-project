FROM public.ecr.aws/lambda/python:3.9

WORKDIR ${LAMBDA_TASK_ROOT}

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY lambda_handler.py .
COPY pipeline.py .
COPY extract.py .
COPY models.py .
COPY transform.py .
COPY load.py .
COPY code_to_name.csv .


CMD [ "lambda_handler.lambda_handler" ]