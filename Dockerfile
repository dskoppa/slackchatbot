# Use the official Python base image with Alpine Linux
FROM python:3.9-alpine

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apk add --no-cache gcc musl-dev

# Copy the requirements.txt file to the working directory
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files to the working directory
COPY . .

# Set the environment variables
ENV SLACK_API_TOKEN=<your_slack_api_token>
ENV GPT_API_TOKEN=<your_gpt_api_token>

# Expose the port that the application will listen on (if applicable)
EXPOSE <port_number>

# Run the application
CMD [ "python", "slackchatbot.py" ]
