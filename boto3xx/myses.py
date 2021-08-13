import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

if __name__=='__main__':
    # Change the profile of the default session in code

    boto3.setup_default_session(profile_name='notprod')
    client = boto3.client(
    'ses',
    region_name='eu-west-2'
    )

    response = client.send_email(
    Destination={
        'ToAddresses': ['siddartha.bommireddy@digital.homeoffice.gov.uk'],
    },
    Message={
        'Body': {
            'Text': {
                'Charset': 'UTF-8',
                'Data': 'Hello email from SES',
            },
        },
        'Subject': {
            'Charset': 'UTF-8',
            'Data': 'Test email please from SES',
        },
    },
    Source='siddartha.bommireddy@digital.homeoffice.gov.uk',
)

    print(response)
