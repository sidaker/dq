import re
from datetime import datetime

tb_name = 'api_record_level_accuracy_scored_20221101'

part_dt_format='YYYYMMDD'

# printing original string
print("The original string is : " + str(tb_name))
# searching string
match_str = re.search(r'\d{8}', tb_name)

print("******")
print(match_str)
print(match_str.string)
print(match_str.group())
print("******")

# initializing string
test_str = "gfg at 2021-01-04"

# printing original string
print("The original string is : " + str(test_str))

# searching string
match_str = re.search(r'\d{4}-\d{2}-\d{2}', test_str)

# computed date
# feeding format
res = datetime.strptime(match_str.group(), '%Y-%m-%d').date()

# printing result
print("Computed date : " + str(res))