FROM public.ecr.aws/lambda/python:3.8

COPY requirements.txt .

RUN pip3 install -r requirements.txt

RUN mkdir data



COPY rds_manager.py .

COPY data_helper.py .

COPY s3_manager.py .

COPY test_rds_manager.py .

COPY test_data_helper.py .

COPY test_s3_manager.py .

COPY pipeline.py .

COPY lambda_handler.py .


CMD ["lambda_handler.lambda_handler"]