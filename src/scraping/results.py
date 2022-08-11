#!/usr/bin/env python3
"""
This script logs into the coderbyte website, scrapes coding results, and saves them to DB or a .csv file.
Because the coderbyte API costs $200/month, this script can save Ishango costs.
"""
import scraping.definitions as D
import scraping.tools as T


def extract_results(
    pre_process: bool = True,
    save_to_db: bool = True,
    save_to_file: bool = True,
    write_to_gsheets: bool = True,
) -> None:
    # login into coderbyte and return the session
    session = T.login()

    # retrieve results for a list of assessments
    results = T.retrieve_and_union_results(assessments=D.Assessments.ghana_2022_october_assessments, session=session)

    if pre_process:
        # pre_process results to be inserted into the database
        results = T.pre_process_results(dataframe=results)

    if save_to_db:
        # verify that pre-processing is done before saving to the database
        if not pre_process:
            print("Cannot save to database without pre-processing the results.")
            return
        # save results to database
        db = T.DataBaseInteraction(dataframe=results, table_name=D.DatabaseTables.TABLE_ghana_2022.value)
        db.save_results_to_db()

    if save_to_file:
        # save the resulting dataframe
        T.save_results(dataframe=results, path=D.Paths.ghana_2022_export_path)

    if write_to_gsheets:
        gs = T.GoogleSheets(table_name=D.DatabaseTables.TABLE_ghana_2022.value)
        gs.sqltosheets()


if __name__ == "__main__":
    extract_results(save_to_file=False)
