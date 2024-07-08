# Use an official Python runtime as a parent image
FROM python:3.11-slim


# Set the working directory in the container
WORKDIR /app

# Copy the rest of the backend code into the container
COPY . /app

# Copy the Pipfile and Pipfile.lock to the container
#COPY requirements.txt ./


# Install pipenv and compile dependencies
#RUN pip install --no-cache-dir --upgrade pip \
#    && pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

ENV DATABASE_URL="postgresql://default:HePa1sdgW7vM@ep-young-smoke-a4l644r7.us-east-1.aws.neon.tech:5432/hngstage2?sslmode=require"
ENV PYTHONBUFFERED=1

# Expose the port that the app runs on
EXPOSE 8000

# Command to run the app with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
