FROM python:3.6-buster
WORKDIR /ValuationApi
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]