import pandas as pd
import json
from database.query_executor import fetch_data
from validation.data_comparator import compare_data
from utils.logger import log_results
import numpy as np
import time

def load_test_cases(file_path):

    with open(file_path, "r") as file:
        return json.load(file)

def validate_data(test_cases_file,max_retries=5,retry_delay=10):
    
    test_cases = load_test_cases(test_cases_file)  
    all_results = []

    for test_case, details in test_cases.items():
        source_query = details["source_query"]
        destination_query = details["destination_query"]
        widget_param = details["widget_param"]
        parameter=details["parameter"]

        retries=0
        while(retries<max_retries):
             try:
                    log_results(f"Running Test Case: {test_case}")
                    source_data = fetch_data("source", source_query)
                    destination_data = fetch_data("source", destination_query)
                    source_df = pd.DataFrame(source_data)
                    destination_df = pd.DataFrame(destination_data)
                    destination_df.columns=source_df.columns
                    source_df = source_df.reset_index(drop=True)
                    destination_df = destination_df.reset_index(drop=True)
                    source_df = source_df.astype(int)
                    destination_df = destination_df.astype(int)
                    if source_data.empty or destination_data.empty:
                        log_results(f"ERROR: One of the databases returned no data for test case: {test_case}")
                        break
                    log_results(f"Source Data (Rounded) for Test Case {test_case}:\n{source_data.to_string(index=False)}")
                    log_results(f"Destination Data (Rounded) for Test Case {test_case}:\n{destination_data.to_string(index=False)}")
                    differences = compare_data(source_df, destination_df)
                    differences = differences.reset_index()
                    source_values = source_data.values.flatten()
                    destination_values = destination_data.values.flatten()
                    if differences.empty:
                        validation_status = 'PASS'
                    else:
                        validation_status = 'FAIL'
                    test_case_results = pd.DataFrame({
                        'Test_Case_Id':test_case,
                        'Source': source_values,
                        'Destination': destination_values,
                        'Validation Status': [validation_status],
                        'Widget_Param':widget_param,
                        'parameter':parameter
                    })
                    time.sleep(30)
                    all_results.append(test_case_results)
                    log_results(f"Validation Data for Test Case {test_case}:\n{test_case_results.to_string(index=False)}")
                    break
               
             except (TimeoutError, ConnectionError)  as e:
                 retries+=1
                 log_results(f"WARNING: Connection timed out for Test Case {test_case}. Retrying {retries}/{max_retries}...")
                 time.sleep(retry_delay)

             except Exception as e:
                    log_results(f"ERROR: Unexpected issue in Test Case {test_case}: {e}")
                    break 
             
             if retries == max_retries:
                    log_results(f"Test Case {test_case} failed after {max_retries} retries. Skipping.")
        
    if all_results:
        final_results_df = pd.concat(all_results, ignore_index=True)
        try:
            final_results_df.to_excel("Test_Execution_Report.xlsx", index=False)
            log_results("Validation results for all test cases saved to 'Test_Execution_Report.xlsx'.")
        except Exception as e:
            log_results(f"Error saving validation data: {e}")



