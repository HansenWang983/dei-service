FROM public.ecr.aws/lambda/python:3.8

WORKDIR ${LAMBDA_TASK_ROOT}

COPY . .
RUN pip install --no-cache-dir -r app/requirements.txt --target "${LAMBDA_TASK_ROOT}"
RUN pip uninstall protobuf | echo y
RUN pip install protobuf==3.19.0

CMD [ "app.handler" ]