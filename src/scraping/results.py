#!/usr/bin/env python3
'''
This script logs into the coderbyte website, scrapes coding results, and saves them to a .csv file.
Because the coderbyte API costs $200/month, this script can save Ishango costs.
'''
import scraping.definitions as D
from scraping.tools import login, retrieve_and_model_results, save_results


def extract_results() -> None:
    # login into coderbyte and return the session
    session = login()

    # retrieve results for a list of assessments
    results = retrieve_and_model_results(D.Assessments.ghana_2022_assessments, session)

    # save the resulting dataframe
    save_results(results, D.Paths.ghana_2022_export_path)


if __name__ == '__main__':
    extract_results()
