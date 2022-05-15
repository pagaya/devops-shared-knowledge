FROM public.ecr.aws/lambda/python:3.8
ARG PIP_INDEX_URL
COPY main.py ${LAMBDA_TASK_ROOT}
COPY requirements.txt  .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"
CMD [ "main.lambda_handler" ]