# Use an official Python runtime as a parent image
FROM python:3.11-slim


# Set the working directory in the container
WORKDIR /app

# Copy the Pipfile and Pipfile.lock to the container
COPY app/requirements.txt ./

# Install pipenv and compile dependencies
RUN pip install -r requirements.txt

# Copy the rest of the backend code into the container
COPY app /app

ENV DATABASE_URL="postgresql://default:HePa1sdgW7vM@ep-young-smoke-a4l644r7.us-east-1.aws.neon.tech:5432/flasker?sslmode=require"

# Expose the port that the app runs on
EXPOSE 8000

# Command to run the app with uvicorn
CMD ["sh", "-c", "cd /app && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"]