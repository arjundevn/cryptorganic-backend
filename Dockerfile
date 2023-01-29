FROM python

WORKDIR /mavericks_app

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

# run the API
CMD ["python", "./app/Mavericks_eth_key.py"]
#CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=8000"]
