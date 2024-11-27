# dq-tf-api-record-level-score-pipeline

All artefacts relating to the processing of API files and applying record level scoring.

## Date parameterisation
* By default will scan partitions for all schedule data received in the last 30 days to match data the new arriving data
* When loading historical data this can be adjusted by specifying the date ranges explicitly
```
aws lambda invoke --function-name api-record-level-score-${NAMESPACE}-lambda-athena --cli-read-timeout 0 --log-type Tail --payload ' {"Records": [{"eventTime": "2019-02-18T06:19:38.454Z",
                                            "pathNameCsMin": "2019-01-01",
                                            "pathNameCsMax": "2019-01-31",
                                            "s3": { "bucket": {"name": "s3-dq-api-internal-'${NAMESPACE}'",
                                                    "arn": "arn:aws:s3:::s3-dq-api-internal-'${NAMESPACE}'"},
                                                    "object": {"key": "bulk/'${BATCH_FOLDER}'/defaultkey"}}}]}'  outputfile.txt  | jq -r '. | .LogResult' | base64 --decode
```

## Performance

### Approach
#### Bulk load API data via the API input pipeline
* This avoids triggering record level scoring for each file individually
* See the dq-tf-api-input-pipeline README for more details
* Example commands below show data loaded under the bulk/day1000/2019-02-17/ prefix

#### Clear down tables
* See migration details below

#### Clear down S3 to avoid target path clashes
```
aws s3 rm s3://s3-dq-api-internal-test/bulk/day1000 --recursive
aws s3 rm s3://s3-dq-api-record-level-scoring-test/bulk/day1000 --recursive
aws s3 rm s3://s3-dq-cross-record-scored-test/bulk/day1000 --recursive
```

#### Initiate processing in bulk from the CLI
```
aws lambda invoke --function-name api-record-level-score-test-lambda-trigger --log-type Tail \
                  --payload '	{"Records": [{"eventTime": "2019-02-18T06:19:38.454Z",
                                            "s3": { "bucket": {"name": "s3-dq-api-internal-test",
                                                    "arn": "arn:aws:s3:::s3-dq-api-internal-test"},
                                                    "object": {"key": "bulk/day1000/2019-02-17"}}}]}' \
                  outputfile.txt
```

### Results
#### Single file
* Record count: 131
* End to end time: 46 seconds
* Input time: 3.875 seconds
* Input data scanned: 122,859 bytes
* Scoring time: 12.598 seconds
* Scoring data scanned: 405,122 bytes

#### 237 files
* Record count: 49717
* End to end time: 46 seconds
* Input time: 4.971 seconds
* Input data scanned: 43,442,325 bytes
* Scoring time: 16.721 seconds
* Scoring data scanned: 6,337,653 bytes

#### 1185 files
* Record count: 248638
* End to end time: 55 seconds
* Input time: 6.178 seconds
* Input data scanned: 217,873,108 bytes
* Scoring time: 21.107 seconds
* Scoring data scanned: 30,596,932 byes

## Schema Migration
* Schema migrations may be executed using the following syntax
* Note that the transform_schema_v1 drops any existing objects and is used to reset the environment
* This command can be used in test environments to reset the environment
* Note that pipelines do NOT recreate tables themselves so it is necessary to run this
* Migration steps need to be run sequentially, so if production has been running on v1 for some time, then if there is a v2 we would need to run v2 to upgrade it
```
aws lambda invoke --function-name api-record-level-score-${NAMESPACE}-lambda-athena --cli-read-timeout 0 --log-type Tail \
--payload '{"Records": [{"transformDir": "transform_schema_v1"}]}' \
outputfile.txt
```

