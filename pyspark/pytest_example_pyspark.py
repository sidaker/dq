from package.application import filter_spark_data_frame
# your spark application is called  application and it is under the directory package
import pandas as pd
# import pandas as you may want to convert your spark dataframes to pandas dataframe to compare.

def get_sorted_data_frame(pandas_data_frame, columns_list):
    return pandas_data_frame.sort_values(columns_list).reset_index(drop=True)

def test_filter_spark_data_frame(sql_context):
    # Create Input Data frame
    input = sql_context.createDataFrame(
        [('Likhitha', 16),
         ('fabien', 15),
         ('sam', 21),
         ('sam', 25),
         ('nick', 19),
         ('nick', 40)],
        ['name', 'age'],
    )
    # Create Expected Output Data frame
    expected_output = sql_context.createDataFrame(
        [('sam', 25),
         ('sam', 21),
         ('nick', 40)],
        ['name', 'age'],
    )
    real_output = filter_spark_data_frame(input)

    '''
    while comparing two data frames the order of rows and columns is important for Pandas.
    Pandas provides such function like pandas.testing.assert_frame_equal with the parameter
    check_like=True to ignore the
    order of columns. However, it does not have a built-in functionality to ignore the
    order of rows.
    Therefore, to make the two data frames comparable we will use the created method
     get_sorted_data_frame.

    '''

    # convert the spark dataframe to Pandas dataframe and Sort.
    # Pass the arguments Pandas dataframe and list of columns to the function
    real_output_pandas = get_sorted_data_frame(
        real_output.toPandas(),
        ['age', 'name'],
    )
    expected_output_pandas = get_sorted_data_frame(
        expected_output.toPandas(),
        ['age', 'name'],
    )

    # Use Pandas assertion rule.
    pd.testing.assert_frame_equal(expected_output_pandas, real_output_pandas, check_like=True)
