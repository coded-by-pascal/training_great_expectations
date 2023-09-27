import os
from ruamel import yaml
from typing import Dict
import great_expectations as gx
from great_expectations.core.batch import BatchRequest, RuntimeBatchRequest
from great_expectations.profile.user_configurable_profiler import UserConfigurableProfiler
from great_expectations.checkpoint.checkpoint import SimpleCheckpoint

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

def _get_ge_datasource() -> Dict:
    datasource_config = {
        "name": "my_snowflake_datasource",
        "class_name": "Datasource",
        "execution_engine": {
            "class_name": "SqlAlchemyExecutionEngine",
            "connection_string": _get_connection_string(),
            "create_temp_table": False
        },
        "data_connectors": {
            "default_runtime_data_connector_name": {
                "class_name": "RuntimeDataConnector",
                "batch_identifiers": ["default_identifier_name"],
            },
            "default_inferred_data_connector_name": {
                "class_name": "InferredAssetSqlDataConnector",
                "include_schema_name": True,
            },
        }
    }
    
    return datasource_config
    


context = gx.get_context()

datasource_config = _get_ge_datasource()

context.test_yaml_config(yaml.dump(datasource_config))

context.add_datasource(**datasource_config)

batch_request = BatchRequest(
    datasource_name="my_snowflake_datasource",
    data_connector_name="default_inferred_data_connector_name",
    data_asset_name='tjf_2023_09_source.retail_analytics_net_ppm',  # this is the name of the table you want to retrieve
)

batch_request2 = BatchRequest(
    datasource_name="my_snowflake_datasource",
    data_connector_name="default_inferred_data_connector_name",
    data_asset_name='tjf_2023_09_stage.retail_analytics_net_ppm',  # this is the name of the table you want to retrieve
)

expectation_suite_name="test_suite"

context.add_or_update_expectation_suite(expectation_suite_name=expectation_suite_name)

validator = context.get_validator(
    batch_request=batch_request, expectation_suite_name=expectation_suite_name
)

validator2 = context.get_validator(
    batch_request=batch_request2, expectation_suite_name=expectation_suite_name
)
print(validator.head())


profiler = UserConfigurableProfiler(profile_dataset=validator)

suite = profiler.build_suite()

# Review and save our Expectation Suite
print(validator.get_expectation_suite(discard_failed_expectations=False))
validator.save_expectation_suite(discard_failed_expectations=False)

# Set up and run a Simple Checkpoint for ad hoc validation of our data
checkpoint_config = {
    "class_name": "SimpleCheckpoint",
    "validations": [
        {
            "batch_request": batch_request,
            "expectation_suite_name": expectation_suite_name,
        }
    ],
}
checkpoint = SimpleCheckpoint(
    f"{validator.active_batch_definition.data_asset_name}_{expectation_suite_name}", context, **checkpoint_config
)
checkpoint_result = checkpoint.run()

# Build Data Docs
context.build_data_docs()

# Get the only validation_result_identifier from our SimpleCheckpoint run, and open Data Docs to that page
validation_result_identifier = checkpoint_result.list_validation_result_identifiers()[0]
context.open_data_docs(resource_identifier=validation_result_identifier)



checkpoint_config2 = {
    "class_name": "SimpleCheckpoint",
    "validations": [
        {
            "batch_request": batch_request2,
            "expectation_suite_name": expectation_suite_name,
        }
    ],
}
checkpoint2 = SimpleCheckpoint(
    f"{validator.active_batch_definition.data_asset_name}_{expectation_suite_name}", context, **checkpoint_config2
)
checkpoint_result2 = checkpoint2.run()

# Build Data Docs
context.build_data_docs()

# Get the only validation_result_identifier from our SimpleCheckpoint run, and open Data Docs to that page
validation_result_identifier2 = checkpoint_result2.list_validation_result_identifiers()[0]
context.open_data_docs(resource_identifier=validation_result_identifier2)