import great_expectations as gx
import os
from datetime import datetime

def _get_connection_string() -> str:
    host = "btelligent.eu-central-1"  # The account name (include region -- ex 'ABCD.us-east-1')
    username = os.getenv("sf_user", "NO_USER")
    password = os.getenv("sf_password", "NO_PWD")
    database = "PASCAL_DB"  # The database name
    schema_name = "TJF_2023_09_SOURCE"  # The schema name
    warehouse = "LOAD_WH"  # The warehouse name
    role = "PUBLIC"  # The role name
    
    connection_string = f"snowflake://{username}:{password}@{host}/{database}/{schema_name}?warehouse={warehouse}&role={role}&application=great_expectations_oss"

    return connection_string;



context = gx.get_context()

sf_stage_datasource = context.sources.add_sql(
    name="sf_stage", connection_string=_get_connection_string()
)
sf_stage_datasource.add_table_asset(
    name="retail_analytics_net_ppm", schema_name="tjf_2023_09_stage", table_name="retail_analytics_net_ppm"
)

sf_stage_batch = sf_stage_datasource.get_asset("retail_analytics_net_ppm").build_batch_request()

validator=sf_stage_batch

expectation_suite_name = "write own expectations"

suite = context.add_expectation_suite(expectation_suite_name=expectation_suite_name)


from great_expectations.core.expectation_configuration import ExpectationConfiguration


expectation_configuration_1 = ExpectationConfiguration(
    expectation_type="expect_table_columns_to_match_ordered_list",
    kwargs={
        "column_list": ['id', '_created_on', '_last_updated_on', '_revision', '_partneruuid', 'date', 'period', 'program', 'distributor_view', 'asin', 'product_title', 'net_ppm', 'net_ppm_prior_period', 'net_ppm_last_year', 'raw_record']
    },
    meta={
        "notes": {
            "format": "markdown",
            "content": "Table structure",
        }
    },
)

suite.add_expectation(expectation_configuration=expectation_configuration_1)

expectation_configuration_2 = ExpectationConfiguration(
    expectation_type="expect_column_values_to_be_in_set",
    kwargs={
        "column": "program",
        "value_set": ["Amazon Retail"],
    },

)
suite.add_expectation(expectation_configuration=expectation_configuration_2)


context.add_or_update_expectation_suite(expectation_suite=suite)


checkpoint = context.add_or_update_checkpoint(
    name="comparison_checkpoint",
    validations=[
        {
            "batch_request": sf_stage_batch,
            "expectation_suite_name": expectation_suite_name,
        }
    ],
)

validator = context.get_validator(
    batch_request=sf_stage_batch, expectation_suite_name=expectation_suite_name
)

# Review and save our Expectation Suite in json
date = (datetime.today()).strftime('%Y%m%d')
print(validator.get_expectation_suite(discard_failed_expectations=False))
validator.save_expectation_suite(filepath= "expect_suite_" + str(date) + ".json", discard_failed_expectations=False)


checkpoint_result = checkpoint.run()

context.build_data_docs()
context.open_data_docs()