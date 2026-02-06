FROM python:3.10-slim
RUN apt-get update && apt-get install -y redis-server curl && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && apt-get install -y nodejs
RUN pip install SmartApi pyotp redis flask
WORKDIR /app
COPY . .
RUN npm install && npm run build
RUN chmod +x start.sh
CMD ["./start.sh"]
