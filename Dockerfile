FROM python:3.11-slim
LABEL maintainer="@NotLawson and @MitchExists"
LABEL description="A Docker image for the server file in this repository."

# Set the working directory
WORKDIR /app

# Copy the requirements filintoe  the container and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Set the startup command to run the server
CMD ["python", "-u", "main.py"]