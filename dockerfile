# Take the latest (python:latest) python image you find on the Docker server
# (we could potentially specify a version, e.g. 3.10.4-slim, but I had problems
# installing the app as a package if I did so)
FROM python:latest

# Set the working directory for the app
WORKDIR /coderbyte_ishango

# Copy the app from the current folder to the working directory
COPY . .

# Install the required libraries and the module itself (necessary
# to be able to run the tests with pytes)
RUN pip install -r ./requirements.txt
RUN pip install -e .

# Run the App
CMD ["python", "./src/scraping/results.py"]
