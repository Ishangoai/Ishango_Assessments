# Take the latest (python:latest) python image you find on the Docker server
# (we could potentially specify a version, e.g. 3.10.4-slim, but I had problems
# installing the app as a package if I did so)
FROM python:latest
RUN apt-get update && apt-get -y install cron

# Set the working directory for the app
WORKDIR /coderbyte_ishango

# Copy the app from the current folder to the working directory
COPY . .

# Install the required libraries and the module itself (necessary
# to be able to run the tests with pytes)

RUN pip install -r ./requirements.txt
RUN pip install -e .

# Run the App
RUN chmod 0644 /coderbyte_ishango/crontab
RUN crontab /coderbyte_ishango/crontab

ENTRYPOINT ["/coderbyte_ishango/entrypoint.sh"]
CMD ["cron", "-f"]

#CMD ["python", "/coderbyte_ishango/src/scraping/results.py"]
