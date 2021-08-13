# pylint: disable=broad-except
""" processes an s3 notification
    downloads a jsonl file from s3
    converts each json message into a single line in a delimited file
    uploads the file to s3
"""

import sys
import os
import glob
import re
import json
import datetime
import time
import shutil
import zipfile
import urllib.parse
import urllib.request
import logging
import csv
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError


LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
LOG_GROUP_NAME = None
LOG_STREAM_NAME = None

CONFIG = Config(
    retries=dict(
        max_attempts=20
    )
)


def error_handler(lineno, error):

    LOGGER.error('The following error has occurred on line: %s', lineno)
    LOGGER.error(str(error))
    sess = boto3.session.Session()
    region = sess.region_name

    raise Exception("https://{0}.console.aws.amazon.com/cloudwatch/home?region={0}#logEventViewer:group={1};stream={2}".format(region, LOG_GROUP_NAME, LOG_STREAM_NAME))


def send_message_to_slack(text):
    """
    Formats the text provides and posts to a specific Slack web app's URL

    Args:
        text : the message to be displayed on the Slack channel

    Returns:
        Slack API repsonse
    """


    try:
        post = {"text": "{0}".format(text)}

        ssm_param_name = 'slack_notification_webhook'
        ssm = boto3.client('ssm', config=CONFIG)
        try:
            response = ssm.get_parameter(Name=ssm_param_name, WithDecryption=True)
        except ClientError as e:
            if e.response['Error']['Code'] == 'ParameterNotFound':
                LOGGER.info('Slack SSM parameter %s not found. No notification sent', ssm_param_name)
                return
            else:
                LOGGER.error("Unexpected error when attempting to get Slack webhook URL: %s", e)
                return
        if 'Value' in response['Parameter']:
            url = response['Parameter']['Value']

            json_data = json.dumps(post)
            req = urllib.request.Request(
                url,
                data=json_data.encode('ascii'),
                headers={'Content-Type': 'application/json'})
            LOGGER.info('Sending notification to Slack')
            response = urllib.request.urlopen(req)

        else:
            LOGGER.info('Value for Slack SSM parameter %s not found. No notification sent', ssm_param_name)
            return

    except Exception as err:
        LOGGER.error(
            'The following error has occurred on line: %s',
            sys.exc_info()[2].tb_lineno)
        LOGGER.error(str(err))


def get_path_name(key_name):
    """
    Get path name from key name

    Args:
        key_name

    Returns:
        path_name
    """

    keysplit = key_name.split('/')
    return '/'.join(keysplit[0:len(keysplit)-1])

def get_file_name(key_name):
    """
    Get file name from key name

    Args:
        key_name

    Returns:
        file_name
    """

    return key_name.split('/')[-1]

def clear_container():
    """
    The container may get reused by Lambda so ensure it is clean

    Args:
        None

    Returns:
        None
    """

    try:
        folder = '/tmp'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path): shutil.rmtree(file_path)

    except Exception as err:
        error_handler(sys.exc_info()[2].tb_lineno, err)

def download_s3_file(bucket_name, key_name):
    """
    Downloads files from a bucket within a given prefix

    Args:
        bucket_name : The name of the bucket (without the s3:// prefix)
        key_name    : The full key name of the object

    Returns:
       The file downloaded
    """
    try:
        filename = key_name.split('/')[-1]
        paths = key_name.split('/')[:-1]
        paths_to_create = '/tmp/' + '/'.join(paths)
        os.makedirs(paths_to_create, exist_ok=True)

        s3_conn = boto3.resource('s3', config=CONFIG)
        local_filename = paths_to_create + '/' + filename
        s3_conn.Bucket(bucket_name).download_file(key_name, local_filename)

        return local_filename

    except Exception as err:
        error_handler(sys.exc_info()[2].tb_lineno, err)


def recs_in_file(filename, header):
    """ returns the total records in the file """
    try:
        recs = sum(1 for line in open(filename))
        if header == 'y':
            recs = recs - 1
        return recs
    except Exception as err:
        error_handler(sys.exc_info()[2].tb_lineno, err)

def append_local():
    """ append to local file """
    try:
        if not os.path.isfile("/tmp/full.csv"):
            with open("/tmp/full.csv", "a+") as outfile:
                with open("/tmp/api.csv") as infile:
                    outfile.write(infile.read())
        else:
            # file already exists so do not repeat the header
            with open("/tmp/full.csv", "a+") as outfile:
                with open("/tmp/api.csv") as infile:
                    for l in infile.readlines()[1:]:
                        outfile.write(l)
    except Exception as err:
        error_handler(sys.exc_info()[2].tb_lineno, err)

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


def listdir_fullpath(d):
    return [os.path.join(d, f) for f in os.listdir(d)]


def log_counts(document):
    """ audit counts """

    try:
        documentdetails = len(document['body']['commonAPIPlus']['APIData']['passengerDetails']['documentDetails'])
        flightitinerary = len(document['body']['commonAPIPlus']['APIData']['flightItinerary'])

        logs = {}
        logs['documentDetails'] = documentdetails
        logs['flightItinerary'] = flightitinerary

        LOGGER.info(logs)

    except Exception as err:
        error_handler(sys.exc_info()[2].tb_lineno, err)


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



def get_processed_file_location(filename):
    """
    Get processed file folder from filename
    """
    try:
        return "processed/" + get_date_from_filename(filename) + '/' + filename

    except Exception as err:
        error_handler(sys.exc_info()[2].tb_lineno, err)



def get_processed_xmlfile_location(zipfilename, xmlfilename):
    """
    Get processed xml file folder from zipfilename and xmlfilename
    """
    try:
        return "processed/xml/" + get_date_from_filename(zipfilename) + '/' + zipfilename + '/' + xmlfilename

    except Exception as err:
        error_handler(sys.exc_info()[2].tb_lineno, err)


def xml_file_exists(bucket_name, zipfilename, xmlfilename):
    """
    The specific filename may already have been processed under a different prefix
    If the filename exists, the event is ignored
    """
    try:
        result = False
        client = boto3.client('s3', config=CONFIG)
        response = client.list_objects_v2(
            Bucket=bucket_name,
            Prefix=get_processed_xmlfile_location(zipfilename, xmlfilename)
        )
        if response.get('Contents'):
            LOGGER.warning('%s xml file part of zip %s exists in the prior processed files list. Event ignored. Exiting.',
                           xmlfilename,zipfilename
                           )
            result = True
        else:
            LOGGER.info('%s xml file part of zip %s does not exist in the prior processed files list. Continuing.',
                        xmlfilename,zipfilename
                        )


        return result

    except Exception as err:
        error_handler(sys.exc_info()[2].tb_lineno, err)

def file_exists(bucket_name, filename):
    """
    The specific filename may already have been processed under a different prefix
    If the filename exists, the event is ignored
    """
    try:
        result = False
        client = boto3.client('s3', config=CONFIG)
        response = client.list_objects_v2(
            Bucket=bucket_name,
            Prefix=get_processed_file_location(filename)
        )
        if response.get('Contents'):
            LOGGER.warning('%s exists in the prior processed files list. Event ignored. Exiting.',
                           filename,
                           )
            result = True
        else:
            LOGGER.info('%s does not exist in the prior processed files list. Continuing.',
                        filename,
                        )
        return result

    except Exception as err:
        error_handler(sys.exc_info()[2].tb_lineno, err)



def clean_newline(varx):
    """
    Takes as input a variable varx and strips it off newline characters.
    Also checks if it is of type None or Boolean and returns empty string if so.
    """
    try:
        if(varx is None):
            LOGGER.info('When Processing %s None found', varx)
            return ''
        elif(isinstance(varx, bool)):
            LOGGER.info('When Processing %s Boolean found', varx)
            return ''
        else:
            return varx.replace('\n', '')
    except Exception as err:
        error_handler(sys.exc_info()[2].tb_lineno, err)


def get_date_from_filename(filename):
    """
    Extract date from API filename.
    """
    try:
        filedate = re.search("(20[0-9]{2}[0-9]{2}[0-9]{2})", filename).group(0)
        return filedate[0:4] + '/' + filedate[4:6] + '/' + filedate[6:8]

    except Exception as err:
        error_handler(sys.exc_info()[2].tb_lineno, err)


