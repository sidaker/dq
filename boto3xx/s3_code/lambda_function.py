import boto3

def lambda_client():
    aws_lambda = boto3.client('lambda',region_name='eu-west-2')
    ''' type pyboto3.lambda '''
    print(type(aws_lambda))
    return aws_lambda


def iam_client():
    iam = boto3.client('iam',region_name='eu-west-2')
    ''' type pyboto3.iam '''
    print(type(iam))
    return iam

def access_policy_for_lambda():
    s3_access_policy_document =  {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": "s3:*",
                "Resource": "*"
                }
            ]
        }       
