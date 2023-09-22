FROM python:3.11

# Allows docker to cache installed dependencies between builds
COPY _installation/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Mounts the application code to the image
COPY . app
COPY ./scripts/entrypoint.sh /app/scripts
RUN ["chmod", "+x", "/app/scripts/entrypoint.sh"]
WORKDIR /app

EXPOSE 8000

# runs the production server
ENTRYPOINT ["/app/scripts/entrypoint.sh"]
CMD ["runserver", "0.0.0.0:8000"]
