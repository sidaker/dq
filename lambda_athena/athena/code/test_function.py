import unittest
import function 
 
class TestFunction(unittest.TestCase):
 
    def setUp(self):
        pass

    def test_substitute_params(self):
        sql = 'LOCATION s3://{bucket-name}/folder;'
        sql_params = {'bucket-name':'test-bucket'}
        self.assertEqual(function.substitute_params(sql, sql_params),
                        'LOCATION s3://test-bucket/folder;') 

    def test_substitute_params_quoting(self):
        sql = "LOCATION 's3://{bucket-name}/folder';"
        sql_params = {'bucket-name':'test-bucket'}
        self.assertEqual(function.substitute_params(sql, sql_params),
                        "LOCATION 's3://test-bucket/folder';") 

    def test_get_sql_files(self):
        self.assertEqual(function.get_sql_files()[0],
                         'transform/sql/create_table_input_file.sql')

    def test_get_parameter(self):
        self.assertEqual(function.get_parameter('OUTPUT_BUCKET_NAME'),
                         's3://dq-feature-airports-internal-test')

if __name__ == '__main__':
    unittest.main()
