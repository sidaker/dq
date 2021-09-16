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

        #csv_file = "/tmp/api" + str(idx) + ".csv"
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
def main():
    """

    """


    try:


        #bucket_name = event['Records'][0]['s3']['bucket']['name']
        downloaded_file = '/Users/sbommireddy/Downloads/PARSED_20201002_2226_9979.jsonl'


        processed_files = 0
        ignored_files = 0
        bad_files = 0
        total_docdetails = 0
        total_files_with_docdetails = 0
        files_processed = []

        parsedfile = open(downloaded_file, "r")
        for idx,eachjsonrec in enumerate(parsedfile):
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


            expected_docdetails = len(res.get('body',{}).get('commonAPIPlus',{}).get('APIData',{}).get('passengerDetails',{}).get('documentDetails',{}))
            LOGGER.info('No of Document Details Found: %s', expected_docdetails)

            # result-1'APIData'
            # result-1 sendingPartyDetails
            apidata['sendingpartydetails_contactid'] = type(all_fields.get('body_commonAPIPlus_APIData_sendingPartyDetails_contactId'))
            apidata['sendingpartydetails_contactname'] = type(all_fields.get('body_commonAPIPlus_APIData_sendingPartyDetails_contactName'))
            apidata['sendingpartydetails_firstcommsaddressid'] = type(all_fields.get('body_commonAPIPlus_APIData_sendingPartyDetails_firstCommsAddressId'))
            # incorrect
            apidata['sendingpartydetails_firstcommsaddresscode'] = type(all_fields.get('body_commonAPIPlus_APIData_sendingPartyDetails_firstCommsAddressCode'))
            apidata['sendingpartydetails_secondcommsaddresscode'] = type(all_fields.get('body_commonAPIPlus_APIData_sendingPartyDetails_secondCommsAddressCode'))
            apidata['sendingpartydetails_secondcommsaddressid'] = type(all_fields.get('body_commonAPIPlus_APIData_sendingPartyDetails_secondCommsAddressId'))

            # result-1 flightDetails
            apidata['flightdetails_flightid'] = type(all_fields.get('body_commonAPIPlus_APIData_flightDetails_flightId'))
            apidata['flightdetails_arrivalairport'] = type(all_fields.get('body_commonAPIPlus_APIData_flightDetails_arrivalAirport'))
            apidata['flightdetails_arrivaldatetime'] = type(all_fields.get('body_commonAPIPlus_APIData_flightDetails_arrivalDateTime'))
            apidata['flightdetails_arrivaldatetimeutc'] = type(all_fields.get('body_commonAPIPlus_APIData_flightDetails_arrivalDateTimeUTC'))
            apidata['flightdetails_cargo'] = type(all_fields.get('body_commonAPIPlus_APIData_flightDetails_cargo'))
            apidata['flightdetails_carrier'] = type(all_fields.get('body_commonAPIPlus_APIData_flightDetails_carrier'))
            apidata['flightdetails_carriertype'] = type(all_fields.get('body_commonAPIPlus_APIData_flightDetails_carrierType'))
            apidata['flightdetails_craftid'] = type(all_fields.get('body_commonAPIPlus_APIData_flightDetails_craftId'))
            apidata['flightdetails_crewcount'] = type(all_fields.get('body_commonAPIPlus_APIData_flightDetails_crewCount'))
            apidata['flightdetails_datetimesent'] = type(all_fields.get('body_commonAPIPlus_APIData_flightDetails_dateTimeSent'))
            apidata['flightdetails_departureairport'] = type(all_fields.get('body_commonAPIPlus_APIData_flightDetails_departureAirport'))
            apidata['flightdetails_departuredatetime'] = type(all_fields.get('body_commonAPIPlus_APIData_flightDetails_departureDateTime'))
            apidata['flightdetails_departuredatetimeutc'] = type(all_fields.get('body_commonAPIPlus_APIData_flightDetails_departureDateTimeUTC'))
            apidata['flightdetails_eventcode'] = type(all_fields.get('body_commonAPIPlus_APIData_flightDetails_eventCode'))
            apidata['flightdetails_exception'] = type(all_fields.get('body_commonAPIPlus_APIData_flightDetails_exception'))
            apidata['flightdetails_hireorcharter'] = type(all_fields.get('body_commonAPIPlus_APIData_flightDetails_hireOrCharter'))
            apidata['flightdetails_hireorcharterdetails'] = type(all_fields.get('body_commonAPIPlus_APIData_flightDetails_hireOrCharterDetails'))
            apidata['flightdetails_manifesttype'] = type(all_fields.get('body_commonAPIPlus_APIData_flightDetails_manifestType'))
            apidata['flightdetails_passengercount'] = type(all_fields.get('body_commonAPIPlus_APIData_flightDetails_passengerCount'))
            apidata['flightdetails_rawflightid'] = type(all_fields.get('body_commonAPIPlus_APIData_flightDetails_rawFlightId'))
            apidata['flightdetails_route'] = type(all_fields.get('body_commonAPIPlus_APIData_flightDetails_route'))
            apidata['flightdetails_subsequentport'] = type(all_fields.get('body_commonAPIPlus_APIData_flightDetails_subsequentPort'))

            apidata['flightdetails_operatoraddress_addressline'] = type(all_fields.get('body_commonAPIPlus_APIData_flightDetails_operatorAddress_addressLine_0'))
            apidata['flightdetails_operatoraddress_country'] = type(all_fields.get('body_commonAPIPlus_APIData_flightDetails_operatorAddress_country'))
            apidata['flightdetails_operatoraddress_postcode'] = type(all_fields.get('body_commonAPIPlus_APIData_flightDetails_operatorAddress_postCode'))

            apidata['flightdetails_operatorname_firstname'] = type(all_fields.get('body_commonAPIPlus_APIData_flightDetails_operatorName_firstName'))
            apidata['flightdetails_operatorname_middlename'] = type(all_fields.get('body_commonAPIPlus_APIData_flightDetails_operatorName_middleName'))
            apidata['flightdetails_operatorname_surname'] = type(all_fields.get('body_commonAPIPlus_APIData_flightDetails_operatorName_surname'))

            apidata['flightdetails_arrivalairportextended_description'] = type(all_fields.get('body_commonAPIPlus_APIData_flightDetails_arrivalAirportExtended_description'))
            apidata['flightdetails_arrivalairportextended_iatacode'] = type(all_fields.get('body_commonAPIPlus_APIData_flightDetails_arrivalAirportExtended_iataCode'))
            apidata['flightdetails_arrivalairportextended_icaocode'] = type(all_fields.get('body_commonAPIPlus_APIData_flightDetails_arrivalAirportExtended_icaoCode'))
            apidata['flightdetails_arrivalairportextended_unlocode'] = type(all_fields.get('body_commonAPIPlus_APIData_flightDetails_arrivalAirportExtended_unloCode'))

            apidata['flightdetails_arrivalairportextended_address_country'] = type(all_fields.get('body_commonAPIPlus_APIData_flightDetails_arrivalAirportExtended_address_country'))
            apidata['flightdetails_arrivalairportextended_address_addressline'] = type(all_fields.get('body_commonAPIPlus_APIData_flightDetails_arrivalAirportExtended_address_addressLine_0'))
            # wrong. above field not found.
            apidata['flightdetails_arrivalairportextended_address_postcode'] = type(all_fields.get('body_commonAPIPlus_APIData_flightDetails_arrivalAirportExtended_address_postCode'))

            apidata['flightdetails_arrivalairportextended_coordinates_latitude'] = type(all_fields.get('body_commonAPIPlus_APIData_flightDetails_arrivalAirportExtended_coordinates_latitude'))
            apidata['flightdetails_arrivalairportextended_coordinates_longitude'] = type(all_fields.get('body_commonAPIPlus_APIData_flightDetails_arrivalAirportExtended_coordinates_longitude'))

            # Departure. Fixed by Sid.
            apidata['flightdetails_departureairportextended_description'] = type(all_fields.get('body_commonAPIPlus_APIData_flightDetails_departureAirportExtended_description'))
            apidata['flightdetails_departureairportextended_iatacode'] = type(all_fields.get('body_commonAPIPlus_APIData_flightDetails_departureAirportExtended_iataCode'))
            apidata['flightdetails_departureairportextended_icaocode'] = type(all_fields.get('body_commonAPIPlus_APIData_flightDetails_departureAirportExtended_icaoCode'))
            apidata['flightdetails_departureairportextended_unlocode'] = type(all_fields.get('body_commonAPIPlus_APIData_flightDetails_departureAirportExtended_unloCode'))

            apidata['flightdetails_departureairportextended_address_country'] = type(all_fields.get('body_commonAPIPlus_APIData_flightDetails_departureAirportExtended_address_country'))
            apidata['flightdetails_departureairportextended_address_addressline'] = type(all_fields.get('body_commonAPIPlus_APIData_flightDetails_departureAirportExtended_address_addressLine_0'))

            apidata['flightdetails_departureairportextended_address_postcode'] = type(all_fields.get('body_commonAPIPlus_APIData_flightDetails_departureAirportExtended_address_postCode'))

            apidata['flightdetails_departureairportextended_coordinates_latitude'] = type(all_fields.get('body_commonAPIPlus_APIData_flightDetails_departureAirportExtended_coordinates_latitude'))
            apidata['flightdetails_departureairportextended_coordinates_longitude'] = type(all_fields.get('body_commonAPIPlus_APIData_flightDetails_departureAirportExtended_coordinates_longitude'))

            # result-1 craftDetails
            apidata['craftdetails_make'] = type(all_fields.get('body_commonAPIPlus_APIData_craftDetails_make'))
            apidata['craftdetails_model'] = type(all_fields.get('body_commonAPIPlus_APIData_craftDetails_model'))
            apidata['craftdetails_ownerorganisation'] = type(all_fields.get('body_commonAPIPlus_APIData_craftDetails_ownerOrganisation'))
            apidata['craftdetails_imonumber'] = type(all_fields.get('body_commonAPIPlus_APIData_craftDetails_imoNumber'))
            apidata['craftdetails_imodate'] = type(all_fields.get('body_commonAPIPlus_APIData_craftDetails_imoDate'))
            apidata['craftdetails_mmsinumber'] = type(all_fields.get('body_commonAPIPlus_APIData_craftDetails_mmsiNumber'))
            apidata['craftdetails_callsign'] = type(all_fields.get('body_commonAPIPlus_APIData_craftDetails_callSign'))
            apidata['craftdetails_hullcolour'] = type(all_fields.get('body_commonAPIPlus_APIData_craftDetails_hullColour'))
            apidata['craftdetails_metrelength'] = type(all_fields.get('body_commonAPIPlus_APIData_craftDetails_metreLength'))
            apidata['craftdetails_registrationno'] = type(all_fields.get('body_commonAPIPlus_APIData_craftDetails_registrationNo'))
            apidata['craftdetails_registrationcountrycode'] = type(all_fields.get('body_commonAPIPlus_APIData_craftDetails_registrationCountryCode'))
            apidata['craftdetails_sailmarkings'] = type(all_fields.get('body_commonAPIPlus_APIData_craftDetails_sailMarkings'))
            apidata['craftdetails_tonnage'] = type(all_fields.get('body_commonAPIPlus_APIData_craftDetails_tonnage'))
            apidata['craftdetails_transporttype'] = type(all_fields.get('body_commonAPIPlus_APIData_craftDetails_transportType'))
            apidata['craftdetails_type'] = type(all_fields.get('body_commonAPIPlus_APIData_craftDetails_type'))
            apidata['craftdetails_vesselname'] = type(all_fields.get('body_commonAPIPlus_APIData_craftDetails_vesselName'))
            apidata['craftdetails_yearbuilt'] = type(all_fields.get('body_commonAPIPlus_APIData_craftDetails_yearBuilt'))

            apidata['craftdetails_portofregistration_type'] = type(all_fields.get('body_commonAPIPlus_APIData_craftDetails_portOfRegistration_type'))

            apidata['craftdetails_portofregistration_location_iatacode'] = type(all_fields.get('body_commonAPIPlus_APIData_craftDetails_portOfRegistration_location_iataCode'))
            apidata['craftdetails_portofregistration_location_icaocode'] = type(all_fields.get('body_commonAPIPlus_APIData_craftDetails_portOfRegistration_location_icaoCode'))
            apidata['craftdetails_portofregistration_location_unlocode'] = type(all_fields.get('body_commonAPIPlus_APIData_craftDetails_portOfRegistration_location_unloCode'))
            apidata['craftdetails_portofregistration_location_description'] = type(all_fields.get('body_commonAPIPlus_APIData_craftDetails_portOfRegistration_location_description'))

            apidata['craftdetails_portofregistration_location_address_addressline'] = type(all_fields.get('body_commonAPIPlus_APIData_craftDetails_portOfRegistration_location_address_addressLine_0'))
            apidata['craftdetails_portofregistration_location_address_country'] = type(all_fields.get('body_commonAPIPlus_APIData_craftDetails_portOfRegistration_location_address_country'))
            apidata['craftdetails_portofregistration_location_address_postcode'] = type(all_fields.get('body_commonAPIPlus_APIData_craftDetails_portOfRegistration_location_address_postCode'))

            apidata['craftdetails_portofregistration_location_coordinates_latitude'] = type(all_fields.get('body_commonAPIPlus_APIData_craftDetails_portOfRegistration_location_coordinates_latitude'))
            apidata['craftdetails_portofregistration_location_coordinates_longitude'] = type(all_fields.get('body_commonAPIPlus_APIData_craftDetails_portOfRegistration_location_coordinates_longitude'))

            apidata['craftdetails_imoregistryplace_location_iatacode'] = type(all_fields.get('body_commonAPIPlus_APIData_craftDetails_imoRegistryPlace_location_iataCode'))
            apidata['craftdetails_imoregistryplace_location_icaocode'] = type(all_fields.get('body_commonAPIPlus_APIData_craftDetails_imoRegistryPlace_location_icaoCode'))
            apidata['craftdetails_imoregistryplace_location_unlocode'] = type(all_fields.get('body_commonAPIPlus_APIData_craftDetails_imoRegistryPlace_location_unloCode'))
            apidata['craftdetails_imoregistryplace_location_description'] = type(all_fields.get('body_commonAPIPlus_APIData_craftDetails_imoRegistryPlace_location_description'))

            apidata['craftdetails_imoregistryplace_location_coordinates_latitude'] = type(all_fields.get('body_commonAPIPlus_APIData_craftDetails_imoRegistryPlace_location_coordinates_latitude'))
            apidata['craftdetails_imoregistryplace_location_coordinates_longitude'] = type(all_fields.get('body_commonAPIPlus_APIData_craftDetails_imoRegistryPlace_location_coordinates_longitude'))

            apidata['craftdetails_imoregistryplace_location_address_addressline'] = type(all_fields.get('body_commonAPIPlus_APIData_craftDetails_imoRegistryPlace_location_address_addressLine_0'))
            apidata['craftdetails_imoregistryplace_location_address_country'] = type(all_fields.get('body_commonAPIPlus_APIData_craftDetails_imoRegistryPlace_location_address_country'))
            apidata['craftdetails_imoregistryplace_location_address_postcode'] = type(all_fields.get('body_commonAPIPlus_APIData_craftDetails_imoRegistryPlace_location_address_postCode'))

            apidata['craftdetails_ownername_firstname'] = type(all_fields.get('body_commonAPIPlus_APIData_craftDetails_ownerName_firstName'))
            apidata['craftdetails_ownername_middlename'] = type(all_fields.get('body_commonAPIPlus_APIData_craftDetails_ownerName_middleName'))
            apidata['craftdetails_ownername_surname'] = type(all_fields.get('body_commonAPIPlus_APIData_craftDetails_ownerName_surname'))

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


            flightitinerary_departures['flightitinerary_departure_locationfunctioncode'] = type(all_fields.get('body_commonAPIPlus_APIData_flightItinerary_' + dep_flag + '_locationFunctionCode'))
            flightitinerary_departures['flightitinerary_departure_locationnamecode'] = type(all_fields.get('body_commonAPIPlus_APIData_flightItinerary_' + dep_flag + '_locationNameCode'))
            flightitinerary_departures['flightitinerary_departuredatetime'] = type(all_fields.get('body_commonAPIPlus_APIData_flightItinerary_' + dep_flag + '_departureDateTime'))

            flightitinerary_departures['flightitinerary_departure_locationnameextended_iatacode'] = type(all_fields.get('body_commonAPIPlus_APIData_flightItinerary_' + dep_flag + '_locationNameExtended_iataCode'))
            flightitinerary_departures['flightitinerary_departure_locationnameextended_icaocode'] = type(all_fields.get('body_commonAPIPlus_APIData_flightItinerary_' + dep_flag + '_locationNameExtended_icaoCode'))

            # flightitinerary_arrival Arrivals locationfunctioncode == '87'
            flightitinerary_arrivals['flightitinerary_arrival_locationfunctioncode'] = type(all_fields.get('body_commonAPIPlus_APIData_flightItinerary_' + arr_flag + '_locationFunctionCode'))
            flightitinerary_arrivals['flightitinerary_arrival_locationnamecode'] = type(all_fields.get('body_commonAPIPlus_APIData_flightItinerary_' + arr_flag + '_locationNameCode'))
            flightitinerary_arrivals['flightitinerary_arrivaldatetime'] = type(all_fields.get('body_commonAPIPlus_APIData_flightItinerary_' + arr_flag + '_arrivalDateTime'))

            flightitinerary_arrivals['flightitinerary_arrival_locationnameextended_iatacode'] = type(all_fields.get('body_commonAPIPlus_APIData_flightItinerary_' + arr_flag + '_locationNameExtended_iataCode'))
            flightitinerary_arrivals['flightitinerary_arrival_locationnameextended_icaocode'] = type(all_fields.get('body_commonAPIPlus_APIData_flightItinerary_' + arr_flag + '_locationNameExtended_icaoCode'))

            # manifest details.
            # result-4
            manifestdetails = {}

            manifestdetails['manifestdetails_datatype'] = type(all_fields.get('body_commonAPIPlus_manifestDetails_dataType'))
            manifestdetails['manifestdetails_datetimereceived'] = type(all_fields.get('body_commonAPIPlus_manifestDetails_datetimeReceived'))
            manifestdetails['manifestdetails_manifestguid'] = type(all_fields.get('body_commonAPIPlus_manifestDetails_manifestGUID'))
            manifestdetails['manifestdetails_protocol'] = type(all_fields.get('body_commonAPIPlus_manifestDetails_protocol'))

            # source data.
            # result-5
            sourcedetails = {}

            sourcedetails['sourcedata_component'] = type(all_fields.get('body_commonAPIPlus_SourceData_0_Component'))
            sourcedetails['sourcedata_source'] = type(all_fields.get('body_commonAPIPlus_SourceData_0_Source'))
            sourcedetails['sourcedata_subject'] = type(all_fields.get('body_commonAPIPlus_SourceData_0_Subject'))
            sourcedetails['sourcedata_type'] = type(all_fields.get('body_commonAPIPlus_SourceData_0_Type'))

            sourcedetails['sourcedata_interactivedata_commonaccessref'] = type(all_fields.get('body_commonAPIPlus_SourceData_0_interactiveData_0_commonAccessRef'))
            sourcedetails['sourcedata_interactivedata_functionalgrouprefno'] = type(all_fields.get('body_commonAPIPlus_SourceData_0_interactiveData_0_functionalGroupRefNo'))
            sourcedetails['sourcedata_interactivedata_isinteractive'] = type(all_fields.get('body_commonAPIPlus_SourceData_0_interactiveData_0_isInteractive'))
            sourcedetails['sourcedata_interactivedata_route'] = type(all_fields.get('body_commonAPIPlus_SourceData_0_interactiveData_0_route'))
            sourcedetails['sourcedata_interactivedata_senderid'] = type(all_fields.get('body_commonAPIPlus_SourceData_0_interactiveData_0_senderId'))
            sourcedetails['sourcedata_interactivedata_variant'] = type(all_fields.get('body_commonAPIPlus_SourceData_0_interactiveData_0_variant'))

            # PNR Must not store PNR Details.
            # result-6
            pnrdetails = {}
            pnrdetails['pnrdetails_accompaniedbyinfant'] = type(None)
            pnrdetails['pnrdetails_unaccompaniedminor'] = type(None)
            pnrdetails['pnrdetails_bookingdate'] = type(None)
            pnrdetails['pnrdetails_creationdate'] = type(None)
            pnrdetails['pnrdetails_masterpnrlocator'] = type(None)
            pnrdetails['pnrdetails_modifieddate'] = type(None)
            pnrdetails['pnrdetails_pnrlocator'] = type(None)
            pnrdetails['pnrdetails_retrieveddate'] = type(None)
            pnrdetails['pnrdetails_splitpnr'] = type(None)
            pnrdetails['pnrdetails_travelagent'] = type(None)

            # Passenger Details.
            # result-7
            passengerdetails = {}
            passengerdetails['passengerdetails_age'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_age'))
            passengerdetails['passengerdetails_city'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_city'))
            passengerdetails['passengerdetails_country'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_country'))
            passengerdetails['passengerdetails_countryofresidence'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_countryOfResidence'))
            passengerdetails['passengerdetails_dateofbirth'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_dateOfBirth'))
            passengerdetails['passengerdetails_firstname'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_firstName'))
            passengerdetails['passengerdetails_gender'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_gender'))
            passengerdetails['passengerdetails_intransitflag'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_inTransitFlag'))
            passengerdetails['passengerdetails_lengthofstayinuk'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_lengthOfStayInUK'))
            passengerdetails['passengerdetails_nationality'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_nationality'))
            passengerdetails['passengerdetails_officeofclearance'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_officeOfClearance'))
            passengerdetails['passengerdetails_passengertype'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_passengerType'))
            passengerdetails['passengerdetails_placeofbirth'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_placeOfBirth'))
            passengerdetails['passengerdetails_pnrlocator'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_pnrLocator'))
            passengerdetails['passengerdetails_portofdisembark'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_portOfDisembark'))
            passengerdetails['passengerdetails_portofembark'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_portOfEmbark'))
            passengerdetails['passengerdetails_postalcode'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_postalCode'))
            passengerdetails['passengerdetails_purposeofvisit'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_purposeOfVisit'))
            passengerdetails['passengerdetails_rankrating'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_rankRating'))
            passengerdetails['passengerdetails_secondname'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_secondName'))
            passengerdetails['passengerdetails_state'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_state'))
            passengerdetails['passengerdetails_street'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_street'))
            passengerdetails['passengerdetails_surname'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_surname'))
            passengerdetails['passengerdetails_visaholder'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_visaHolder'))

            passengerdetails['passengerdetails_contactnumber_phonenumber'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_contactNumber_phoneNumber'))
            passengerdetails['passengerdetails_contactnumber_phonenumbertype'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_contactNumber_phoneNumberType'))

            passengerdetails['passengerdetails_crewallowance_goodsdetail'] = type(all_fields.get(''))
            passengerdetails['passengerdetails_crewallowance_goodstodeclare'] = type(all_fields.get(''))

            passengerdetails['passengerdetails_homeaddress_addressline'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_homeAddress_addressLine_0'))
            passengerdetails['passengerdetails_homeaddress_country'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_homeAddress_country'))
            passengerdetails['passengerdetails_homeaddress_postcode'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_homeAddress_postCode'))

            passengerdetails['passengerdetails_interactivedetail_knowntravellerno'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_interactiveDetail_knownTravellerNo'))
            passengerdetails['passengerdetails_interactivedetail_passengeridentifier'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_interactiveDetail_passengerIdentifier'))
            # passengerIdentifier mapped twice in GP code?? Where is it available.
            passengerdetails['passengerdetails_passengeridentifier'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_interactiveDetail_passengerIdentifier'))
            passengerdetails['passengerdetails_interactivedetail_redressno'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_interactiveDetail_redressNo'))

            passengerdetails['passengerdetails_portofdisembarkationextended_iatacode'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_portOfDisembarkationExtended_iataCode'))
            passengerdetails['passengerdetails_portofdisembarkationextended_icaocode'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_portOfDisembarkationExtended_icaoCode'))
            passengerdetails['passengerdetails_portofdisembarkationextended_unlocode'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_portOfDisembarkationExtended_unloCode'))

            passengerdetails['passengerdetails_portofdisembarkationextended_address_addressl'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_portOfDisembarkationExtended_address_addressLine_0'))
            passengerdetails['passengerdetails_portofdisembarkationextended_address_postcode'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_portOfDisembarkationExtended_address_postCode'))

            passengerdetails['passengerdetails_portofdisembarkationextended_coordinates_lati'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_portOfDisembarkationExtended_coordinates_latitude'))
            passengerdetails['passengerdetails_portofdisembarkationextended_coordinates_long'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_portOfDisembarkationExtended_coordinates_longitude'))

            passengerdetails['passengerdetails_vehicledetails_colour'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_vehicleDetails_colour'))
            passengerdetails['passengerdetails_vehicledetails_make'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_vehicleDetails_make'))
            passengerdetails['passengerdetails_vehicledetails_model'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_vehicleDetails_model'))
            passengerdetails['passengerdetails_vehicledetails_registrationcountry'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_vehicleDetails_registrationCountry'))
            passengerdetails['passengerdetails_vehicledetails_registrationnumber'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_vehicleDetails_registrationNumber'))
            passengerdetails['passengerdetails_vehicledetails_vehicletype'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_vehicleDetails_vehicleType'))
            passengerdetails['passengerdetails_vehicledetails_vin'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_vehicleDetails_vin'))
            passengerdetails['passengerdetails_vehicledetails_year'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_vehicleDetails_year'))

            # Passenger Details document details.
            ### Dont ignore . Handle this. May get multiple records.
            ### documentdetails = []
            # result-8

            '''
            passengerdetails_documentdetails = {}
            passengerdetails_documentdetails['passengerdetails_documentdetails_documenttype'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_documentDetails_0_documentType'))
            passengerdetails_documentdetails['passengerdetails_documentdetails_documentno'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_documentDetails_0_documentNo'))
            passengerdetails_documentdetails['passengerdetails_documentdetails_docissuedate'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_documentDetails_0_docIssueDate'))
            passengerdetails_documentdetails['passengerdetails_documentdetails_docexpirationdate'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_documentDetails_0_docExpirationDate'))
            passengerdetails_documentdetails['passengerdetails_documentdetails_countryofissue'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_documentDetails_0_countryOfIssue'))
            passengerdetails_documentdetails['passengerdetails_documentdetails_cityofissue'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_documentDetails_0_cityOfIssue'))
            '''
            ### documentdetails.append(passengerdetails_documentdetails)

            # dcs details.
            # result-9
            dcsdetails = {}

            dcsdetails['dcsdetails_flightsummary_airlinecode'] = type(all_fields.get('body_commonAPIPlus_dcsDetails_flightSummary_airlineCode'))
            dcsdetails['dcsdetails_flightsummary_flightarrivalairport'] = type(all_fields.get('body_commonAPIPlus_dcsDetails_flightSummary_flightArrivalAirport'))
            dcsdetails['dcsdetails_flightsummary_flightarrivaldate'] = type(all_fields.get('body_commonAPIPlus_dcsDetails_flightSummary_flightArrivalDate'))
            dcsdetails['dcsdetails_flightsummary_flightarrivaltime'] = type(all_fields.get('body_commonAPIPlus_dcsDetails_flightSummary_flightArrivalTime'))
            dcsdetails['dcsdetails_flightsummary_flightcode'] = type(all_fields.get('body_commonAPIPlus_dcsDetails_flightSummary_flightCode'))
            dcsdetails['dcsdetails_flightsummary_flightdepartureairport'] = type(all_fields.get('body_commonAPIPlus_dcsDetails_flightSummary_flightDepartureAirport'))
            dcsdetails['dcsdetails_flightsummary_flightdeparturedate'] = type(all_fields.get('body_commonAPIPlus_dcsDetails_flightSummary_flightDepartureDate'))
            dcsdetails['dcsdetails_flightsummary_flightdeparturetime'] = type(all_fields.get('body_commonAPIPlus_dcsDetails_flightSummary_flightDepartureTime'))
            dcsdetails['dcsdetails_flightsummary_rawflightcode'] = type(all_fields.get('body_commonAPIPlus_dcsDetails_flightSummary_rawFlightCode'))

            dcsdetails['dcsdetails_dcsdata_dcsrecord_baggagedetail'] = type(all_fields.get(''))
            dcsdetails['dcsdetails_dcsdata_dcsrecord_cabinclass'] = type(all_fields.get(''))
            dcsdetails['dcsdetails_dcsdata_dcsrecord_carryoncount'] = type(all_fields.get(''))
            dcsdetails['dcsdetails_dcsdata_dcsrecord_checkedincount'] = type(all_fields.get(''))
            dcsdetails['dcsdetails_dcsdata_dcsrecord_checkedinweight'] = type(all_fields.get(''))
            dcsdetails['dcsdetails_dcsdata_dcsrecord_checkinagent'] = type(all_fields.get(''))
            dcsdetails['dcsdetails_dcsdata_dcsrecord_checkindatetime'] = type(all_fields.get(''))
            dcsdetails['dcsdetails_dcsdata_dcsrecord_checkinlocation'] = type(all_fields.get(''))
            dcsdetails['dcsdetails_dcsdata_dcsrecord_destination'] = type(all_fields.get(''))
            dcsdetails['dcsdetails_dcsdata_dcsrecord_firstname'] = type(all_fields.get(''))
            dcsdetails['dcsdetails_dcsdata_dcsrecord_frequentflyernumber'] = type(all_fields.get(''))
            dcsdetails['dcsdetails_dcsdata_dcsrecord_passengerseq'] = type(all_fields.get(''))
            dcsdetails['dcsdetails_dcsdata_dcsrecord_pnrlocator'] = type(all_fields.get(''))
            dcsdetails['dcsdetails_dcsdata_dcsrecord_pooledto'] = type(all_fields.get(''))
            dcsdetails['dcsdetails_dcsdata_dcsrecord_seatnumber'] = type(all_fields.get(''))
            dcsdetails['dcsdetails_dcsdata_dcsrecord_securitynumber'] = type(all_fields.get(''))
            dcsdetails['dcsdetails_dcsdata_dcsrecord_sequencenumber'] = type(all_fields.get(''))
            dcsdetails['dcsdetails_dcsdata_dcsrecord_surname'] = type(all_fields.get(''))
            dcsdetails['dcsdetails_dcsdata_dcsrecord_ticketnumber'] = type(all_fields.get(''))
            dcsdetails['dcsdetails_dcsdata_dcsrecord_ticketstatus'] = type(all_fields.get(''))

            dcsdetails['dcsdetails_dcsdata_dcsrecord_traveldocument_traveldocnumber'] = type(all_fields.get(''))
            dcsdetails['dcsdetails_dcsdata_dcsrecord_traveldocument_traveldoctype'] = type(all_fields.get(''))
            dcsdetails['dcsdetails_dcsdata_dcsrecord_traveldocument_traveldoclocofissue'] = type(all_fields.get(''))
            dcsdetails['dcsdetails_dcsdata_dcsrecord_traveldocument_dateofbirth'] = type(all_fields.get(''))
            dcsdetails['dcsdetails_dcsdata_dcsrecord_traveldocument_gender'] = type(all_fields.get(''))
            dcsdetails['dcsdetails_dcsdata_dcsrecord_traveldocument_docissuedate'] = type(all_fields.get(''))
            dcsdetails['dcsdetails_dcsdata_dcsrecord_traveldocument_docexpirationdate'] = type(all_fields.get(''))
            dcsdetails['dcsdetails_dcsdata_dcsrecord_traveldocument_cityofissue'] = type(all_fields.get(''))
            dcsdetails['dcsdetails_dcsdata_dcsrecord_traveldocument_pnrpassengerref'] = type(all_fields.get(''))

            result = apidata.copy()
            result.update(passengerdetails)
            result.update(dcsdetails)
            result.update(pnrdetails)
            result.update(sourcedetails)
            result.update(manifestdetails)
            result.update(flightitinerary_arrivals)
            result.update(flightitinerary_departures)

            result.update({'s3_location': type('s3_file_name not populated')})
            # parsed.
            # parsed/2020-06-12/06:01:00.227909/PARSED_20200610_1820_9999_20200612033510.zip/2020-06-10T18-20-39Z_e160c302-6e1d-3903-ae16-484a1e631192_2cc3e859-b734-3d3b-9de0-36d34fe043b7_Parsed.xml/api.csv
            result.update({'xml_file_name': type(xml_file)})
            result.update({'file_name': type(zip_file)})
            result.update({'extra_rec_type': type('main')})
            #result.update(passengerdetails_documentdetails)

            results = []
            count_docdetails = 0
            files_with_docdetails = 0
            if(expected_docdetails > 0):
                documentdetails = []
                #
                passengerdetails_documentdetails = {}
                passengerdetails_documentdetails['passengerdetails_documentdetails_documenttype'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_documentDetails_0_documentType'))
                passengerdetails_documentdetails['passengerdetails_documentdetails_documentno'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_documentDetails_0_documentNo'))
                passengerdetails_documentdetails['passengerdetails_documentdetails_docissuedate'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_documentDetails_0_docIssueDate'))
                passengerdetails_documentdetails['passengerdetails_documentdetails_docexpirationdate'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_documentDetails_0_docExpirationDate'))
                passengerdetails_documentdetails['passengerdetails_documentdetails_countryofissue'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_documentDetails_0_countryOfIssue'))
                passengerdetails_documentdetails['passengerdetails_documentdetails_cityofissue'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_documentDetails_0_cityOfIssue'))
                documentdetails.append(passengerdetails_documentdetails)
                result.update(documentdetails[0])
                files_with_docdetails += 1
                count_docdetails += 1

                while(count_docdetails<expected_docdetails):

                    doc = {}
                    passengerdetails_documentdetails = {}
                    passengerdetails_documentdetails['passengerdetails_documentdetails_documenttype'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_documentDetails_' + str(count_docdetails) + '_documentType'))
                    passengerdetails_documentdetails['passengerdetails_documentdetails_documentno'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_documentDetails_' + str(count_docdetails) + '_documentNo'))
                    passengerdetails_documentdetails['passengerdetails_documentdetails_docissuedate'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_documentDetails_' + str(count_docdetails) + '_docIssueDate'))
                    passengerdetails_documentdetails['passengerdetails_documentdetails_docexpirationdate'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_documentDetails_' + str(count_docdetails) + '_docExpirationDate'))
                    passengerdetails_documentdetails['passengerdetails_documentdetails_countryofissue'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_documentDetails_' + str(count_docdetails) + '_countryOfIssue'))
                    passengerdetails_documentdetails['passengerdetails_documentdetails_cityofissue'] = type(all_fields.get('body_commonAPIPlus_APIData_passengerDetails_documentDetails_' + str(count_docdetails) + '_cityOfIssue'))
                    documentdetails.append(passengerdetails_documentdetails)

                    doc = passengerdetails_documentdetails
                    doc.update({'manifestdetails_datetimereceived': manifestdetails['manifestdetails_datetimereceived']})
                    doc.update({'s3_location': 's3_file_name not updated'})
                    doc.update({'xml_file_name': xml_file})
                    doc.update({'file_name': zip_file})
                    doc.update({'extra_rec_type': 'documentdetails'})
                    count_docdetails += 1
                    results.append(doc)



            # All docyment details logic.
            # there may be zero or more documentdetail entries
            # add the first one and then generate dummy rows for the rest
            # This needs to be done.  Separate lines for document details.
            # type(all_fields.get('header_sourceFilename').split('/')[-1]
            # type(all_fields.get('header_sourceZipArchive').split('/')[-1]

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


        LOGGER.info("We're done here.")

    except Exception as err:
        error_handler(sys.exc_info()[2].tb_lineno, err)



if __name__ == '__main__':
    main()
