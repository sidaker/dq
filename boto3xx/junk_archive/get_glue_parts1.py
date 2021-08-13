import boto3
from botocore.config import Config
from botocore.exceptions import ClientError



def get_partitions(database, table):
    """
    Loop until the query is either successful or fails
    Args:
        execution_id             : the submitted query execution id
    Returns:
        None
    """
    try:
        #gluesession = boto3.Session(profile_name='prod')
        #glue_client = gluesession.client("glue", "eu-west-2")

        kwargs = {
            'DatabaseName' : database,
            'TableName' : table,
            'MaxResults' : 25,
            }

        while True:
            resp = GLUE.get_partitions(**kwargs)
            #print(len(resp['Partitions']))

            # filter(lambda x: x.get('name') == 'pluto',resp['Partitions'])
            # glue_partition_list = [{'Values': [vals]}]
            listb = [{'Values': d['Values']} for d in resp['Partitions'] ]
            print(listb)
            print(len(listb))
            #print(len([[{'Values': ['2020-08-04/180019']}, {'Values': ['2020-08-15/12:10:10.507617-consolidated']}]]))
            # single list of list
            # [[{'Values': ['2020-08-04/180019']}, {'Values': ['2020-08-15/12:10:10.507617-consolidated']}]]

            #yield from resp['Partitions']
            x = [[]]
            for idx,val in enumerate(listb):
                 x[0].append(val)
            print(x)
            print(len(x))
            break

            yield from x
            try:
                kwargs['NextToken'] = resp['NextToken']
            except KeyError as err:
                break
    except Exception as err:
        print(err)


if __name__=='__main__':
    # Change the profile of the default session in code
    boto3.setup_default_session(profile_name='prod')
    database_name='internal_reporting_prod'
    table_name='dim_parsed_message'
    CONFIG = Config(
        retries=dict(
            max_attempts=10
        )
    )

    GLUE = boto3.client('glue', config=CONFIG , region_name='eu-west-2')

    # yields one partition at a time
    for parts in get_partitions(database_name, table_name):
        print(parts)
        print(type((parts)))
        print(len((parts)))
        print(parts.keys())
        print(parts.values())
        break
