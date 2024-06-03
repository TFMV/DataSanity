from great_expectations.expectations.core import ExpectationConfiguration
from great_expectations.execution_engine import PandasExecutionEngine
from great_expectations.expectations.metrics import ColumnMetricProvider

# Create custom Expectation for specific logic
class ExpectColumnToHaveUniqueValues(ColumnMetricProvider):
  metric_name = "column.values.unique.count"

  def _metric_function(self, column, **kwargs):
    # Perform custom calculation to check unique values
    unique_values = len(column.unique())
    return unique_values

  @classmethod
  def _generate_expectation_configuration(cls, **kwargs):
    kwargs.update({
      "meta": {
        "details": "Ensures all values in the column are unique",
        "metric_dependencies": [
          "column.values.unique.count"
        ]
      },
    })

    return ExpectationConfiguration(expectation_type="expect_column_to_have_unique_values", **kwargs)