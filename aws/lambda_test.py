


def lambda_handler(event, context):
    #You can pass event objects that you pass into the handler function.
    #The handler is a method inside the AWS Lambda function that you create and include in your package.
    #The handler function can interact with other AWS services and make third-party API requests to web services that it might need to interact with.
    return "Test AWS Lambda Function"

    #The event includes all the data and metadata that your AWS Lambda function needs to implement the logic
