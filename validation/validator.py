import pandas as pd
import json
from database.query_executor import fetch_data
from validation.data_comparator import compare_data
from utils.logger import log_results

def load_test_cases(file_path):

    with open(file_path, "r") as file:
        return json.load(file)

def validate_data(test_cases_file):
    
    test_cases = load_test_cases(test_cases_file)  
    all_results = []

    for test_case, details in test_cases.items():
        source_query = details["source_query"]
        destination_query = details["destination_query"]
        widget_param = details["widget_param"]

        log_results(f"Running Test Case: {test_case}")
        source_data = fetch_data("source", source_query)
        destination_data = fetch_data("source", destination_query)

        if source_data.empty or destination_data.empty:
            log_results(f"ERROR: One of the databases returned no data for test case: {test_case}")
            continue

        source_data = source_data.round(2)
        destination_data = destination_data.round(2)

        log_results(f"Source Data (Rounded) for Test Case {test_case}:\n{source_data.to_string(index=False)}")
        log_results(f"Destination Data (Rounded) for Test Case {test_case}:\n{destination_data.to_string(index=False)}")

        differences = compare_data(source_data, destination_data)
        differences = differences.reset_index()

        source_values = source_data.values.flatten()
        destination_values = destination_data.values.flatten()

        # Prepare results for this test case
        if differences.empty:
            validation_status = 'PASS'
        else:
            validation_status = 'FAIL'

        test_case_results = pd.DataFrame({
            'Test_Case_Id':test_case,
            'Source': source_values,
            'Destination': destination_values,
            'Validation Status': [validation_status],
            'Widget_Param':widget_param
        })

        all_results.append(test_case_results)

        log_results(f"Validation Data for Test Case {test_case}:\n{test_case_results.to_string(index=False)}")


    final_results_df = pd.concat(all_results, ignore_index=True)

    try:
        final_results_df.to_excel("all_validation_results_with_widget.xlsx", index=False)
        log_results("Validation results for all test cases saved to 'all_validation_results_with_widget.xlsx'.")
    except Exception as e:
        log_results(f"Error saving validation data: {e}")


