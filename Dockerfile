# Use an official Python runtime as a parent image
FROM python:3.12

# Install wget and tar
RUN apt-get update && apt-get install -y wget tar

# Set the geckodriver installation path
ENV EXEC_PATH="/usr/bin/geckodriver"

# Check if geckodriver exists
RUN if [ -d "$EXEC_PATH" ]; then \
        echo "geckodriver exists"; \
    else \
        # Install Firefox
        install -d -m 0755 /etc/apt/keyrings && \
        echo 'Package: *Pin: origin packages.mozilla.org Pin-Priority: 1000' | tee /etc/apt/preferences.d/mozilla && \
        wget -q https://packages.mozilla.org/apt/repo-signing-key.gpg -O- | tee /etc/apt/keyrings/packages.mozilla.org.asc > /dev/null && \
        echo "deb [signed-by=/etc/apt/keyrings/packages.mozilla.org.asc] https://packages.mozilla.org/apt mozilla main" | tee -a /etc/apt/sources.list.d/mozilla.list > /dev/null && \
        apt-get update && apt-get install -y firefox && \
        \
        # Install geckodriver
        wget https://github.com/mozilla/geckodriver/releases/download/v0.34.0/geckodriver-v0.34.0-linux64.tar.gz && \
        tar -xvf geckodriver-v0.34.0-linux64.tar.gz -C /usr/local/bin/ && \
        rm geckodriver-v0.34.0-linux64.tar.gz; \
    fi

# Set the PATH environment variable to include geckodriver
ENV PATH="/usr/local/bin:${PATH}"

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose the port that the web application will run on
EXPOSE 8080

# Run the start.sh bash file
CMD ["python", "main.py"]
