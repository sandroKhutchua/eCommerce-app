FROM python:3.9-slim

WORKDIR /ecommerceapp

COPY . /ecommerceapp

CMD ["python3", "ecommerceapp.py"]