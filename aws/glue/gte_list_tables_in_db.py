import boto3
import os


# get_tables(**kwargs)
'''
Request Syntax

response = client.get_tables(
    CatalogId='string',
    DatabaseName='string',
    Expression='string',
    NextToken='string',
    MaxResults=123
)
'''

def get_table_list(env,dbname,tablepattern):
    """
    Lists log streams with a log group.
    You can list all your log groups or filter the results by prefix.
    """
    session = boto3.Session(profile_name=env)
    client = session.client("glue", "eu-west-2")

    kwargs = {
        'DatabaseName': dbname,
        'Expression': tablepattern,
        'MaxResults': 500,

        }

    while True:
        resp = client.get_tables(**kwargs)
        #print(len(resp))
        yield from resp['TableList']
        try:
            kwargs['NextToken'] = resp['NextToken']

        except KeyError:
            break


'''
'''

if __name__ == '__main__':
    env='notprod'
    #env='prod'
    #env='default'
    # export AWS_DEFAULT_REGION=us-west-2
    #api_working_transformed_document_details_alkilplplhcckmpgpdlmiigldjkencmj
    dbname='api_record_level_score_notprod'
    #tablepattern='api_working_transformed_document_details_a'
    tablepattern='internal_storage_archive'
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"
    for resp in get_table_list(env,dbname,tablepattern):
        print(resp['Name'])
        
