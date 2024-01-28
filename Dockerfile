FROM python:3.10-slim

WORKDIR ./api

COPY ./requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0"]