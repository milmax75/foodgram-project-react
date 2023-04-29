FROM python:3.9-slim 
 
WORKDIR /app 
 
COPY requirements.txt .
 
RUN pip3 install -r ./requirements.txt --no-cache-dir 
 
COPY ./backend .
 
CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0.0.0.0:8000" ]

LABEL author='milmax75', version=1.0, status='reading theory again'
