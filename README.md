# Ishango_Assessments
[Ishango](https://ishango.ai) is an NGO based in London, that provides African students the chance to work on Data Science projects for companies all around the world.
To assess the candidates, they ask them to perform coding challenges/problems via an online coding platform.

Ishango wants to automatically (and periodically) retrieve the results of these assessments - this repo contains the code to "solve" this problem.

### The structure of the project is the following:

    .
    ├── ...
    ├── src/scrapping               # Folder that holds the main files and the data extracts
    │   ├── credentials.py          # File to store the credentials to acess the platform and the Postgres DB
    │   ├── definitions.py          # File to store constants and strings (edit the paths for each assessment here)
    │   ├── results.py              # Main app file (should be the one called to retrieve the results)
    │   └── tools.py                # All functions used by the main app
    ├── tests                       # Tests folder, to assess the functions used by the package
    └── README.md


[![Main Python application](https://github.com/Ishangoai/Ishango_Assessments/actions/workflows/main.yml/badge.svg)](https://github.com/Ishangoai/Ishango_Assessments/actions/workflows/main.yml)

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Ishangoai_Ishango_Assessments&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=Ishangoai_Ishango_Assessments)

