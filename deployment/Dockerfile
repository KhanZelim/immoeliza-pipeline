FROM python:3.12


# Define /app as the working directory
WORKDIR /app

# Copy all the files in the current directory in /app
COPY . .

# Update pip
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt && echo "All Installed"

# Run the app
# Set host to 0.0.0.0 to make it run on the container's network
CMD uvicorn api.aplic:app --host 0.0.0.0
