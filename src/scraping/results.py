#!/usr/bin/env python3
'''
This script logs into the coderbyte website, scrapes coding results, and saves them to DB or a .csv file.
Because the coderbyte API costs $200/month, this script can save Ishango costs.
'''
import scraping.definitions as D
import scraping.tools as T
import time


def extract_results(
                    pre_process: bool = True,
                    save_to_db: bool = True,
                    db_type: str = D.DatabaseTypes.SQLITE,
                    save_to_file: bool = True,
                    ) -> None:
    # login into coderbyte and return the session
    session = T.login()

    # retrieve results for a list of assessments
    results = T.retrieve_and_union_results(D.Assessments.ghana_2022_assessments, session)

    if pre_process:
        # pre_process results to be inserted into the database
        results = T.pre_process_results(results, D.PandasSchemas.ghana_2022_schema)

    if save_to_db:
        # verify that pre-processing is done before saving to the database
        if not pre_process:
            print("Cannot save to database without pre-processing the results.")
            return
        # save results to database
        db = T.DataBaseInteraction(results, D.DatabaseTables.TABLE_ghana_2022.value)
        db.save_results_to_db(db_type)

    if save_to_file:
        # save the resulting dataframe
        T.save_results(results, D.Paths.ghana_2022_export_path)


if __name__ == '__main__':
    time.sleep(120)
    extract_results(db_type=D.DatabaseTypes.POSTGRES, save_to_file=False)
