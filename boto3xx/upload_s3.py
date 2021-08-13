def upload_s3_object(local_file, bucket_name, key_name):
    """ upload local_file as key_name to bucket_name """

    try:
        s3_conn = boto3.resource('s3', config=CONFIG)
        s3_conn.Bucket(bucket_name).upload_file(local_file, key_name)
        LOGGER.info(
            '%s uploaded to %s as %s',
            local_file,
            bucket_name,
            key_name)

    except Exception as err:
        error_handler(sys.exc_info()[2].tb_lineno, err)
