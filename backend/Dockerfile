# Use the official Python base image with Python 3.9
FROM python:3.9-slim


WORKDIR /app

ADD ./requirements.txt /app/requirements.txt
# Install the project dependencies
RUN pip install -r requirements.txt

ADD . /app
# Copy the rest of the project code to the working directory

# Expose the port on which the FastAPI application will run
EXPOSE 7013

# Start the FastAPI application
#CMD ["gunicorn", "-b", "0.0.0.0:7010", "-w", "1", "-k", "uvicorn.workers.UvicornWorker", "main:app"]