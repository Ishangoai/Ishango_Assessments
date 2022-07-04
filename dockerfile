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
# to be able to run the tests with pytest)
RUN pip install -r ./requirements.txt
RUN pip install -e .

# save environment variables to be used by cronjob (https://stackoverflow.com/a/41938139/5392289)
ENTRYPOINT ["bash", "/coderbyte_ishango/entrypoint.sh"]

# Run the App
RUN crontab /coderbyte_ishango/crontab