## Partition Consolidation
* As Athena processes using files and it is more efficient to process larger files and avoids KMS throttling issues, files are stored at three levels of consolidation
* internal_storage_table - contains individual files as originally received in archive
* internal_storage_consolidated - contains intra-day consolidation of the files in internal_storage_table (see below)
* internal_storage_history - a further level of consolidation at the day level of the files from internal_storage_consolidated (see below)
* Data is accessed via the internal_storage view which is over the three tables above, preventing queries reading the data needing to know how the data is stored
* When consolidation runs, the view is modified to prevent duplicate data being shown in the view between the time of adding the consolidated partition and removing the granualr partitions
### Intra-day partition consolidation is invoked with the following
```
aws lambda invoke --function-name api-record-level-score-${NAMESPACE}-lambda-athena --cli-read-timeout 0 --log-type Tail \
--payload '{"Records": [{"transformDir": "transform_consolidate_v1",
                         "consolidationTarget": "internal_storage_table",
                         "minPathName": "2019-02-22/10:00:00",
                         "maxPathName": "2019-02-22/11:00:00"}]}' \
outputfile.txt
```
* This is normally to be run multiple times during the day to consolidate files
* The minPathName and maxPathName parameters specify the path name range to consolidate
### Daily partition consolidation is invoked with the following
```
aws lambda invoke --function-name api-record-level-score-${NAMESPACE}-lambda-athena --cli-read-timeout 0 --log-type Tail \
--payload '{"Records": [{"transformDir": "transform_consolidate_history_v1",
                         "consolidationTarget": "internal_storage_table_consolidated",
                         "consolidatedPathName": "2019-03-16-history",
                         "minPathName": "2019-02-22/10:00:00",
                         "maxPathName": "2019-02-22/11:00:00"}]}' \
outputfile.txt
```
* This is normally run daily
* The consolidatedPathName parameter is used to specify the name of the partition
* This consolidates the intra day partitions into larger partitions for longer term access

## Sequence Numbers
* The record level scoring applies voyage sequence numbers for identification of unique voyages
* Note that local time is used to identify these 
* The order of precedence is api record departure datetime, schedule datetime, api manifest received timestamp
* The legacy Greenplum system used api record departure datetime and system datetime, the above rule is more robust for cases of bad data in api record departure datetime
* The specific fields are treated as follows:
```
COALESCE(UPPER(TRIM(CAST(TRY(CAST(COALESCE(CAST(TRY(DATE_PARSE(api.flightdetails_departureDateTime, '%Y-%m-%d %H:%i:%s')) AS TIMESTAMP), 
                                                  std_datetime_local,
                                                  CAST(TRY(DATE_PARSE(api.manifestdetails_datetimereceived, '%Y-%m-%dT%H:%i:%sZ')) AS TIMESTAMP)
                                                  ) AS DATE )) AS VARCHAR(10) ))), '')
```
* Example behaviour is as below:
```
SELECT COALESCE(UPPER(TRIM(CAST(TRY(CAST(COALESCE(CAST(TRY(DATE_PARSE('2019-03-30 11:20:00', '%Y-%m-%d %H:%i:%s')) AS TIMESTAMP), 
                                                  CAST('2019-03-01' AS TIMESTAMP),
                                                  CAST(TRY(DATE_PARSE('2019-03-28T12:20:12Z', '%Y-%m-%dT%H:%i:%sZ')) AS TIMESTAMP)
                                                  ) AS DATE )) AS VARCHAR(10) ))), '')

2019-03-30

SELECT COALESCE(UPPER(TRIM(CAST(TRY(CAST(COALESCE(CAST(TRY(DATE_PARSE('11:20:00', '%Y-%m-%d %H:%i:%s')) AS TIMESTAMP), 
                                                  CAST('2019-03-01' AS TIMESTAMP),
                                                  CAST(TRY(DATE_PARSE('2019-03-28T12:20:12Z', '%Y-%m-%dT%H:%i:%sZ')) AS TIMESTAMP)
                                                  ) AS DATE )) AS VARCHAR(10) ))), '')


2019-03-01

SELECT COALESCE(UPPER(TRIM(CAST(TRY(CAST(COALESCE(CAST(TRY(DATE_PARSE('11:20:00', '%Y-%m-%d %H:%i:%s')) AS TIMESTAMP), 
                                                  CAST(null AS TIMESTAMP),
                                                  CAST(TRY(DATE_PARSE('2019-03-28T12:20:12Z', '%Y-%m-%dT%H:%i:%sZ')) AS TIMESTAMP)
                                                  ) AS DATE )) AS VARCHAR(10) ))), '')


2019-03-28

SELECT LENGTH(COALESCE(UPPER(TRIM(CAST(TRY(CAST(COALESCE(CAST(TRY(DATE_PARSE('11:20:00', '%Y-%m-%d %H:%i:%s')) AS TIMESTAMP), 
                                                  CAST(null AS TIMESTAMP),
                                                  CAST(TRY(DATE_PARSE('03-28T12:20:12Z', '%Y-%m-%dT%H:%i:%sZ')) AS TIMESTAMP)
                                                  ) AS DATE )) AS VARCHAR(10) ))), ''))

0
```

