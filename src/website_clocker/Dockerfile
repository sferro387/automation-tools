FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY ../../requirements.txt .

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the website clocker source code
COPY . .

# Command to run the website clocker
CMD ["python", "website_clocker/clock_hours.py"]