def prefix_exists(bucket_name, prefix):
    """
    AWS guarantee that an S3 event notification will be delivered at least once.
    If the prefix exists in the target bucket / location, the event is ignored
    """
    try:
        result = False
        client = boto3.client('s3', config=CONFIG)
        response = client.list_objects_v2(
            Bucket=bucket_name,
            Prefix=prefix
        )
        if response.get('Contents'):
            LOGGER.warning('%s exists in %s. Event ignored. Exiting.',
                           prefix,
                           bucket_name)
            result = True
        else:
            LOGGER.info('%s does not exist in %s. Continuing.',
                        prefix,
                        bucket_name)
        return result

    except Exception as err:
        error_handler(sys.exc_info()[2].tb_lineno, err)
