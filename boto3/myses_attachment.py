import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart


if __name__=='__main__':
    # Change the profile of the default session in code

    boto3.setup_default_session(profile_name='notprod')
    client = boto3.client(
    'ses',
    region_name='eu-west-2'
    )

    message = MIMEMultipart()
    message['Subject'] = 'Test email attachments'
    message['From'] = 'siddartha.bommireddy@digital.homeoffice.gov.uk'
    message['To'] = ', '.join(['siddartha.bommireddy@digital.homeoffice.gov.uk'])

    # message body
    part = MIMEText('this message is sent from sid and ses', 'html')
    message.attach(part)
    # attachment
    if attachment_string:   # if bytestring available
        part = MIMEApplication(str.encode('attachment_string'))
    else:    # if file provided
        part = MIMEApplication(open(attachment_file.csv, 'rb').read())
        part.add_header('Content-Disposition', 'attachment', filename='name_of_attachment.csv')
        message.attach(part)

    response = client.send_raw_email(
        Source=message['From'],
        Destinations=['recipient1@domain.com', 'recipient2@domain.com'],
        RawMessage={
        'Data': message.as_string()
        }
    )

    print(response)
