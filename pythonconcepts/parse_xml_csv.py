# pylint: disable=broad-except
""" processes an s3 notification
    downloads a zip file from s3
    converts the xml into a delimited file
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
import xml.dom.minidom
import logging
import csv
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


def error_handler(lineno, error):

    LOGGER.error('The following error has occurred on line: %s', lineno)
    LOGGER.error(str(error))


    raise error

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



def listdir_fullpath(d):
    return [os.path.join(d, f) for f in os.listdir(d)]

def unzip(filename):

    try:
        os.mkdir('/tmp/unzip/')
        zip_ref = zipfile.ZipFile(filename, 'r')
        zip_ref.extractall('/tmp/unzip/')
        zip_ref.close()
        LOGGER.info('Unzipped %s', filename)
        xml_file_list = glob.glob('/tmp/unzip/' + '/**/*.xml', recursive=True)
        LOGGER.info('%s xml files found', len(xml_file_list))
        return xml_file_list
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

def get_tag_value(element, tag_name):

    try:

        if element.getElementsByTagName(tag_name):
            if element.getElementsByTagName(tag_name)[0].firstChild is not None:
                return element.getElementsByTagName(tag_name)[0].firstChild.nodeValue.replace('\n', '')
            else:
                return ''

    except Exception as err:
        error_handler(sys.exc_info()[2].tb_lineno, err)

def process_manifestdetails(document):

    try:
        manifestdetails = {}
        for el_md in document.getElementsByTagName('manifestDetails'):

            manifestdetails['manifestdetails_datatype'] = get_tag_value(el_md, 'dataType')
            manifestdetails['manifestdetails_datetimereceived'] = get_tag_value(el_md, 'datetimeReceived')
            manifestdetails['manifestdetails_manifestguid'] = get_tag_value(el_md, 'manifestGUID')
            manifestdetails['manifestdetails_protocol'] = get_tag_value(el_md, 'protocol')

        LOGGER.debug(manifestdetails)
        return manifestdetails

    except Exception as err:
        error_handler(sys.exc_info()[2].tb_lineno, err)

def process_sourcedata(document):

    try:
        sourcedetails = {}
        for el_sd in document.getElementsByTagName('SourceData'):

            sourcedetails['sourcedata_component'] = get_tag_value(el_sd, 'Component')
            sourcedetails['sourcedata_source'] = get_tag_value(el_sd, 'Source')
            sourcedetails['sourcedata_subject'] = get_tag_value(el_sd, 'Subject')
            sourcedetails['sourcedata_type'] = get_tag_value(el_sd, 'Type')

            for el_sd_id in el_sd.getElementsByTagName('interactiveData'):

                sourcedetails['sourcedata_interactivedata_commonaccessref'] = get_tag_value(el_sd_id, 'commonAccessRef')
                sourcedetails['sourcedata_interactivedata_functionalgrouprefno'] = get_tag_value(el_sd_id, 'functionalGroupRefNo')
                sourcedetails['sourcedata_interactivedata_isinteractive'] = get_tag_value(el_sd_id, 'isInteractive')
                sourcedetails['sourcedata_interactivedata_route'] = get_tag_value(el_sd_id, 'route')
                sourcedetails['sourcedata_interactivedata_senderid'] = get_tag_value(el_sd_id, 'senderId')
                sourcedetails['sourcedata_interactivedata_variant'] = get_tag_value(el_sd_id, 'variant')

        LOGGER.debug(sourcedetails)
        return sourcedetails

    except Exception as err:
        error_handler(sys.exc_info()[2].tb_lineno, err)

def process_pnrdetails(document):
    """ must not store pnrDetails """

    try:
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

        LOGGER.debug(pnrdetails)
        return pnrdetails

    except Exception as err:
        error_handler(sys.exc_info()[2].tb_lineno, err)

def process_passengerdetails(document):

    try:
        passengerdetails = {}

        for el in document.getElementsByTagName('APIData'):

            for el_pd in el.getElementsByTagName('passengerDetails'):

                passengerdetails['passengerdetails_age'] = get_tag_value(el_pd, 'age')
                passengerdetails['passengerdetails_city'] = get_tag_value(el_pd, 'city')
                passengerdetails['passengerdetails_country'] = get_tag_value(el_pd, 'country')
                passengerdetails['passengerdetails_countryofresidence'] = get_tag_value(el_pd, 'countryOfResidence')
                passengerdetails['passengerdetails_dateofbirth'] = get_tag_value(el_pd, 'dateOfBirth')
                passengerdetails['passengerdetails_firstname'] = get_tag_value(el_pd, 'firstName')
                passengerdetails['passengerdetails_gender'] = get_tag_value(el_pd, 'gender')
                passengerdetails['passengerdetails_intransitflag'] = get_tag_value(el_pd, 'inTransitFlag')
                passengerdetails['passengerdetails_lengthofstayinuk'] = get_tag_value(el_pd, 'lengthOfStayInUK')
                passengerdetails['passengerdetails_nationality'] = get_tag_value(el_pd, 'nationality')
                passengerdetails['passengerdetails_officeofclearance'] = get_tag_value(el_pd, 'officeOfClearance')
                passengerdetails['passengerdetails_passengertype'] = get_tag_value(el_pd, 'passengerType')
                passengerdetails['passengerdetails_placeofbirth'] = get_tag_value(el_pd, 'placeOfBirth')
                passengerdetails['passengerdetails_pnrlocator'] = get_tag_value(el_pd, 'pnrLocator')
                passengerdetails['passengerdetails_portofdisembark'] = get_tag_value(el_pd, 'portOfDisembark')
                passengerdetails['passengerdetails_portofembark'] = get_tag_value(el_pd, 'portOfEmbark')
                passengerdetails['passengerdetails_postalcode'] = get_tag_value(el_pd, 'postalCode')
                passengerdetails['passengerdetails_purposeofvisit'] = get_tag_value(el_pd, 'purposeOfVisit')
                passengerdetails['passengerdetails_rankrating'] = get_tag_value(el_pd, 'rankRating')
                passengerdetails['passengerdetails_secondname'] = get_tag_value(el_pd, 'secondName')
                passengerdetails['passengerdetails_state'] = get_tag_value(el_pd, 'state')
                passengerdetails['passengerdetails_street'] = get_tag_value(el_pd, 'street')
                passengerdetails['passengerdetails_surname'] = get_tag_value(el_pd, 'surname')
                passengerdetails['passengerdetails_visaholder'] = get_tag_value(el_pd, 'visaHolder')

                for el_pd_cn in el_pd.getElementsByTagName('contactNumber'):

                    passengerdetails['passengerdetails_contactnumber_phonenumber'] = get_tag_value(el_pd_cn, 'phoneNumber')
                    passengerdetails['passengerdetails_contactnumber_phonenumbertype'] = get_tag_value(el_pd_cn, 'phoneNumberType')

                for el_pd_cr in el_pd.getElementsByTagName('crewAllowance'):

                    passengerdetails['passengerdetails_crewallowance_goodsdetails'] = get_tag_value(el_pd_cr, 'goodsDetails')
                    passengerdetails['passengerdetails_crewallowance_goodstodeclare'] = get_tag_value(el_pd_cr, 'goodsToDeclare')

                for el_pd_ha in el_pd.getElementsByTagName('homeAddress'):

                    passengerdetails['passengerdetails_homeaddress_addressline'] = get_tag_value(el_pd_ha, 'addressLine')
                    passengerdetails['passengerdetails_homeaddress_country'] = get_tag_value(el_pd_ha, 'country')
                    passengerdetails['passengerdetails_homeaddress_postcode'] = get_tag_value(el_pd_ha, 'postCode')

                for el_pd_id in el_pd.getElementsByTagName('interactiveDetail'):

                    passengerdetails['passengerdetails_interactivedetail_knowntravellerno'] = get_tag_value(el_pd_id, 'knownTravellerNo')
                    passengerdetails['passengerdetails_interactivedetail_passengeridentifier'] = get_tag_value(el_pd_id, 'passengerIdentifier')
                    # passengerIdentifier mapped twice in GP code
                    passengerdetails['passengerdetails_passengeridentifier'] = get_tag_value(el_pd_id, 'passengerIdentifier')
                    passengerdetails['passengerdetails_interactivedetail_redressno'] = get_tag_value(el_pd_id, 'redressNo')

                for el_pd_po in el_pd.getElementsByTagName('portOfDisembarkationExtended'):

                    passengerdetails['passengerdetails_portofdisembarkationextended_iatacode'] = get_tag_value(el_pd_po, 'iataCode')
                    passengerdetails['passengerdetails_portofdisembarkationextended_icaocode'] = get_tag_value(el_pd_po, 'icaoCode')
                    passengerdetails['passengerdetails_portofdisembarkationextended_unlocode'] = get_tag_value(el_pd_po, 'unloCode')

                    for el_pd_po_ad in el_pd_po.getElementsByTagName('address'):

                        passengerdetails['passengerdetails_portofdisembarkationextended_address_addressline'] = get_tag_value(el_pd_po_ad, 'addressLine')
                        passengerdetails['passengerdetails_portofdisembarkationextended_address_postcode'] = get_tag_value(el_pd_po_ad, 'postcode')

                    for el_pd_po_co in el_pd_po.getElementsByTagName('coordinates'):

                        passengerdetails['passengerdetails_portofdisembarkationExtended_coordinates_latitude'] = get_tag_value(el_pd_po_co, 'latitude')
                        passengerdetails['passengerdetails_portofdisembarkationExtended_coordinates_longitude'] = get_tag_value(el_pd_po_co, 'longitude')

                for el_pd_vd in el_pd.getElementsByTagName('vehicleDetails'):

                    passengerdetails['passengerdetails_vehicledetails_colour'] = get_tag_value(el_pd_vd, 'colour')
                    passengerdetails['passengerdetails_vehicledetails_make'] = get_tag_value(el_pd_vd, 'make')
                    passengerdetails['passengerdetails_vehicledetails_model'] = get_tag_value(el_pd_vd, 'model')
                    passengerdetails['passengerdetails_vehicledetails_registrationcountry'] = get_tag_value(el_pd_vd, 'registrationCountry')
                    passengerdetails['passengerdetails_vehicledetails_registrationnumber'] = get_tag_value(el_pd_vd, 'registrationNumber')
                    passengerdetails['passengerdetails_vehicledetails_vehicletype'] = get_tag_value(el_pd_vd, 'vehicleType')
                    passengerdetails['passengerdetails_vehicledetails_vin'] = get_tag_value(el_pd_vd, 'vin')
                    passengerdetails['passengerdetails_vehicledetails_year'] = get_tag_value(el_pd_vd, 'year')

        LOGGER.debug(passengerdetails)
        return passengerdetails

    except Exception as err:
        error_handler(sys.exc_info()[2].tb_lineno, err)

def process_passengerdetails_documentdetails(document):

    try:
        documentdetails = []
        for el in document.getElementsByTagName('APIData'):

            for el_pd in el.getElementsByTagName('passengerDetails'):

                for el_pd_dd in el_pd.getElementsByTagName('documentDetails'):

                    passengerdetails_documentdetails = {}
                    passengerdetails_documentdetails['passengerdetails_documentdetails_documenttype'] = get_tag_value(el_pd_dd, 'documentType')
                    passengerdetails_documentdetails['passengerdetails_documentdetails_documentno'] = get_tag_value(el_pd_dd, 'documentNo')
                    passengerdetails_documentdetails['passengerdetails_documentdetails_docissuedate'] = get_tag_value(el_pd_dd, 'docIssueDate')
                    passengerdetails_documentdetails['passengerdetails_documentdetails_docexpirationdate'] = get_tag_value(el_pd_dd, 'docExpirationDate')
                    passengerdetails_documentdetails['passengerdetails_documentdetails_countryofissue'] = get_tag_value(el_pd_dd, 'countryOfIssue')
                    passengerdetails_documentdetails['passengerdetails_documentdetails_cityofissue'] = get_tag_value(el_pd_dd, 'cityOfIssue')

                    documentdetails.append(passengerdetails_documentdetails)

        return documentdetails

    except Exception as err:
        error_handler(sys.exc_info()[2].tb_lineno, err)

def process_dcsdetails(document):

    try:
        dcsdetails = {}
        for el_dcs in document.getElementsByTagName('dcsDetails'):

            for el_dcs_fs in el_dcs.getElementsByTagName('flightSummary'):

                dcsdetails['dcsdetails_flightsummary_airlinecode'] = get_tag_value(el_dcs_fs, 'airlineCode')
                dcsdetails['dcsdetails_flightsummary_flightarrivalairport'] = get_tag_value(el_dcs_fs, 'flightArrivalAirport')
                dcsdetails['dcsdetails_flightsummary_flightarrivaldate'] = get_tag_value(el_dcs_fs, 'flightArrivalDate')
                dcsdetails['dcsdetails_flightsummary_flightarrivaltime'] = get_tag_value(el_dcs_fs, 'flightArrivalTime')
                dcsdetails['dcsdetails_flightsummary_flightcode'] = get_tag_value(el_dcs_fs, 'flightCode')
                dcsdetails['dcsdetails_flightsummary_flightdepartureairport'] = get_tag_value(el_dcs_fs, 'flightDepartureAirport')
                dcsdetails['dcsdetails_flightsummary_flightdeparturedate'] = get_tag_value(el_dcs_fs, 'flightDepartureDate')
                dcsdetails['dcsdetails_flightsummary_flightdeparturetime'] = get_tag_value(el_dcs_fs, 'flightDepartureTime')
                dcsdetails['dcsdetails_flightsummary_rawflightcode'] = get_tag_value(el_dcs_fs, 'rawFlightCode')

            for el_dcs_d in el_dcs.getElementsByTagName('dcsData'):

                for el_dcs_d_dr in el_dcs_d.getElementsByTagName('dcsRecord'):

                    dcsdetails['dcsdetails_dcsdata_dcsrecord_baggagedetail'] = get_tag_value(el_dcs_d_dr, 'baggageDetail')
                    dcsdetails['dcsdetails_dcsdata_dcsrecord_cabinclass'] = get_tag_value(el_dcs_d_dr, 'cabinClass')
                    dcsdetails['dcsdetails_dcsdata_dcsrecord_carryoncount'] = get_tag_value(el_dcs_d_dr, 'carryOnCount')
                    dcsdetails['dcsdetails_dcsdata_dcsrecord_checkedincount'] = get_tag_value(el_dcs_d_dr, 'checkedInCount')
                    dcsdetails['dcsdetails_dcsdata_dcsrecord_checkedinweight'] = get_tag_value(el_dcs_d_dr, 'checkedInWeight')
                    dcsdetails['dcsdetails_dcsdata_dcsrecord_checkinagent'] = get_tag_value(el_dcs_d_dr, 'checkinAgent')
                    dcsdetails['dcsdetails_dcsdata_dcsrecord_checkindatetime'] = get_tag_value(el_dcs_d_dr, 'checkinDateTime')
                    dcsdetails['dcsdetails_dcsdata_dcsrecord_checkinlocation'] = get_tag_value(el_dcs_d_dr, 'checkinLocation')
                    dcsdetails['dcsdetails_dcsdata_dcsrecord_destination'] = get_tag_value(el_dcs_d_dr, 'destination')
                    dcsdetails['dcsdetails_dcsdata_dcsrecord_firstname'] = get_tag_value(el_dcs_d_dr, 'firstname')
                    dcsdetails['dcsdetails_dcsdata_dcsrecord_frequentflyernumber'] = get_tag_value(el_dcs_d_dr, 'frequentFlyerNumber')
                    dcsdetails['dcsdetails_dcsdata_dcsrecord_passengerseq'] = get_tag_value(el_dcs_d_dr, 'passengerSeq')
                    dcsdetails['dcsdetails_dcsdata_dcsrecord_pnrlocator'] = get_tag_value(el_dcs_d_dr, 'pnrLocator')
                    dcsdetails['dcsdetails_dcsdata_dcsrecord_pooledto'] = get_tag_value(el_dcs_d_dr, 'pooledTo')
                    dcsdetails['dcsdetails_dcsdata_dcsrecord_seatnumber'] = get_tag_value(el_dcs_d_dr, 'seatNumber')
                    dcsdetails['dcsdetails_dcsdata_dcsrecord_securitynumber'] = get_tag_value(el_dcs_d_dr, 'securityNumber')
                    dcsdetails['dcsdetails_dcsdata_dcsrecord_sequencenumber'] = get_tag_value(el_dcs_d_dr, 'sequenceNumber')
                    dcsdetails['dcsdetails_dcsdata_dcsrecord_surname'] = get_tag_value(el_dcs_d_dr, 'surname')
                    dcsdetails['dcsdetails_dcsdata_dcsrecord_ticketnumber'] = get_tag_value(el_dcs_d_dr, 'ticketNumber')
                    dcsdetails['dcsdetails_dcsdata_dcsrecord_ticketstatus'] = get_tag_value(el_dcs_d_dr, 'ticketStatus')

                    for el_dcs_d_dr_td in el_dcs_d_dr.getElementsByTagName('travelDocument'):

                        dcsdetails['dcsdetails_dcsdata_dcsrecord_traveldocument_traveldocnumber'] = get_tag_value(el_dcs_d_dr_td, 'travelDocNumber')
                        dcsdetails['dcsdetails_dcsdata_dcsrecord_traveldocument_traveldoctype'] = get_tag_value(el_dcs_d_dr_td, 'travelDocType')
                        dcsdetails['dcsdetails_dcsdata_dcsrecord_traveldocument_traveldoclocofissue'] = get_tag_value(el_dcs_d_dr_td, 'travelDocLocOfIssue')
                        dcsdetails['dcsdetails_dcsdata_dcsrecord_traveldocument_dateofbirth'] = get_tag_value(el_dcs_d_dr_td, 'dateOfBirth')
                        dcsdetails['dcsdetails_dcsdata_dcsrecord_traveldocument_gender'] = get_tag_value(el_dcs_d_dr_td, 'gender')
                        dcsdetails['dcsdetails_dcsdata_dcsrecord_traveldocument_docissuedate'] = get_tag_value(el_dcs_d_dr_td, 'docIssueDate')
                        dcsdetails['dcsdetails_dcsdata_dcsrecord_traveldocument_docexpirationdate'] = get_tag_value(el_dcs_d_dr_td, 'docExpirationDate')
                        dcsdetails['dcsdetails_dcsdata_dcsrecord_traveldocument_cityofissue'] = get_tag_value(el_dcs_d_dr_td, 'cityOfIssue')
                        dcsdetails['dcsdetails_dcsdata_dcsrecord_traveldocument_pnrpassengerref'] = get_tag_value(el_dcs_d_dr_td, 'pnrPassengerRef')

        LOGGER.debug(dcsdetails)
        return dcsdetails

    except Exception as err:
        error_handler(sys.exc_info()[2].tb_lineno, err)

def process_flightitinerary_arrivals(document):

    try:
        flightitinerary_arrivals = {}

        for el_fl in document.getElementsByTagName('flightItinerary'):

            locationfunctioncode = get_tag_value(el_fl, 'locationFunctionCode')
            #arrivals
            if locationfunctioncode == '87':
                flightitinerary_arrivals['flightitinerary_arrival_locationfunctioncode'] = get_tag_value(el_fl, 'locationFunctionCode')
                flightitinerary_arrivals['flightitinerary_arrival_locationnamecode'] = get_tag_value(el_fl, 'locationNameCode')
                flightitinerary_arrivals['flightitinerary_arrivaldatetime'] = get_tag_value(el_fl, 'arrivalDateTime')

                for el_fl_le in el_fl.getElementsByTagName('locationNameExtended'):

                    flightitinerary_arrivals['flightitinerary_arrival_locationnameextended_iatacode'] = get_tag_value(el_fl_le, 'iataCode')
                    flightitinerary_arrivals['flightitinerary_arrival_locationnameextended_icaocode'] = get_tag_value(el_fl_le, 'icaoCode')

        LOGGER.debug(flightitinerary_arrivals)
        return flightitinerary_arrivals

    except Exception as err:
        error_handler(sys.exc_info()[2].tb_lineno, err)

def process_flightitinerary_departures(document):

    try:
        flightitinerary_departures = {}

        for el_fl in document.getElementsByTagName('flightItinerary'):

            locationfunctioncode = get_tag_value(el_fl, 'locationFunctionCode')
            #departures
            if locationfunctioncode == '125':
                flightitinerary_departures['flightitinerary_departure_locationfunctioncode'] = get_tag_value(el_fl, 'locationFunctionCode')
                flightitinerary_departures['flightitinerary_departure_locationnamecode'] = get_tag_value(el_fl, 'locationNameCode')
                flightitinerary_departures['flightitinerary_departuredatetime'] = get_tag_value(el_fl, 'departureDateTime')

                for el_fl_le in el_fl.getElementsByTagName('locationNameExtended'):

                    flightitinerary_departures['flightitinerary_departure_locationnameextended_iatacode'] = get_tag_value(el_fl_le, 'iataCode')
                    flightitinerary_departures['flightitinerary_departure_locationnameextended_icaocode'] = get_tag_value(el_fl_le, 'icaoCode')

        LOGGER.debug(flightitinerary_departures)
        return flightitinerary_departures

    except Exception as err:
        error_handler(sys.exc_info()[2].tb_lineno, err)

def process_apidata(document):

    try:
        apidata = {}
        for el_api in document.getElementsByTagName('APIData'):

            for el_sp in el_api.getElementsByTagName('sendingPartyDetails'):

                apidata['sendingpartydetails_contactid'] = get_tag_value(el_sp, 'contactId')
                apidata['sendingpartydetails_contactname'] = get_tag_value(el_sp, 'contactName')
                apidata['sendingpartydetails_firstcommsaddressid'] = get_tag_value(el_sp, 'firstCommsAddressId')
                # incorrect
                apidata['sendingpartydetails_firstcommsaddresscode'] = get_tag_value(el_sp, 'firstCommsAddressCode')
                apidata['sendingpartydetails_secondcommsaddresscode'] = get_tag_value(el_sp, 'secondCommsAddressCode')
                apidata['sendingpartydetails_secondcommsaddressid'] = get_tag_value(el_sp, 'secondCommsAddressId')

            for el_fd in document.getElementsByTagName('flightDetails'):

                apidata['flightdetails_flightid'] = get_tag_value(el_fd, 'flightId')
                apidata['flightdetails_arrivalairport'] = get_tag_value(el_fd, 'arrivalAirport')
                apidata['flightdetails_arrivaldatetime'] = get_tag_value(el_fd, 'arrivalDateTime')
                apidata['flightdetails_arrivaldatetimeutc'] = get_tag_value(el_fd, 'arrivalDateTimeUTC')
                apidata['flightdetails_cargo'] = get_tag_value(el_fd, 'cargo')
                apidata['flightdetails_carrier'] = get_tag_value(el_fd, 'carrier')
                apidata['flightdetails_carriertype'] = get_tag_value(el_fd, 'carrierType')
                apidata['flightdetails_craftid'] = get_tag_value(el_fd, 'craftId')
                apidata['flightdetails_crewcount'] = get_tag_value(el_fd, 'crewCount')
                apidata['flightdetails_datetimesent'] = get_tag_value(el_fd, 'dateTimeSent')
                apidata['flightdetails_departureairport'] = get_tag_value(el_fd, 'departureAirport')
                apidata['flightdetails_departuredatetime'] = get_tag_value(el_fd, 'departureDateTime')
                apidata['flightdetails_departuredatetimeutc'] = get_tag_value(el_fd, 'departureDateTimeUTC')
                apidata['flightdetails_eventcode'] = get_tag_value(el_fd, 'eventCode')
                apidata['flightdetails_exception'] = get_tag_value(el_fd, 'exception')
                apidata['flightdetails_hireorcharter'] = get_tag_value(el_fd, 'hireOrCharter')
                apidata['flightdetails_hireorcharterdetails'] = get_tag_value(el_fd, 'hireOrCharterDetails')
                apidata['flightdetails_manifesttype'] = get_tag_value(el_fd, 'manifestType')
                apidata['flightdetails_passengercount'] = get_tag_value(el_fd, 'passengerCount')
                apidata['flightdetails_rawflightid'] = get_tag_value(el_fd, 'rawFlightId')
                apidata['flightdetails_route'] = get_tag_value(el_fd, 'route')
                apidata['flightdetails_subsequentport'] = get_tag_value(el_fd, 'subsequentPort')

                for el_fd_oa in el_fd.getElementsByTagName('operatorAddress'):
                    apidata['flightdetails_operatoraddress_addressline'] = get_tag_value(el_fd_oa, 'addressLine')
                    apidata['flightdetails_operatoraddress_country'] = get_tag_value(el_fd_oa, 'country')
                    apidata['flightdetails_operatoraddress_postcode'] = get_tag_value(el_fd_oa, 'postCode')

                for el_fd_on in el_fd.getElementsByTagName('operatorName'):
                    apidata['flightdetails_operatorname_firstname'] = get_tag_value(el_fd_on, 'firstName')
                    apidata['flightdetails_operatorname_middlename'] = get_tag_value(el_fd_on, 'middleName')
                    apidata['flightdetails_operatorname_surname'] = get_tag_value(el_fd_on, 'surname')

                for el_fd_aae in el_fd.getElementsByTagName('arrivalAirportExtended'):

                    apidata['flightdetails_arrivalairportextended_description'] = get_tag_value(el_fd_aae, 'description')
                    apidata['flightdetails_arrivalairportextended_iatacode'] = get_tag_value(el_fd_aae, 'iataCode')
                    apidata['flightdetails_arrivalairportextended_icaocode'] = get_tag_value(el_fd_aae, 'icaoCode')
                    apidata['flightdetails_arrivalairportextended_unlocode'] = get_tag_value(el_fd_aae, 'unloCode')

                    for el_fd_aae_ad in el_fd_aae.getElementsByTagName('Address'):

                        apidata['flightdetails_arrivalairportextended_address_country'] = get_tag_value(el_fd_aae_ad, 'country')
                        apidata['flightdetails_arrivalairportextended_address_addressline'] = get_tag_value(el_fd_aae_ad, 'addressLine')
                        # wrong
                        apidata['flightdetails_arrivalairportextended_address_postcode'] = get_tag_value(el_fd_aae_ad, 'addressLine')

                    for el_fd_aae_co in el_fd_aae.getElementsByTagName('coordinates'):

                        apidata['flightdetails_arrivalairportextended_coordinates_latitude'] = get_tag_value(el_fd_aae_co, 'latitude')
                        apidata['flightdetails_arrivalairportextended_coordinates_longitude'] = get_tag_value(el_fd_aae_co, 'longitude')

                for el_fd_dae in el_fd.getElementsByTagName('departureAirportExtended'):

                    apidata['flightdetails_arrivalairportextended_description'] = get_tag_value(el_fd_dae, 'description')
                    apidata['flightdetails_arrivalairportextended_iatacode'] = get_tag_value(el_fd_dae, 'iataCode')
                    apidata['flightdetails_arrivalairportextended_icaocode'] = get_tag_value(el_fd_dae, 'icaoCode')
                    apidata['flightdetails_arrivalairportextended_unlocode'] = get_tag_value(el_fd_dae, 'unloCode')

                    for el_fd_aae_ad in el_fd_dae.getElementsByTagName('Address'):

                        apidata['flightdetails_arrivalairportextended_address_country'] = get_tag_value(el_fd_aae_ad, 'country')
                        apidata['flightdetails_arrivalairportextended_address_addressline'] = get_tag_value(el_fd_aae_ad, 'addressLine')
                        # wrong
                        apidata['flightdetails_arrivalairportextended_address_postcode'] = get_tag_value(el_fd_aae_ad, 'addressLine')

                    for el_fd_dae_co in el_fd_dae.getElementsByTagName('coordinates'):

                        apidata['flightdetails_arrivalairportextended_coordinates_latitude'] = get_tag_value(el_fd_dae_co, 'latitude')
                        apidata['flightdetails_arrivalairportextended_coordinates_longitude'] = get_tag_value(el_fd_dae_co, 'longitude')

            for el_craft in el_api.getElementsByTagName('craftDetails'):

                apidata['craftdetails_make'] = get_tag_value(el_craft, 'make')
                apidata['craftdetails_model'] = get_tag_value(el_craft, 'model')
                apidata['craftdetails_ownerorganisation'] = get_tag_value(el_craft, 'ownerOrganisation')
                apidata['craftdetails_imonumber'] = get_tag_value(el_craft, 'imoNumber')
                apidata['craftdetails_imodate'] = get_tag_value(el_craft, 'imoDate')
                apidata['craftdetails_mmsinumber'] = get_tag_value(el_craft, 'mmsiNumber')
                apidata['craftdetails_callsign'] = get_tag_value(el_craft, 'callSign')
                apidata['craftdetails_hullcolour'] = get_tag_value(el_craft, 'hullColour')
                apidata['craftdetails_metrelength'] = get_tag_value(el_craft, 'metreLength')
                apidata['craftdetails_registrationno'] = get_tag_value(el_craft, 'registrationNo')
                apidata['craftdetails_registrationcountrycode'] = get_tag_value(el_craft, 'registrationCountryCode')
                apidata['craftdetails_sailmarkings'] = get_tag_value(el_craft, 'sailMarkings')
                apidata['craftdetails_tonnage'] = get_tag_value(el_craft, 'tonnage')
                apidata['craftdetails_transporttype'] = get_tag_value(el_craft, 'transportType')
                apidata['craftdetails_type'] = get_tag_value(el_craft, 'type')
                apidata['craftdetails_vesselname'] = get_tag_value(el_craft, 'vesselName')
                apidata['craftdetails_yearbuilt'] = get_tag_value(el_craft, 'yearBuilt')

                for el_craft_por in el_craft.getElementsByTagName('portOfRegistration'):

                    apidata['craftdetails_portofregistration_type'] = get_tag_value(el_craft_por, 'type')

                    for el_craft_por_loc in el_craft_por.getElementsByTagName('location'):

                        apidata['craftdetails_portofregistration_location_iatacode'] = get_tag_value(el_craft_por_loc, 'iataCode')
                        apidata['craftdetails_portofregistration_location_icaocode'] = get_tag_value(el_craft_por_loc, 'icaoCode')
                        apidata['craftdetails_portofregistration_location_unlocode'] = get_tag_value(el_craft_por_loc, 'unloCode')
                        apidata['craftdetails_portofregistration_location_description'] = get_tag_value(el_craft_por_loc, 'description')

                        for el_craft_por_loc_add in el_craft_por_loc.getElementsByTagName('address'):
                            apidata['craftdetails_portofregistration_location_address_address_line'] = get_tag_value(el_craft_por_loc_add, 'addressLine')
                            apidata['craftdetails_portofregistration_location_address_country'] = get_tag_value(el_craft_por_loc_add, 'country')
                            apidata['craftdetails_portofregistration_location_address_postcode'] = get_tag_value(el_craft_por_loc_add, 'postCode')

                    for el_craft_por_cor in el_craft_por.getElementsByTagName('coordinates'):

                        apidata['craftdetails_portofregistration_coordinates_latitude'] = get_tag_value(el_craft_por_cor, 'latitude')
                        apidata['craftdetails_portofregistration_coordinates_longitude'] = get_tag_value(el_craft_por_cor, 'longitude')

                for el_craft_imp in el_craft.getElementsByTagName('imoRegistryPlace'):

                    for el_craft_imp_loc in el_craft_imp.getElementsByTagName('location'):

                        apidata['craftdetails_imoregistryplace_location_iatacode'] = get_tag_value(el_craft_imp_loc, 'iataCode')
                        apidata['craftdetails_imoregistryplace_location_icaocode'] = get_tag_value(el_craft_imp_loc, 'icaoCode')
                        apidata['craftdetails_imoregistryplace_location_unlocode'] = get_tag_value(el_craft_imp_loc, 'unloCode')
                        apidata['craftdetails_imoregistryplace_location_description'] = get_tag_value(el_craft_imp_loc, 'description')

                        for el_craft_imp_loc_cor in el_craft_imp_loc.getElementsByTagName('coordinates'):

                            apidata['craftdetails_imoregistryplace_location_coordinates_latitude'] = get_tag_value(el_craft_imp_loc_cor, 'latitude')
                            apidata['craftdetails_imoregistryplace_location_coordinates_longitude'] = get_tag_value(el_craft_imp_loc_cor, 'longitude')

                        for el_craft_imp_loc_add in el_craft_imp_loc.getElementsByTagName('addressline'):

                            apidata['craftdetails_imoregistryplace_location_address_addressline'] = get_tag_value(el_craft_imp_loc_add, 'addressline')
                            # wrong
                            apidata['craftdetails_imoregistryplace_location_address_country'] = get_tag_value(el_craft_imp_loc_add, 'addressline')
                            apidata['craftdetails_imoregistryplace_location_address_postcode'] = get_tag_value(el_craft_imp_loc_add, 'postcode')

                for el_craft_imp in el_craft.getElementsByTagName('ownerName'):

                    apidata['craftdetails_ownername_firstname'] = get_tag_value(el_craft_imp, 'firstName')
                    apidata['craftdetails_ownername_middlename'] = get_tag_value(el_craft_imp, 'middleName')
                    apidata['craftdetails_ownername_surname'] = get_tag_value(el_craft_imp, 'surname')

        LOGGER.debug(apidata)
        return apidata

    except Exception as err:
        error_handler(sys.exc_info()[2].tb_lineno, err)

def log_counts(document):
    """ audit counts """

    try:
        documentdetails = len(document.getElementsByTagName('documentDetails'))
        flightitinerary = len(document.getElementsByTagName('flightItinerary'))

        logs = {}
        logs['documentDetails'] = documentdetails
        logs['flightItinerary'] = flightitinerary

        LOGGER.info(logs)

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

# pylint: disable=unused-argument
def main():
    """
    Respond to triggering event by running Athena SQL.

    Args:
        event (dict)           : Data about the triggering event
        context (LamdaContext) : Runtime information

    Returns:
        null
    """


    try:

        downloaded_file = "/Users/sbommireddy/Downloads/PARSED_20200210_0627_9999.zip"
        # Downloaded the following: /tmp/parsed/2020-03-05/09:04:58.888990/PARSED_20200305_0904_9999.zip
        LOGGER.info('Downloaded the following: %s', downloaded_file)

        xml_file_list = unzip(downloaded_file)
        LOGGER.debug(xml_file_list)

        processed_files = 0
        ignored_files = 0
        bad_files = 0
        total_docdetails = 0
        total_files_with_docdetails = 0
        for xml_file in xml_file_list:
            processed_files += 1
            LOGGER.info('Processing file %s of %s: %s', processed_files, len(xml_file_list), xml_file)
            try:
                document = xml.dom.minidom.parse(
                    "{0}".format(xml_file))
            except Exception as err:
                bad_files += 1
                LOGGER.error('The file %s could not be parsed by the XML library. Moving to %s/%s and Exiting with failure.',
                             xml_file, target_bucket_name, failed_to_parse_loc + xml_file.split('/')[-1])
                upload_s3_object(
                    xml_file,
                    target_bucket_name,
                    failed_to_parse_loc + xml_file.split('/')[-1])
                continue

            log_counts(document)

            if document.getElementsByTagName('APIData'):
                apidata = process_apidata(document)
                passengerdetails = process_passengerdetails(document)
                documentdetails = process_passengerdetails_documentdetails(document)
                dcsdata = process_dcsdetails(document)
                prndetails = process_pnrdetails(document)
                sourcedata = process_sourcedata(document)
                manifestdetails = process_manifestdetails(document)
                flightitinerary_arrivals = process_flightitinerary_arrivals(document)
                flightitinerary_departures = process_flightitinerary_departures(document)
                s3_file_name =  xml_file.split('/')[-1] + '/api.csv'

                document.unlink()

                result = apidata.copy()
                result.update(passengerdetails)
                result.update(dcsdata)
                result.update(prndetails)
                result.update(sourcedata)
                result.update(manifestdetails)
                result.update(flightitinerary_arrivals)
                result.update(flightitinerary_departures)
                result.update({'s3_location': s3_file_name})
                result.update({'xml_file_name': xml_file.split('/')[-1]})
                result.update({'file_name': file_name})
                result.update({'extra_rec_type': 'main'})

                # there may be zero or more documentdetail entries
                # add the first one and then generate dummy rows for the rest
                results = []
                count_docdetails = 0
                files_with_docdetails = 0
                if documentdetails:
                    files_with_docdetails += 1
                    count_docdetails += 1
                    result.update(documentdetails[0])
                    for doc in documentdetails[1:]:
                        count_docdetails += 1
                        doc.update({'manifestdetails_datetimereceived': manifestdetails['manifestdetails_datetimereceived']})
                        doc.update({'s3_location': s3_file_name})
                        doc.update({'xml_file_name': xml_file.split('/')[-1]})
                        doc.update({'file_name': file_name})
                        doc.update({'extra_rec_type': 'documentdetails'})
                        results.append(doc)
                results.append(result)

                create_csv(results)
                LOGGER.info('%s record(s) in file %s from %s',
                            recs_in_file('/tmp/api.csv', 'y'),
                            xml_file.split('/')[-1],
                            downloaded_file.split('/')[-1])

                append_local()

                total_docdetails += count_docdetails
                total_files_with_docdetails += files_with_docdetails
                os.remove('/tmp/api.csv')

            else:
                LOGGER.info("No APIData tag found in %s", xml_file.split('/')[-1])
                ignored_files += 1

        written_recs = recs_in_file('/tmp/full.csv', 'y')
        LOGGER.info('%s record(s) in file %s from %s',
                    written_recs,
                    '/tmp/full.csv',
                    downloaded_file.split('/')[-1])
        LOGGER.info('No. files processed: %s', processed_files)
        LOGGER.info('No. bad files: %s', bad_files)
        LOGGER.info('No. files ignored: %s', ignored_files)
        LOGGER.info('No. files with a document details record: %s', total_files_with_docdetails)
        LOGGER.info('No. document details records: %s', total_docdetails)
        balancing_figure = processed_files - bad_files - ignored_files + (total_docdetails - total_files_with_docdetails)
        LOGGER.info('Total files less bad less ignored plus (total doc details less files with a doc detail record): %s', balancing_figure)
        if written_recs != balancing_figure:
            LOGGER.warning('Mismatch between total records written out %s and the checksum figure %s', written_recs, balancing_figure)

        LOGGER.info("We're done here.")
        return event

    except Exception as err:
        error_handler(sys.exc_info()[2].tb_lineno, err)


if __name__== "__main__":
  main()