def create_csv(results_list):

    try:
        csv_cols = [
            'craftdetails_make',
            'craftdetails_model',
            'craftdetails_ownerorganisation',
            'craftdetails_imoregistryplace_type',
            'craftdetails_imonumber',
            'craftdetails_imodate',
            'craftdetails_mmsinumber',
            'craftdetails_callsign',
            'craftdetails_hullcolour',
            'craftdetails_metrelength',
            'craftdetails_portofregistration_type',
            'craftdetails_portofregistration_location_iatacode',
            'craftdetails_portofregistration_location_icaocode',
            'craftdetails_portofregistration_location_coordinates_latitude',
            'craftdetails_portofregistration_location_coordinates_longitude',
            'craftdetails_imoregistryplace_location_iatacode',
            'craftdetails_imoregistryplace_location_icaocode',
            'craftdetails_imoregistryplace_location_unlocode',
            'craftdetails_imoregistryplace_location_coordinates_latitude',
            'craftdetails_imoregistryplace_location_coordinates_longitude',
            'craftdetails_imoregistryplace_location_address_addressline',
            'craftdetails_imoregistryplace_location_address_postcode',
            'craftdetails_imoregistryplace_location_address_country',
            'craftdetails_imoregistryplace_location_description',
            'craftdetails_ownername_firstname',
            'craftdetails_ownername_middlename',
            'craftdetails_ownername_surname',
            'craftdetails_registrationcountrycode',
            'craftdetails_registrationno',
            'craftdetails_sailmarkings',
            'craftdetails_tonnage',
            'craftdetails_portofregistration_location_unlocode',
            'craftdetails_transporttype',
            'craftdetails_type',
            'craftdetails_vesselname',
            'craftdetails_yearbuilt',
            'craftdetails_portofregistration_location_address_addressline',
            'craftdetails_portofregistration_location_address_postcode',
            'craftdetails_portofregistration_location_address_country',
            'craftdetails_portofregistration_location_description',
            'flightdetails_arrivalairport',
            'flightdetails_arrivalairportextended_address_addressline',
            'flightdetails_arrivalairportextended_address_country',
            'flightdetails_arrivalairportextended_address_postcode',
            'flightdetails_arrivalairportextended_coordinates_latitude',
            'flightdetails_arrivalairportextended_coordinates_longitude',
            'flightdetails_arrivalairportextended_description',
            'flightdetails_arrivalairportextended_iatacode',
            'flightdetails_arrivalairportextended_icaocode',
            'flightdetails_arrivalairportextended_unlocode',
            'flightdetails_arrivaldatetime',
            'flightdetails_arrivaldatetimeutc',
            'flightdetails_cargo',
            'flightdetails_carrier',
            'flightdetails_carriertype',
            'flightdetails_craftid',
            'flightdetails_crewcount',
            'flightdetails_datetimesent',
            'flightdetails_departureairport',
            'flightdetails_departureairportextended_address_addressline',
            'flightdetails_departureairportextended_address_country',
            'flightdetails_departureairportextended_address_postcode',
            'flightdetails_departureairportextended_coordinates_latitude',
            'flightdetails_departureairportextended_coordinates_longitude',
            'flightdetails_departureairportextended_description',
            'flightdetails_departureairportextended_iatacode',
            'flightdetails_departureairportextended_icaocode',
            'flightdetails_departureairportextended_unlocode',
            'flightdetails_departuredatetime',
            'flightdetails_departuredatetimeutc',
            'flightdetails_eventcode',
            'flightdetails_exception',
            'flightdetails_flightid',
            'flightdetails_hireorcharter',
            'flightdetails_hireorcharterdetails',
            'flightdetails_manifesttype',
            'flightdetails_operatoraddress_addressline',
            'flightdetails_operatoraddress_country',
            'flightdetails_operatoraddress_postcode',
            'flightdetails_operatorname_firstname',
            'flightdetails_operatorname_middlename',
            'flightdetails_operatorname_surname',
            'flightdetails_passengercount',
            'flightdetails_rawflightid',
            'flightdetails_route',
            'flightdetails_subsequentport',
            'flightitinerary_departure_locationnamecode',
            'flightitinerary_departure_locationfunctioncode',
            'flightitinerary_departuredatetime',
            'flightitinerary_departure_locationnameextended_iatacode',
            'flightitinerary_departure_locationnameextended_icaocode',
            'flightitinerary_arrival_locationnamecode',
            'flightitinerary_arrival_locationfunctioncode',
            'flightitinerary_arrivaldatetime',
            'flightitinerary_arrival_locationnameextended_iatacode',
            'flightitinerary_arrival_locationnameextended_icaocode',
            'passengerdetails_officeofclearance',
            'passengerdetails_passengeridentifier',
            'passengerdetails_age',
            'passengerdetails_dateofbirth',
            'passengerdetails_firstname',
            'passengerdetails_secondname',
            'passengerdetails_surname',
            'passengerdetails_gender',
            'passengerdetails_homeaddress_addressline',
            'passengerdetails_homeaddress_postcode',
            'passengerdetails_homeaddress_country',
            'passengerdetails_intransitflag',
            'passengerdetails_nationality',
            'passengerdetails_countryofresidence',
            'passengerdetails_country',
            'passengerdetails_postalcode',
            'passengerdetails_rankrating',
            'passengerdetails_placeofbirth',
            'passengerdetails_state',
            'passengerdetails_passengertype',
            'passengerdetails_pnrlocator',
            'passengerdetails_street',
            'passengerdetails_city',
            'passengerdetails_portofdisembarkationextended_iatacode',
            'passengerdetails_portofdisembarkationextended_icaocode',
            'passengerdetails_portofdisembarkationextended_unlocode',
            'passengerdetails_portofdisembarkationextended_coordinates_lati',
            'passengerdetails_portofdisembarkationextended_coordinates_long',
            'passengerdetails_portofdisembarkationextended_address_addressl',
            'passengerdetails_portofdisembarkationextended_address_postcode',
            'passengerdetails_portofdisembarkationextended_address_country',
            'passengerdetails_vehicledetails_registrationnumber',
            'passengerdetails_vehicledetails_vehicletype',
            'passengerdetails_vehicledetails_make',
            'passengerdetails_vehicledetails_model',
            'passengerdetails_vehicledetails_registrationcountry',
            'passengerdetails_vehicledetails_vin',
            'passengerdetails_vehicledetails_year',
            'passengerdetails_vehicledetails_colour',
            'passengerdetails_portofembark',
            'passengerdetails_portofdisembark',
            'passengerdetails_crewallowance_goodstodeclare',
            'passengerdetails_crewallowance_goodsdetail',
            'passengerdetails_purposeofvisit',
            'passengerdetails_lengthofstayinuk',
            'passengerdetails_visaholder',
            'passengerdetails_contactnumber_phonenumber',
            'passengerdetails_contactnumber_phonenumbertype',
            'passengerdetails_interactivedetail_passengeridentifier',
            'passengerdetails_interactivedetail_redressno',
            'passengerdetails_interactivedetail_knowntravellerno',
            'passengerdetails_documentdetails_documenttype',
            'passengerdetails_documentdetails_documentno',
            'passengerdetails_documentdetails_docissuedate',
            'passengerdetails_documentdetails_docexpirationdate',
            'passengerdetails_documentdetails_countryofissue',
            'passengerdetails_documentdetails_cityofissue',
            'sendingpartydetails_contactid',
            'sendingpartydetails_contactname',
            'sendingpartydetails_firstcommsaddresscode',
            'sendingpartydetails_firstcommsaddressid',
            'sendingpartydetails_secondcommsaddresscode',
            'sendingpartydetails_secondcommsaddressid',
            'dcsdetails_flightsummary_airlinecode',
            'dcsdetails_flightsummary_flightarrivalairport',
            'dcsdetails_flightsummary_flightarrivaldate',
            'dcsdetails_flightsummary_flightarrivaltime',
            'dcsdetails_flightsummary_flightcode',
            'dcsdetails_flightsummary_flightdepartureairport',
            'dcsdetails_flightsummary_flightdeparturedate',
            'dcsdetails_flightsummary_flightdeparturetime',
            'dcsdetails_flightsummary_rawflightcode',
            'dcsdetails_dcsdata_dcsrecord_baggagedetail',
            'dcsdetails_dcsdata_dcsrecord_cabinclass',
            'dcsdetails_dcsdata_dcsrecord_carryoncount',
            'dcsdetails_dcsdata_dcsrecord_checkedincount',
            'dcsdetails_dcsdata_dcsrecord_checkedinweight',
            'dcsdetails_dcsdata_dcsrecord_checkinagent',
            'dcsdetails_dcsdata_dcsrecord_checkindatetime',
            'dcsdetails_dcsdata_dcsrecord_checkinlocation',
            'dcsdetails_dcsdata_dcsrecord_destination',
            'dcsdetails_dcsdata_dcsrecord_firstname',
            'dcsdetails_dcsdata_dcsrecord_frequentflyernumber',
            'dcsdetails_dcsdata_dcsrecord_passengerseq',
            'dcsdetails_dcsdata_dcsrecord_pnrlocator',
            'dcsdetails_dcsdata_dcsrecord_pooledto',
            'dcsdetails_dcsdata_dcsrecord_seatnumber',
            'dcsdetails_dcsdata_dcsrecord_securitynumber',
            'dcsdetails_dcsdata_dcsrecord_sequencenumber',
            'dcsdetails_dcsdata_dcsrecord_surname',
            'dcsdetails_dcsdata_dcsrecord_ticketnumber',
            'dcsdetails_dcsdata_dcsrecord_ticketstatus',
            'dcsdetails_dcsdata_dcsrecord_traveldocument_traveldocnumber',
            'dcsdetails_dcsdata_dcsrecord_traveldocument_traveldoctype',
            'dcsdetails_dcsdata_dcsrecord_traveldocument_traveldoclocofissue',
            'dcsdetails_dcsdata_dcsrecord_traveldocument_dateofbirth',
            'dcsdetails_dcsdata_dcsrecord_traveldocument_gender',
            'dcsdetails_dcsdata_dcsrecord_traveldocument_docissuedate',
            'dcsdetails_dcsdata_dcsrecord_traveldocument_docexpirationdate',
            'dcsdetails_dcsdata_dcsrecord_traveldocument_cityofissue',
            'dcsdetails_dcsdata_dcsrecord_traveldocument_pnrpassengerref',
            'pnrdetails_accompaniedbyinfant',
            'pnrdetails_bookingdate',
            'pnrdetails_creationdate',
            'pnrdetails_masterpnrlocator',
            'pnrdetails_modifieddate',
            'pnrdetails_pnrlocator',
            'pnrdetails_retrieveddate',
            'pnrdetails_splitpnr',
            'pnrdetails_travelagent',
            'pnrdetails_unaccompaniedminor',
            'sourcedata_component',
            'sourcedata_interactivedata_commonaccessref',
            'sourcedata_interactivedata_functionalgrouprefno',
            'sourcedata_interactivedata_isinteractive',
            'sourcedata_interactivedata_route',
            'sourcedata_interactivedata_senderid',
            'sourcedata_interactivedata_variant',
            'sourcedata_source',
            'sourcedata_subject',
            'sourcedata_type',
            'manifestdetails_datetimereceived',
            'manifestdetails_manifestguid',
            'manifestdetails_datatype',
            'manifestdetails_protocol',
            's3_location',
            'xml_file_name',
            'file_name',
            'extra_rec_type']

        csv_file = "/tmp/api.csv"
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(
                csvfile,
                fieldnames=csv_cols,
                quoting=csv.QUOTE_ALL)
            writer.writeheader()
            for data in results_list:
                writer.writerow(data)

    except Exception as err:
        error_handler(sys.exc_info()[2].tb_lineno, err)


