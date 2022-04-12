#!/usr/bin/env python3
'''
This script logs into the coderbyte website, scrapes coding results, and saves them to a .csv file.
Because the coderbyte API costs $200/month, this script can save Ishango costs.
'''
import definitions as D
from tools import return_results

# retrieve results for a list of assessments
assessment_results = return_results(D.Assessments.GHANA_2022_ASSESSMENT_PAGES)

# Export results
assessment_results.to_csv(D.Paths.export_file, index=False)
