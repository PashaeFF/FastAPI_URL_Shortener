FROM python:3.9

WORKDIR /

COPY . /

RUN pip3 install --no-cache-dir --upgrade -r ./requirements.txt

CMD [
    "poetry", "run",
    "uvicorn",
    "main:app",
    "--port", "8000"
  ]
