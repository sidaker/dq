from collections import defaultdict
import csv

new_dict = defaultdict(list)
i=0
for n,key in enumerate(get_matching_s3_keys(bucket=S3_SRC_BUCKET_NAME, prefix=S3_SRC_KEY_PREFIX, suffix='.json')):
    if(n % BATCH_SIZE == 0):
        i=i+1
    new_dict['batch' + str(i)].append(key)

logger.info('Batch Schedule Prepared')


with open(f'{BASE_PATH}/batchfile{CSV_SUFFIX}.csv', 'w', newline="") as csv_file:
    writer = csv.writer(csv_file)
    for key, value in new_dict.items():
        writer.writerow([key, value])
