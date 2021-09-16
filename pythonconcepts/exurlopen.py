from urllib.request import urlopen
story = urlopen('https://beta.companieshouse.gov.uk/company/08413020/officers')
print(story)
for line in story:
    print(line)

'''
http data is provided as bytes
'''
story.close()
