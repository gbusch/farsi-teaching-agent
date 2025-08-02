FROM python:3.12

EXPOSE 8080
WORKDIR /app

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app/ ./
COPY ./app/.streamlit/secrets-gcp.toml ./.streamlit/secrets.toml

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]