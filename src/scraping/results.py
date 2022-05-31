#!/usr/bin/env python3
'''
This script logs into the coderbyte website, scrapes coding results, and saves them to a .csv file.
Because the coderbyte API costs $200/month, this script can save Ishango costs.
'''
import scraping.definitions as D
import scraping.tools as T


def extract_results(
                    model: bool = True,
                    save_to_db: bool = True,
                    save_to_file: bool = True,
                    ) -> None:
    # login into coderbyte and return the session
    session = T.login()

    # retrieve results for a list of assessments
    results = T.retrieve_and_union_results(D.Assessments.ghana_2022_assessments, session)

    if model:
        # model results to be inserted into the database
        results = T.model_results(results, D.DataTypes.ghana_2022_dtypes)

    if save_to_db:
        conn = T.db_connect(D.Database.DB_PATH)
        T.db_dataframe_to_db(results, conn, D.Database.TABLE_ghana_2022)

    if save_to_file:
        # save the resulting dataframe
        T.save_results(results, D.Paths.ghana_2022_export_path)


if __name__ == '__main__':
    extract_results(model=True, save_to_db=False, save_to_file=True)
