# Author: mahalakshmianandh
# Date: 2023-03-25

FROM python:3.8-slim-buster
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PORT 8501
EXPOSE $PORT
CMD streamlit run app.py --server.enableCORS=false --server.port $PORT --server.address 0.0.0.0
