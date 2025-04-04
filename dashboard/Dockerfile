FROM python:latest

WORKDIR /dashboard

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY dashboard.py .
COPY models.py .

EXPOSE 8501/tcp

CMD ["streamlit", "run", "dashboard.py"]