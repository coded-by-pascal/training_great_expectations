import great_expectations as gx
import os

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
# </snippet>

sf_source_datasource = context.sources.add_sql(
    name="sf_source", connection_string=_get_connection_string(), create_temp_table=False
)
sf_source_asset = sf_source_datasource.add_table_asset(
    name="retail_analytics_net_ppm", schema_name="tjf_2023_09_source", table_name="retail_analytics_net_ppm"
)

# sf_source_asset.add_splitter_year_and_month(column_name="date")

# sf_source_asset = sf_source_asset.add_sorters(["+year"])

sf_stage_datasource = context.sources.add_sql(
    name="sf_stage", connection_string=_get_connection_string(), create_temp_table=False
)
sf_stage_asset = sf_stage_datasource.add_table_asset(
    name="retail_analytics_net_ppm", schema_name="tjf_2023_09_stage", table_name="retail_analytics_net_ppm"
)

# sf_stage_asset.add_splitter_year_and_month(column_name="date")

# sf_stage_asset = sf_stage_asset.add_sorters(["+year"])


sf_source_batch = sf_source_asset.build_batch_request()

sf_stage_batch = sf_stage_asset.build_batch_request()

data_assistant_result = context.assistants.onboarding.run(
    batch_request=sf_stage_batch,
    exclude_column_names=[
        "_CREATED_ON",
        "_LAST_UPDATED_ON",
        "_REVISION",
        "_PARTNERUUID"
    ],
    estimation="flag_outliers"
)

expectation_suite_name = "compare_two_tables"
expectation_suite = data_assistant_result.get_expectation_suite(
    expectation_suite_name=expectation_suite_name
)
context.add_or_update_expectation_suite(expectation_suite=expectation_suite)


checkpoint = context.add_or_update_checkpoint(
    name="comparison_checkpoint",
    validations=[
        {
            "batch_request": sf_source_batch,
            "expectation_suite_name": expectation_suite_name,
        }
    ],
)


checkpoint_result = checkpoint.run()



# assert checkpoint_result["success"] is True
# statistics = checkpoint_result["run_results"][
#     list(checkpoint_result["run_results"].keys())[0]
# ]["validation_result"]["statistics"]
# assert statistics["evaluated_expectations"] != 0
# assert statistics["evaluated_expectations"] == statistics["successful_expectations"]
# assert statistics["unsuccessful_expectations"] == 0
# assert statistics["success_percent"] == 100.0
# data_assistant_result.plot_expectations_and_metrics()

context.build_data_docs()
context.open_data_docs()