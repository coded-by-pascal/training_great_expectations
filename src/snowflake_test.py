host = "btelligent.eu-central-1"  # The account name (include region -- ex 'ABCD.us-east-1')
username = "FLEUR_KINATEDER"
password = "DCSO?;6Pxv)^,n74z};V"
database = "AMAZON_VENDOR_ANALYTICS__SAMPLE_DATASET"  # The database name
schema_name = "PUBLIC"  # The schema name
warehouse = "LOAD_WH"  # The warehouse name
role = "PUBLIC"  # The role name
table_name = "PUBLIC.ADS_DSP_CREATIVE_PERFORMANCE"

connection_string = f"snowflake://{username}:{password}@{host}/{database}/{schema_name}?warehouse={warehouse}&role={role}&application=great_expectations_oss"


from ruamel import yaml

import great_expectations as gx
from great_expectations.core.batch import BatchRequest, RuntimeBatchRequest

context = gx.get_context()

datasource_config = {
    "name": "my_snowflake_datasource",
    "class_name": "Datasource",
    "execution_engine": {
        "class_name": "SqlAlchemyExecutionEngine",
        "connection_string": connection_string,
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
    },
}

context.test_yaml_config(yaml.dump(datasource_config))

context.add_datasource(**datasource_config)

batch_request = BatchRequest(
    datasource_name="my_snowflake_datasource",
    data_connector_name="default_inferred_data_connector_name",
    data_asset_name=f"public.ads_dsp_creative_performance",  # this is the name of the table you want to retrieve
)
expectation_suite_name="test_suite"

context.add_or_update_expectation_suite(expectation_suite_name=expectation_suite_name)

validator = context.get_validator(
    batch_request=batch_request, expectation_suite_name=expectation_suite_name
)
print(validator.head())

from great_expectations.profile.user_configurable_profiler import UserConfigurableProfiler
profiler = UserConfigurableProfiler(profile_dataset=validator)

suite = profiler.build_suite()

from great_expectations.checkpoint.checkpoint import SimpleCheckpoint

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