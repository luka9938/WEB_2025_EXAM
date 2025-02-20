FROM python:3.10.5
WORKDIR /app
RUN apt-get update && \
    apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_16.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g npm
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN npm install --save-dev tailwindcss postcss autoprefixer
RUN npx tailwindcss init
RUN npx tailwindcss -i ./static/styles.css -o ./static/dist/styles.css
CMD ["python", "app.py"]