def flatten_json(nested_json):
    """
        Flatten json object with nested keys into a single level.
        Args:
            nested_json: A nested json object.
        Returns:
            The flattened json object if successful, None otherwise.
    """
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(nested_json)
    return out



# pylint: disable=unused-argument
def mymain(event, context):
    """
    Respond to triggering event by running Athena SQL.

    Args:
        event (dict)           : Data about the triggering event
        context (LamdaContext) : Runtime information

    Returns:
        null
    """
    LOGGER.info('The following event was received:')
    LOGGER.info(event)

    try:
        global LOG_GROUP_NAME
        global LOG_STREAM_NAME
        LOG_GROUP_NAME = context.log_group_name
        LOG_STREAM_NAME = context.log_stream_name

        bucket_name = 's3-dq-api-cdlz-msk-test'
        key_name = 'parsed/2021-07-21/06:02:56.352746964'
        path_name = get_path_name(key_name)
        file_name = get_file_name(key_name)
        key_size = '2984644'
        prefix = '/'.join(path_name.split('/')[1:])

        now = datetime.datetime.now()
        target_bucket_name = os.environ['output_bucket_name']
        failed_to_parse_loc = 'failed_to_parse/api/' + now.isoformat() + '/'

        LOGGER.info('Bucket name: %s', bucket_name)
        LOGGER.info('Path name: %s', path_name)
        LOGGER.info('Key name: %s', key_name)
        LOGGER.info('File name: %s', file_name)
        LOGGER.info('Key size: %s', key_size)
        LOGGER.info('Prefix: %s', prefix)

        if not file_name:
            LOGGER.error('No file found in S3. Exiting with error')
            sys.exit(1)

        pattern = re.compile("PARSED_[0-9]{8}_[0-9]{4}_[0-9]{4}.*\.jsonl$")
        if not pattern.match(file_name):
            LOGGER.info('Non-parsed file received. Ignoring. Actual file received: %s', file_name)
            return

        if prefix_exists(target_bucket_name, 'working/' + prefix):
            return

        if file_exists(target_bucket_name, file_name):
            return

        clear_container()
        downloaded_file = download_s3_file(bucket_name, key_name)
        LOGGER.info('Downloaded the following: %s', downloaded_file)

        processed_files = 0
        ignored_files = 0
        bad_files = 0
        total_docdetails = 0
        total_files_with_docdetails = 0
        files_processed = []

        parsedfile = open(downloaded_file, "r")
        for eachjsonrec in parsedfile:
            res = json.loads(eachjsonrec)
            all_fields = flatten_json(res)
            apidata = {}

            # if xml_file and zip_file are not present then don't process the file.

            if(all_fields.get('header_sourceFilename') is None):
                LOGGER.info('Could not process. Bad file. no XML file name present')
                bad_files =  bad_files + 1
                continue

            if(all_fields.get('header_sourceZipArchive') is None):
                LOGGER.info('Could not process. Bad file. no ZIP file name present')
                bad_files =  bad_files + 1
                continue

            xml_file = all_fields.get('header_sourceFilename').split('/')[-1]
            zip_file = all_fields.get('header_sourceZipArchive').split('/')[-1]
            # Check if xml file is already processed.
            # New function xml_file_exists
            if xml_file_exists(target_bucket_name, zip_file, xml_file):
                ignored_files =  ignored_files + 1
                LOGGER.info('XML file %s of zip file %s ignored as it has already been processed', xml_file, zip_file)
                continue


            expected_docdetails = len(res.get('body',{}).get('commonAPIPlus',{}).get('APIData',{}).get('passengerDetails',{}).get('documentDetails',{}))
            LOGGER.info('No of Document Details Found: %s', expected_docdetails)

            # result-1'APIData'
            # result-1 sendingPartyDetails
            apidata['sendingpartydetails_contactid'] = all_fields.get('body_commonAPIPlus_APIData_sendingPartyDetails_contactId')
            apidata['sendingpartydetails_contactname'] = all_fields.get('body_commonAPIPlus_APIData_sendingPartyDetails_contactName')
            apidata['sendingpartydetails_firstcommsaddressid'] = all_fields.get('body_commonAPIPlus_APIData_sendingPartyDetails_firstCommsAddressId')
            # incorrect
            apidata['sendingpartydetails_firstcommsaddresscode'] = all_fields.get('body_commonAPIPlus_APIData_sendingPartyDetails_firstCommsAddressCode')
            apidata['sendingpartydetails_secondcommsaddresscode'] = all_fields.get('body_commonAPIPlus_APIData_sendingPartyDetails_secondCommsAddressCode')
            apidata['sendingpartydetails_secondcommsaddressid'] = all_fields.get('body_commonAPIPlus_APIData_sendingPartyDetails_secondCommsAddressId')

            # result-1 flightDetails
            apidata['flightdetails_flightid'] = all_fields.get('body_commonAPIPlus_APIData_flightDetails_flightId')
            apidata['flightdetails_arrivalairport'] = all_fields.get('body_commonAPIPlus_APIData_flightDetails_arrivalAirport')

            try:
                adt = all_fields.get('body_commonAPIPlus_APIData_flightDetails_arrivalDateTime')
                time.strptime(adt[11:], '%H:%M:%S')
                time.strptime(adt[:10], '%Y-%m-%d')
                apidata['flightdetails_arrivaldatetime'] = adt
            except ValueError:
                LOGGER.info('Invalid Arrival date - flightdetails_arrivaldatetime: %s', adt)
                try:
                    apidata['flightdetails_arrivaldatetime'] = datetime.datetime.strptime(adt[:10], '%Y-%m-%d')
                except Exception:
                    apidata['flightdetails_arrivaldatetime'] = "1900-01-01 00:00:00"


            apidata['flightdetails_arrivaldatetimeutc'] = all_fields.get('body_commonAPIPlus_APIData_flightDetails_arrivalDateTimeUTC')
            apidata['flightdetails_cargo'] = all_fields.get('body_commonAPIPlus_APIData_flightDetails_cargo')
            apidata['flightdetails_carrier'] = all_fields.get('body_commonAPIPlus_APIData_flightDetails_carrier')
            apidata['flightdetails_carriertype'] = all_fields.get('body_commonAPIPlus_APIData_flightDetails_carrierType')
            apidata['flightdetails_craftid'] = all_fields.get('body_commonAPIPlus_APIData_flightDetails_craftId')
            apidata['flightdetails_crewcount'] = all_fields.get('body_commonAPIPlus_APIData_flightDetails_crewCount')
            apidata['flightdetails_datetimesent'] = all_fields.get('body_commonAPIPlus_APIData_flightDetails_dateTimeSent')
            apidata['flightdetails_departureairport'] = all_fields.get('body_commonAPIPlus_APIData_flightDetails_departureAirport')

            try:
                ddt = all_fields.get('body_commonAPIPlus_APIData_flightDetails_departureDateTime')
                time.strptime(ddt[11:], '%H:%M:%S')
                time.strptime(ddt[:10], '%Y-%m-%d')
                apidata['flightdetails_departuredatetime'] = ddt

            except ValueError:
                LOGGER.info('Invalid Departure date - flightDetails_departureDateTime: %s', ddt)
                try:
                    apidata['flightdetails_departuredatetime'] = datetime.datetime.strptime(ddt[:10], '%Y-%m-%d')
                except Exception:
                    apidata['flightdetails_departuredatetime'] = "1900-01-01 00:00:00"

            apidata['flightdetails_departuredatetimeutc'] = all_fields.get('body_commonAPIPlus_APIData_flightDetails_departureDateTimeUTC')
            apidata['flightdetails_eventcode'] = all_fields.get('body_commonAPIPlus_APIData_flightDetails_eventCode')
            apidata['flightdetails_exception'] = all_fields.get('body_commonAPIPlus_APIData_flightDetails_exception')
            apidata['flightdetails_hireorcharter'] = all_fields.get('body_commonAPIPlus_APIData_flightDetails_hireOrCharter')
            apidata['flightdetails_hireorcharterdetails'] = all_fields.get('body_commonAPIPlus_APIData_flightDetails_hireOrCharterDetails')
            apidata['flightdetails_manifesttype'] = all_fields.get('body_commonAPIPlus_APIData_flightDetails_manifestType')
            apidata['flightdetails_passengercount'] = all_fields.get('body_commonAPIPlus_APIData_flightDetails_passengerCount')
            apidata['flightdetails_rawflightid'] = all_fields.get('body_commonAPIPlus_APIData_flightDetails_rawFlightId')
            apidata['flightdetails_route'] = all_fields.get('body_commonAPIPlus_APIData_flightDetails_route')
            apidata['flightdetails_subsequentport'] = all_fields.get('body_commonAPIPlus_APIData_flightDetails_subsequentPort')

            apidata['flightdetails_operatoraddress_addressline'] = all_fields.get('body_commonAPIPlus_APIData_flightDetails_operatorAddress_addressLine_0')
            apidata['flightdetails_operatoraddress_country'] = all_fields.get('body_commonAPIPlus_APIData_flightDetails_operatorAddress_country')
            apidata['flightdetails_operatoraddress_postcode'] = all_fields.get('body_commonAPIPlus_APIData_flightDetails_operatorAddress_postCode')

            apidata['flightdetails_operatorname_firstname'] = all_fields.get('body_commonAPIPlus_APIData_flightDetails_operatorName_firstName')
            apidata['flightdetails_operatorname_middlename'] = all_fields.get('body_commonAPIPlus_APIData_flightDetails_operatorName_middleName')
            apidata['flightdetails_operatorname_surname'] = all_fields.get('body_commonAPIPlus_APIData_flightDetails_operatorName_surname')

            apidata['flightdetails_arrivalairportextended_description'] = all_fields.get('body_commonAPIPlus_APIData_flightDetails_arrivalAirportExtended_description')
            apidata['flightdetails_arrivalairportextended_iatacode'] = all_fields.get('body_commonAPIPlus_APIData_flightDetails_arrivalAirportExtended_iataCode')
            apidata['flightdetails_arrivalairportextended_icaocode'] = all_fields.get('body_commonAPIPlus_APIData_flightDetails_arrivalAirportExtended_icaoCode')
            apidata['flightdetails_arrivalairportextended_unlocode'] = all_fields.get('body_commonAPIPlus_APIData_flightDetails_arrivalAirportExtended_unloCode')

            apidata['flightdetails_arrivalairportextended_address_country'] = all_fields.get('body_commonAPIPlus_APIData_flightDetails_arrivalAirportExtended_address_country')
            apidata['flightdetails_arrivalairportextended_address_addressline'] = all_fields.get('body_commonAPIPlus_APIData_flightDetails_arrivalAirportExtended_address_addressLine_0')
            # wrong. above field not found.
            apidata['flightdetails_arrivalairportextended_address_postcode'] = all_fields.get('body_commonAPIPlus_APIData_flightDetails_arrivalAirportExtended_address_postCode')

            apidata['flightdetails_arrivalairportextended_coordinates_latitude'] = all_fields.get('body_commonAPIPlus_APIData_flightDetails_arrivalAirportExtended_coordinates_latitude')
            apidata['flightdetails_arrivalairportextended_coordinates_longitude'] = all_fields.get('body_commonAPIPlus_APIData_flightDetails_arrivalAirportExtended_coordinates_longitude')

            # Departure. Fixed by Sid.
            apidata['flightdetails_departureairportextended_description'] = all_fields.get('body_commonAPIPlus_APIData_flightDetails_departureAirportExtended_description')
            apidata['flightdetails_departureairportextended_iatacode'] = all_fields.get('body_commonAPIPlus_APIData_flightDetails_departureAirportExtended_iataCode')
            apidata['flightdetails_departureairportextended_icaocode'] = all_fields.get('body_commonAPIPlus_APIData_flightDetails_departureAirportExtended_icaoCode')
            apidata['flightdetails_departureairportextended_unlocode'] = all_fields.get('body_commonAPIPlus_APIData_flightDetails_departureAirportExtended_unloCode')

            apidata['flightdetails_departureairportextended_address_country'] = all_fields.get('body_commonAPIPlus_APIData_flightDetails_departureAirportExtended_address_country')
            apidata['flightdetails_departureairportextended_address_addressline'] = all_fields.get('body_commonAPIPlus_APIData_flightDetails_departureAirportExtended_address_addressLine_0')

            apidata['flightdetails_departureairportextended_address_postcode'] = all_fields.get('body_commonAPIPlus_APIData_flightDetails_departureAirportExtended_address_postCode')

            apidata['flightdetails_departureairportextended_coordinates_latitude'] = all_fields.get('body_commonAPIPlus_APIData_flightDetails_departureAirportExtended_coordinates_latitude')
            apidata['flightdetails_departureairportextended_coordinates_longitude'] = all_fields.get('body_commonAPIPlus_APIData_flightDetails_departureAirportExtended_coordinates_longitude')

            # result-1 craftDetails
            apidata['craftdetails_make'] = all_fields.get('body_commonAPIPlus_APIData_craftDetails_make')
            apidata['craftdetails_model'] = all_fields.get('body_commonAPIPlus_APIData_craftDetails_model')
            apidata['craftdetails_ownerorganisation'] = all_fields.get('body_commonAPIPlus_APIData_craftDetails_ownerOrganisation')
            apidata['craftdetails_imonumber'] = all_fields.get('body_commonAPIPlus_APIData_craftDetails_imoNumber')
            apidata['craftdetails_imodate'] = all_fields.get('body_commonAPIPlus_APIData_craftDetails_imoDate')
            apidata['craftdetails_mmsinumber'] = all_fields.get('body_commonAPIPlus_APIData_craftDetails_mmsiNumber')
            apidata['craftdetails_callsign'] = all_fields.get('body_commonAPIPlus_APIData_craftDetails_callSign')
            apidata['craftdetails_hullcolour'] = all_fields.get('body_commonAPIPlus_APIData_craftDetails_hullColour')
            apidata['craftdetails_metrelength'] = all_fields.get('body_commonAPIPlus_APIData_craftDetails_metreLength')
            apidata['craftdetails_registrationno'] = all_fields.get('body_commonAPIPlus_APIData_craftDetails_registrationNo')
            apidata['craftdetails_registrationcountrycode'] = all_fields.get('body_commonAPIPlus_APIData_craftDetails_registrationCountryCode')
            apidata['craftdetails_sailmarkings'] = all_fields.get('body_commonAPIPlus_APIData_craftDetails_sailMarkings')
            apidata['craftdetails_tonnage'] = all_fields.get('body_commonAPIPlus_APIData_craftDetails_tonnage')
            apidata['craftdetails_transporttype'] = all_fields.get('body_commonAPIPlus_APIData_craftDetails_transportType')
            apidata['craftdetails_type'] = all_fields.get('body_commonAPIPlus_APIData_craftDetails_type')
            apidata['craftdetails_vesselname'] = all_fields.get('body_commonAPIPlus_APIData_craftDetails_vesselName')
            apidata['craftdetails_yearbuilt'] = all_fields.get('body_commonAPIPlus_APIData_craftDetails_yearBuilt')

            apidata['craftdetails_portofregistration_type'] = all_fields.get('body_commonAPIPlus_APIData_craftDetails_portOfRegistration_type')

            apidata['craftdetails_portofregistration_location_iatacode'] = all_fields.get('body_commonAPIPlus_APIData_craftDetails_portOfRegistration_location_iataCode')
            apidata['craftdetails_portofregistration_location_icaocode'] = all_fields.get('body_commonAPIPlus_APIData_craftDetails_portOfRegistration_location_icaoCode')
            apidata['craftdetails_portofregistration_location_unlocode'] = all_fields.get('body_commonAPIPlus_APIData_craftDetails_portOfRegistration_location_unloCode')
            apidata['craftdetails_portofregistration_location_description'] = all_fields.get('body_commonAPIPlus_APIData_craftDetails_portOfRegistration_location_description')

            apidata['craftdetails_portofregistration_location_address_addressline'] = all_fields.get('body_commonAPIPlus_APIData_craftDetails_portOfRegistration_location_address_addressLine_0')
            apidata['craftdetails_portofregistration_location_address_country'] = all_fields.get('body_commonAPIPlus_APIData_craftDetails_portOfRegistration_location_address_country')
            apidata['craftdetails_portofregistration_location_address_postcode'] = all_fields.get('body_commonAPIPlus_APIData_craftDetails_portOfRegistration_location_address_postCode')

            apidata['craftdetails_portofregistration_location_coordinates_latitude'] = all_fields.get('body_commonAPIPlus_APIData_craftDetails_portOfRegistration_location_coordinates_latitude')
            apidata['craftdetails_portofregistration_location_coordinates_longitude'] = all_fields.get('body_commonAPIPlus_APIData_craftDetails_portOfRegistration_location_coordinates_longitude')

            apidata['craftdetails_imoregistryplace_location_iatacode'] = all_fields.get('body_commonAPIPlus_APIData_craftDetails_imoRegistryPlace_location_iataCode')
            apidata['craftdetails_imoregistryplace_location_icaocode'] = all_fields.get('body_commonAPIPlus_APIData_craftDetails_imoRegistryPlace_location_icaoCode')
            apidata['craftdetails_imoregistryplace_location_unlocode'] = all_fields.get('body_commonAPIPlus_APIData_craftDetails_imoRegistryPlace_location_unloCode')
            apidata['craftdetails_imoregistryplace_location_description'] = all_fields.get('body_commonAPIPlus_APIData_craftDetails_imoRegistryPlace_location_description')

            apidata['craftdetails_imoregistryplace_location_coordinates_latitude'] = all_fields.get('body_commonAPIPlus_APIData_craftDetails_imoRegistryPlace_location_coordinates_latitude')
            apidata['craftdetails_imoregistryplace_location_coordinates_longitude'] = all_fields.get('body_commonAPIPlus_APIData_craftDetails_imoRegistryPlace_location_coordinates_longitude')

            apidata['craftdetails_imoregistryplace_location_address_addressline'] = all_fields.get('body_commonAPIPlus_APIData_craftDetails_imoRegistryPlace_location_address_addressLine_0')
            apidata['craftdetails_imoregistryplace_location_address_country'] = all_fields.get('body_commonAPIPlus_APIData_craftDetails_imoRegistryPlace_location_address_country')
            apidata['craftdetails_imoregistryplace_location_address_postcode'] = all_fields.get('body_commonAPIPlus_APIData_craftDetails_imoRegistryPlace_location_address_postCode')

            apidata['craftdetails_ownername_firstname'] = all_fields.get('body_commonAPIPlus_APIData_craftDetails_ownerName_firstName')
            apidata['craftdetails_ownername_middlename'] = all_fields.get('body_commonAPIPlus_APIData_craftDetails_ownerName_middleName')
            apidata['craftdetails_ownername_surname'] = all_fields.get('body_commonAPIPlus_APIData_craftDetails_ownerName_surname')

            # end of apidata.
            # Start flightitinerary_departures locationfunctioncode == '125'
            # body_commonAPIPlus_APIData_flightItinerary_0_locationFunctionCode
            # body_commonAPIPlus_APIData_flightItinerary_1_locationNameCode
            # result-2 and result-3
            # flightitinerary_arrivals and flightitinerary_departures
            dep_flag='0'
            arr_flag='1'
            flightitinerary_departures = {}
            flightitinerary_arrivals = {}
            if (all_fields.get('body_commonAPIPlus_APIData_flightItinerary_0_locationFunctionCode') == '125'):
                dep_flag='0'
            elif(all_fields.get('body_commonAPIPlus_APIData_flightItinerary_0_locationFunctionCode') == '87'):
                arr_flag='0'

            if (all_fields.get('body_commonAPIPlus_APIData_flightItinerary_1_locationFunctionCode') == '87'):
                arr_flag='1'
            elif(all_fields.get('body_commonAPIPlus_APIData_flightItinerary_1_locationFunctionCode') == '125'):
                dep_flag='1'


            flightitinerary_departures['flightitinerary_departure_locationfunctioncode'] = all_fields.get('body_commonAPIPlus_APIData_flightItinerary_' + dep_flag + '_locationFunctionCode')
            flightitinerary_departures['flightitinerary_departure_locationnamecode'] = all_fields.get('body_commonAPIPlus_APIData_flightItinerary_' + dep_flag + '_locationNameCode')


            #flightitinerary_departures['flightitinerary_departuredatetime'] = all_fields.get('body_commonAPIPlus_APIData_flightItinerary_' + dep_flag + '_departureDateTime')
            try:
                iddt = all_fields.get('body_commonAPIPlus_APIData_flightItinerary_' + dep_flag + '_departureDateTime')
                time.strptime(iddt[11:], '%H:%M:%S')
                time.strptime(iddt[:10], '%Y-%m-%d')
                flightitinerary_departures['flightitinerary_departuredatetime'] = iddt
            except ValueError:
                LOGGER.info('Invalid Arrival date - flightitinerary_departuredatetime: %s', iddt)
                try:
                    flightitinerary_departures['flightitinerary_departuredatetime'] = datetime.datetime.strptime(iddt[:10], '%Y-%m-%d')
                except Exception:
                    flightitinerary_departures['flightitinerary_departuredatetime'] = "1900-01-01 00:00:00"


            flightitinerary_departures['flightitinerary_departure_locationnameextended_iatacode'] = all_fields.get('body_commonAPIPlus_APIData_flightItinerary_' + dep_flag + '_locationNameExtended_iataCode')
            flightitinerary_departures['flightitinerary_departure_locationnameextended_icaocode'] = all_fields.get('body_commonAPIPlus_APIData_flightItinerary_' + dep_flag + '_locationNameExtended_icaoCode')

            # flightitinerary_arrival Arrivals locationfunctioncode == '87'
            flightitinerary_arrivals['flightitinerary_arrival_locationfunctioncode'] = all_fields.get('body_commonAPIPlus_APIData_flightItinerary_' + arr_flag + '_locationFunctionCode')
            flightitinerary_arrivals['flightitinerary_arrival_locationnamecode'] = all_fields.get('body_commonAPIPlus_APIData_flightItinerary_' + arr_flag + '_locationNameCode')


            #flightitinerary_arrivals['flightitinerary_arrivaldatetime'] = all_fields.get('body_commonAPIPlus_APIData_flightItinerary_' + arr_flag + '_arrivalDateTime')

            try:
                iadt = all_fields.get('body_commonAPIPlus_APIData_flightItinerary_' + arr_flag + '_arrivalDateTime')
                time.strptime(iadt[11:], '%H:%M:%S')
                time.strptime(iadt[:10], '%Y-%m-%d')
                flightitinerary_arrivals['flightitinerary_arrivaldatetime'] = iadt
            except ValueError:
                LOGGER.info('Invalid Arrival date - flightitinerary_arrivaldatetime: %s', iadt)
                try:
                    flightitinerary_arrivals['flightitinerary_arrivaldatetime'] = datetime.datetime.strptime(iadt[:10], '%Y-%m-%d')
                except Exception:
                    flightitinerary_arrivals['flightitinerary_arrivaldatetime'] = "1900-01-01 00:00:00"


            flightitinerary_arrivals['flightitinerary_arrival_locationnameextended_iatacode'] = all_fields.get('body_commonAPIPlus_APIData_flightItinerary_' + arr_flag + '_locationNameExtended_iataCode')
            flightitinerary_arrivals['flightitinerary_arrival_locationnameextended_icaocode'] = all_fields.get('body_commonAPIPlus_APIData_flightItinerary_' + arr_flag + '_locationNameExtended_icaoCode')

            # manifest details.
            # result-4
            manifestdetails = {}

            manifestdetails['manifestdetails_datatype'] = all_fields.get('body_commonAPIPlus_manifestDetails_dataType')
            manifestdetails['manifestdetails_datetimereceived'] = all_fields.get('body_commonAPIPlus_manifestDetails_datetimeReceived')
            manifestdetails['manifestdetails_manifestguid'] = all_fields.get('body_commonAPIPlus_manifestDetails_manifestGUID')
            manifestdetails['manifestdetails_protocol'] = all_fields.get('body_commonAPIPlus_manifestDetails_protocol')

            # source data.
            # result-5
            sourcedetails = {}

            sourcedetails['sourcedata_component'] = all_fields.get('body_commonAPIPlus_SourceData_0_Component')
            sourcedetails['sourcedata_source'] = all_fields.get('body_commonAPIPlus_SourceData_0_Source')
            sourcedetails['sourcedata_subject'] = '' if(all_fields.get('body_commonAPIPlus_SourceData_0_Subject') is None) else all_fields.get('body_commonAPIPlus_SourceData_0_Subject').replace('\n', '')
            sourcedetails['sourcedata_type'] = all_fields.get('body_commonAPIPlus_SourceData_0_Type')

            sourcedetails['sourcedata_interactivedata_commonaccessref'] = all_fields.get('body_commonAPIPlus_SourceData_0_interactiveData_0_commonAccessRef')
            sourcedetails['sourcedata_interactivedata_functionalgrouprefno'] = all_fields.get('body_commonAPIPlus_SourceData_0_interactiveData_0_functionalGroupRefNo')
            sourcedetails['sourcedata_interactivedata_isinteractive'] = all_fields.get('body_commonAPIPlus_SourceData_0_interactiveData_0_isInteractive')
            sourcedetails['sourcedata_interactivedata_route'] = all_fields.get('body_commonAPIPlus_SourceData_0_interactiveData_0_route')
            sourcedetails['sourcedata_interactivedata_senderid'] = all_fields.get('body_commonAPIPlus_SourceData_0_interactiveData_0_senderId')
            sourcedetails['sourcedata_interactivedata_variant'] = all_fields.get('body_commonAPIPlus_SourceData_0_interactiveData_0_variant')

            # PNR Must not store PNR Details.
            # result-6
            pnrdetails = {}
            pnrdetails['pnrdetails_accompaniedbyinfant'] = None
            pnrdetails['pnrdetails_unaccompaniedminor'] = None
            pnrdetails['pnrdetails_bookingdate'] = None
            pnrdetails['pnrdetails_creationdate'] = None
            pnrdetails['pnrdetails_masterpnrlocator'] = None
            pnrdetails['pnrdetails_modifieddate'] = None
            pnrdetails['pnrdetails_pnrlocator'] = None
            pnrdetails['pnrdetails_retrieveddate'] = None
            pnrdetails['pnrdetails_splitpnr'] = None
            pnrdetails['pnrdetails_travelagent'] = None

            # Passenger Details.
            # result-7
            passengerdetails = {}
            passengerdetails['passengerdetails_age'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_age')
            passengerdetails['passengerdetails_city'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_city')
            passengerdetails['passengerdetails_country'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_country')
            passengerdetails['passengerdetails_countryofresidence'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_countryOfResidence')
            passengerdetails['passengerdetails_dateofbirth'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_dateOfBirth')
            passengerdetails['passengerdetails_firstname'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_firstName')
            passengerdetails['passengerdetails_gender'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_gender')
            passengerdetails['passengerdetails_intransitflag'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_inTransitFlag')
            passengerdetails['passengerdetails_lengthofstayinuk'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_lengthOfStayInUK')
            passengerdetails['passengerdetails_nationality'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_nationality')
            passengerdetails['passengerdetails_officeofclearance'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_officeOfClearance')
            passengerdetails['passengerdetails_passengertype'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_passengerType')
            passengerdetails['passengerdetails_placeofbirth'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_placeOfBirth')
            passengerdetails['passengerdetails_pnrlocator'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_pnrLocator')
            passengerdetails['passengerdetails_portofdisembark'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_portOfDisembark')
            passengerdetails['passengerdetails_portofembark'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_portOfEmbark')
            passengerdetails['passengerdetails_postalcode'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_postalCode')
            passengerdetails['passengerdetails_purposeofvisit'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_purposeOfVisit')
            passengerdetails['passengerdetails_rankrating'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_rankRating')
            passengerdetails['passengerdetails_secondname'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_secondName')
            passengerdetails['passengerdetails_state'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_state')
            passengerdetails['passengerdetails_street'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_street')
            passengerdetails['passengerdetails_surname'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_surname')
            passengerdetails['passengerdetails_visaholder'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_visaHolder')

            passengerdetails['passengerdetails_contactnumber_phonenumber'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_contactNumber_phoneNumber')
            passengerdetails['passengerdetails_contactnumber_phonenumbertype'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_contactNumber_phoneNumberType')

            passengerdetails['passengerdetails_crewallowance_goodsdetail'] = all_fields.get('')
            passengerdetails['passengerdetails_crewallowance_goodstodeclare'] = all_fields.get('')

            passengerdetails['passengerdetails_homeaddress_addressline'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_homeAddress_addressLine_0')
            passengerdetails['passengerdetails_homeaddress_country'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_homeAddress_country')
            passengerdetails['passengerdetails_homeaddress_postcode'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_homeAddress_postCode')

            passengerdetails['passengerdetails_interactivedetail_knowntravellerno'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_interactiveDetail_knownTravellerNo')
            passengerdetails['passengerdetails_interactivedetail_passengeridentifier'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_interactiveDetail_passengerIdentifier')
            # passengerIdentifier mapped twice in GP code?? Where is it available.
            passengerdetails['passengerdetails_passengeridentifier'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_interactiveDetail_passengerIdentifier')
            passengerdetails['passengerdetails_interactivedetail_redressno'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_interactiveDetail_redressNo')

            passengerdetails['passengerdetails_portofdisembarkationextended_iatacode'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_portOfDisembarkationExtended_iataCode')
            passengerdetails['passengerdetails_portofdisembarkationextended_icaocode'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_portOfDisembarkationExtended_icaoCode')
            passengerdetails['passengerdetails_portofdisembarkationextended_unlocode'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_portOfDisembarkationExtended_unloCode')

            passengerdetails['passengerdetails_portofdisembarkationextended_address_addressl'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_portOfDisembarkationExtended_address_addressLine_0')
            passengerdetails['passengerdetails_portofdisembarkationextended_address_postcode'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_portOfDisembarkationExtended_address_postCode')

            passengerdetails['passengerdetails_portofdisembarkationextended_coordinates_lati'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_portOfDisembarkationExtended_coordinates_latitude')
            passengerdetails['passengerdetails_portofdisembarkationextended_coordinates_long'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_portOfDisembarkationExtended_coordinates_longitude')

            passengerdetails['passengerdetails_vehicledetails_colour'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_vehicleDetails_colour')
            passengerdetails['passengerdetails_vehicledetails_make'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_vehicleDetails_make')
            passengerdetails['passengerdetails_vehicledetails_model'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_vehicleDetails_model')
            passengerdetails['passengerdetails_vehicledetails_registrationcountry'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_vehicleDetails_registrationCountry')
            passengerdetails['passengerdetails_vehicledetails_registrationnumber'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_vehicleDetails_registrationNumber')
            passengerdetails['passengerdetails_vehicledetails_vehicletype'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_vehicleDetails_vehicleType')
            passengerdetails['passengerdetails_vehicledetails_vin'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_vehicleDetails_vin')
            passengerdetails['passengerdetails_vehicledetails_year'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_vehicleDetails_year')

            # Passenger Details document details.
            ### Dont ignore . Handle this. May get multiple records.
            ### documentdetails = []
            # result-8

            '''
            passengerdetails_documentdetails = {}
            passengerdetails_documentdetails['passengerdetails_documentdetails_documenttype'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_documentDetails_0_documentType')
            passengerdetails_documentdetails['passengerdetails_documentdetails_documentno'] = '' if(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_documentDetails_0_documentNo') is None) else all_fields.get('body_commonAPIPlus_APIData_passengerDetails_documentDetails_0_documentNo').replace('\n', '')
            passengerdetails_documentdetails['passengerdetails_documentdetails_docissuedate'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_documentDetails_0_docIssueDate')
            passengerdetails_documentdetails['passengerdetails_documentdetails_docexpirationdate'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_documentDetails_0_docExpirationDate')
            passengerdetails_documentdetails['passengerdetails_documentdetails_countryofissue'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_documentDetails_0_countryOfIssue')
            passengerdetails_documentdetails['passengerdetails_documentdetails_cityofissue'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_documentDetails_0_cityOfIssue')
            '''
            ### documentdetails.append(passengerdetails_documentdetails)

            # dcs details.
            # result-9
            dcsdetails = {}

            dcsdetails['dcsdetails_flightsummary_airlinecode'] = all_fields.get('body_commonAPIPlus_dcsDetails_flightSummary_airlineCode')
            dcsdetails['dcsdetails_flightsummary_flightarrivalairport'] = all_fields.get('body_commonAPIPlus_dcsDetails_flightSummary_flightArrivalAirport')
            dcsdetails['dcsdetails_flightsummary_flightarrivaldate'] = all_fields.get('body_commonAPIPlus_dcsDetails_flightSummary_flightArrivalDate')
            dcsdetails['dcsdetails_flightsummary_flightarrivaltime'] = all_fields.get('body_commonAPIPlus_dcsDetails_flightSummary_flightArrivalTime')
            dcsdetails['dcsdetails_flightsummary_flightcode'] = all_fields.get('body_commonAPIPlus_dcsDetails_flightSummary_flightCode')
            dcsdetails['dcsdetails_flightsummary_flightdepartureairport'] = all_fields.get('body_commonAPIPlus_dcsDetails_flightSummary_flightDepartureAirport')
            dcsdetails['dcsdetails_flightsummary_flightdeparturedate'] = all_fields.get('body_commonAPIPlus_dcsDetails_flightSummary_flightDepartureDate')
            dcsdetails['dcsdetails_flightsummary_flightdeparturetime'] = all_fields.get('body_commonAPIPlus_dcsDetails_flightSummary_flightDepartureTime')
            dcsdetails['dcsdetails_flightsummary_rawflightcode'] = all_fields.get('body_commonAPIPlus_dcsDetails_flightSummary_rawFlightCode')

            dcsdetails['dcsdetails_dcsdata_dcsrecord_baggagedetail'] = all_fields.get('')
            dcsdetails['dcsdetails_dcsdata_dcsrecord_cabinclass'] = all_fields.get('')
            dcsdetails['dcsdetails_dcsdata_dcsrecord_carryoncount'] = all_fields.get('')
            dcsdetails['dcsdetails_dcsdata_dcsrecord_checkedincount'] = all_fields.get('')
            dcsdetails['dcsdetails_dcsdata_dcsrecord_checkedinweight'] = all_fields.get('')
            dcsdetails['dcsdetails_dcsdata_dcsrecord_checkinagent'] = all_fields.get('')
            dcsdetails['dcsdetails_dcsdata_dcsrecord_checkindatetime'] = all_fields.get('')
            dcsdetails['dcsdetails_dcsdata_dcsrecord_checkinlocation'] = all_fields.get('')
            dcsdetails['dcsdetails_dcsdata_dcsrecord_destination'] = all_fields.get('')
            dcsdetails['dcsdetails_dcsdata_dcsrecord_firstname'] = all_fields.get('')
            dcsdetails['dcsdetails_dcsdata_dcsrecord_frequentflyernumber'] = all_fields.get('')
            dcsdetails['dcsdetails_dcsdata_dcsrecord_passengerseq'] = all_fields.get('')
            dcsdetails['dcsdetails_dcsdata_dcsrecord_pnrlocator'] = all_fields.get('')
            dcsdetails['dcsdetails_dcsdata_dcsrecord_pooledto'] = all_fields.get('')
            dcsdetails['dcsdetails_dcsdata_dcsrecord_seatnumber'] = all_fields.get('')
            dcsdetails['dcsdetails_dcsdata_dcsrecord_securitynumber'] = all_fields.get('')
            dcsdetails['dcsdetails_dcsdata_dcsrecord_sequencenumber'] = all_fields.get('')
            dcsdetails['dcsdetails_dcsdata_dcsrecord_surname'] = all_fields.get('')
            dcsdetails['dcsdetails_dcsdata_dcsrecord_ticketnumber'] = all_fields.get('')
            dcsdetails['dcsdetails_dcsdata_dcsrecord_ticketstatus'] = all_fields.get('')

            dcsdetails['dcsdetails_dcsdata_dcsrecord_traveldocument_traveldocnumber'] = all_fields.get('')
            dcsdetails['dcsdetails_dcsdata_dcsrecord_traveldocument_traveldoctype'] = all_fields.get('')
            dcsdetails['dcsdetails_dcsdata_dcsrecord_traveldocument_traveldoclocofissue'] = all_fields.get('')
            dcsdetails['dcsdetails_dcsdata_dcsrecord_traveldocument_dateofbirth'] = all_fields.get('')
            dcsdetails['dcsdetails_dcsdata_dcsrecord_traveldocument_gender'] = all_fields.get('')
            dcsdetails['dcsdetails_dcsdata_dcsrecord_traveldocument_docissuedate'] = all_fields.get('')
            dcsdetails['dcsdetails_dcsdata_dcsrecord_traveldocument_docexpirationdate'] = all_fields.get('')
            dcsdetails['dcsdetails_dcsdata_dcsrecord_traveldocument_cityofissue'] = all_fields.get('')
            dcsdetails['dcsdetails_dcsdata_dcsrecord_traveldocument_pnrpassengerref'] = all_fields.get('')

            result = apidata.copy()
            result.update(passengerdetails)
            result.update(dcsdetails)
            result.update(pnrdetails)
            result.update(sourcedetails)
            result.update(manifestdetails)
            result.update(flightitinerary_arrivals)
            result.update(flightitinerary_departures)
            s3_file_name = key_name + '/' + all_fields.get('header_sourceFilename').split('/')[-1] + '/api.csv'
            # Key name: parsed/2020-06-28/16:23:59.764861894/PARSED_20200628_0810_9999.jsonl
            result.update({'s3_location': s3_file_name})
            # parsed.
            # parsed/2020-06-12/06:01:00.227909/PARSED_20200610_1820_9999_20200612033510.zip/2020-06-10T18-20-39Z_e160c302-6e1d-3903-ae16-484a1e631192_2cc3e859-b734-3d3b-9de0-36d34fe043b7_Parsed.xml/api.csv
            result.update({'xml_file_name': xml_file})
            result.update({'file_name': zip_file})
            result.update({'extra_rec_type': 'main'})
            #result.update(passengerdetails_documentdetails)

            results = []
            count_docdetails = 0
            files_with_docdetails = 0
            if(expected_docdetails > 0):
                documentdetails = []
                #
                passengerdetails_documentdetails = {}
                passengerdetails_documentdetails['passengerdetails_documentdetails_documenttype'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_documentDetails_0_documentType')
                passengerdetails_documentdetails['passengerdetails_documentdetails_documentno'] =  clean_newline(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_documentDetails_0_documentNo'))
                passengerdetails_documentdetails['passengerdetails_documentdetails_docissuedate'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_documentDetails_0_docIssueDate')
                passengerdetails_documentdetails['passengerdetails_documentdetails_docexpirationdate'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_documentDetails_0_docExpirationDate')
                passengerdetails_documentdetails['passengerdetails_documentdetails_countryofissue'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_documentDetails_0_countryOfIssue')
                passengerdetails_documentdetails['passengerdetails_documentdetails_cityofissue'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_documentDetails_0_cityOfIssue')
                documentdetails.append(passengerdetails_documentdetails)
                result.update(documentdetails[0])
                files_with_docdetails += 1
                count_docdetails += 1

                while(count_docdetails<expected_docdetails):

                    doc = {}
                    passengerdetails_documentdetails = {}
                    passengerdetails_documentdetails['passengerdetails_documentdetails_documenttype'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_documentDetails_' + str(count_docdetails) + '_documentType')
                    passengerdetails_documentdetails['passengerdetails_documentdetails_documentno'] = clean_newline(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_documentDetails_' + str(count_docdetails) + '_documentNo'))
                    passengerdetails_documentdetails['passengerdetails_documentdetails_docissuedate'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_documentDetails_' + str(count_docdetails) + '_docIssueDate')
                    passengerdetails_documentdetails['passengerdetails_documentdetails_docexpirationdate'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_documentDetails_' + str(count_docdetails) + '_docExpirationDate')
                    passengerdetails_documentdetails['passengerdetails_documentdetails_countryofissue'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_documentDetails_' + str(count_docdetails) + '_countryOfIssue')
                    passengerdetails_documentdetails['passengerdetails_documentdetails_cityofissue'] = all_fields.get('body_commonAPIPlus_APIData_passengerDetails_documentDetails_' + str(count_docdetails) + '_cityOfIssue')
                    documentdetails.append(passengerdetails_documentdetails)

                    doc = passengerdetails_documentdetails
                    doc.update({'manifestdetails_datetimereceived': manifestdetails['manifestdetails_datetimereceived']})
                    doc.update({'s3_location': s3_file_name})
                    doc.update({'xml_file_name': xml_file})
                    doc.update({'file_name': zip_file})
                    doc.update({'extra_rec_type': 'documentdetails'})
                    count_docdetails += 1
                    results.append(doc)



            # All docyment details logic.
            # there may be zero or more documentdetail entries
            # add the first one and then generate dummy rows for the rest
            # This needs to be done.  Separate lines for document details.
            # all_fields.get('header_sourceFilename').split('/')[-1]
            # all_fields.get('header_sourceZipArchive').split('/')[-1]

            results.append(result)

            create_csv(results)

            processed_files += 1
            files_processed.append((zip_file, xml_file))
            LOGGER.info('processed file %s : %s.', processed_files, xml_file)

            append_local()

            total_docdetails += count_docdetails
            total_files_with_docdetails += files_with_docdetails
            os.remove('/tmp/api.csv')


        parsedfile.close()
        print('Total processed files %s:',processed_files)
        LOGGER.info('No. files processed: %s', processed_files)
        LOGGER.info('No. bad files: %s', bad_files)
        LOGGER.info('No. files ignored: %s', ignored_files)
        LOGGER.info('No. files with a document details record: %s', total_files_with_docdetails)
        LOGGER.info('No. document details records: %s', total_docdetails)
        balancing_figure = processed_files - bad_files - ignored_files + (total_docdetails - total_files_with_docdetails)
        LOGGER.info('Total files less bad less ignored plus (total doc details less files with a doc detail record): %s', balancing_figure)
        if(processed_files == 0):
            LOGGER.info('No downstream processing required as no files to process. exiting. We are done.')
            return
        written_recs = recs_in_file('/tmp/full.csv', 'y')
        LOGGER.info('%s record(s) in file %s from %s',
                    written_recs,
                    '/tmp/full.csv',
                    downloaded_file.split('/')[-1])
        if written_recs != balancing_figure:
            LOGGER.warning('Mismatch between total records written out %s and the checksum figure %s', written_recs, balancing_figure)

        s3_file_name = s3_file_name.replace('parsed/', '')
        path_name = path_name.replace('parsed/', '')

        # Uses last filename
        upload_s3_object(
            '/tmp/full.csv',
            target_bucket_name,
            'working/' + s3_file_name)
        LOGGER.info('Upload complete')

        with open("/tmp/trigger.csv", "w") as trigger:
            trigger.write("API processing complete.")

        upload_s3_object(
            '/tmp/trigger.csv',
            target_bucket_name,
            'log/' + path_name + '/trigger.csv')

        upload_s3_object(
            '/tmp/trigger.csv',
            target_bucket_name,
            'log-fms/' + path_name + '/trigger.csv')

        upload_s3_object(
            '/tmp/trigger.csv',
            target_bucket_name,
            'log-drt/' + path_name + '/trigger.csv')

        # Upload file to S3 to show this file has already been processed
        audit_file = "/tmp/" + file_name
        with open(audit_file, 'w') as auditfile:
            auditfile.write('')

        upload_s3_object(
            audit_file,
            target_bucket_name,
            get_processed_file_location(file_name))


        # Upload xml file to S3 to show this file has already been processed
        for zip_file_name,xml_file_name in files_processed:
            audit_file = "/tmp/" + xml_file_name
            with open(audit_file, 'w') as auditfile:
                auditfile.write('')

            upload_s3_object(
                audit_file,
                target_bucket_name,
                get_processed_xmlfile_location(zip_file_name, xml_file_name))

        LOGGER.info('Trigger upload complete')

        LOGGER.info("We're done here.")
        return event

    except Exception as err:
        error_handler(sys.exc_info()[2].tb_lineno, err)
