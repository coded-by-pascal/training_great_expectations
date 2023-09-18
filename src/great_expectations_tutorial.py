import great_expectations as gx

context = gx.get_context()

validator = context.sources.pandas_default.read_parquet(
    "../testdata/green_tripdata_2022-01.parquet"
)

validator.expect_column_values_to_not_be_null("lpep_pickup_datetime")
validator.expect_column_values_to_not_be_null("lpep_dropoff_datetime")
validator.expect_column_values_to_not_be_null("store_and_fwd_flag")

validator.expect_column_values_to_be_between("passenger_count", auto=True)
validator.expect_column_values_to_be_between("RatecodeID", auto=True)
validator.expect_column_values_to_be_between("PULocationID", auto=True)
validator.expect_column_values_to_be_between("DOLocationID", auto=True)
validator.expect_column_values_to_be_between("passenger_count", auto=True)
validator.expect_column_values_to_be_between("trip_distance", auto=True)
validator.expect_column_values_to_be_between("fare_amount", auto=True)
validator.expect_column_values_to_be_between("extra", auto=True)
validator.expect_column_values_to_be_between("mta_tax", auto=True)
validator.expect_column_values_to_be_between("tip_amount", auto=True)
validator.expect_column_values_to_be_between("tolls_amount", auto=True)
validator.expect_column_values_to_be_between("improvement_surcharge", auto=True)
validator.expect_column_values_to_be_between("total_amount", auto=True)
validator.expect_column_values_to_be_between("payment_type", auto=True)
validator.expect_column_values_to_be_between("trip_type", auto=True)
validator.expect_column_values_to_be_between("congestion_surcharge", auto=True)

validator.save_expectation_suite()

checkpoint = context.add_or_update_checkpoint(
    name="my_quickstart_checkpoint",
    validator=validator,
)


checkpoint_result = checkpoint.run()


context.view_validation_result(checkpoint_result)