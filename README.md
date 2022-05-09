# Coderbyte_Ishango
[Ishango](https://ishango.ai) is an NGO located in London, that provides African students the chance to do internships in Data Science projects for companies all around the world.
To assess the candidates, they ask them to perform coding challenges/problems via the [Coderbyte](https://codebyte.com) platform.

For Ishango to be able to retrieve the results of these assessments from the platform, a premium value should be paid.
This repo contains the code to "solve" this problem, by logging into the platform and scrapping the tables of the results.

### The structure of the project is the following:

    .
    ├── ...
    ├── results_scrapping           # Folder that holds the main files and the data extracts
    │   ├── definitions.py          # File to store constants and strings (edit the paths for each assessment here)
    │   ├── results.py              # Main app file (should be the one called to retrieve the results)
    │   └── tools.py                # All functions used by the main app
    └── README.md

![Tests]((https://github.com/RicSegundo/Coderbyte_Ishango/actions/workflows/main.yml/badge.svg))
