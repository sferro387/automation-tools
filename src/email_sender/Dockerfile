FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY ../../requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the email sender source code
COPY . .

# Command to run the email sender
CMD ["python", "email_sender/send_email.py"]