#pre_execution_pause_seconds:10
CREATE TABLE api_working_transformed_{instance}
WITH (external_location = '{bucket-name}/{path-name}/',
      format = 'PARQUET',
      parquet_compression = 'SNAPPY')
AS
SELECT
    craftdetails_make,
    craftdetails_model,
    craftdetails_ownerorganisation,
    craftdetails_imoregistryplace_type,
    craftdetails_imonumber,
    craftdetails_imodate,
    craftdetails_mmsinumber,
    craftdetails_callsign,
    craftdetails_hullcolour,
    craftdetails_metrelength,
    craftdetails_portofregistration_type,
    craftdetails_portofregistration_location_iatacode,
    craftdetails_portofregistration_location_icaocode,
    craftdetails_portofregistration_location_coordinates_latitude,
    craftdetails_portofregistration_location_coordinates_longitude,
    craftdetails_imoregistryplace_location_iatacode,
    craftdetails_imoregistryplace_location_icaocode,
    craftdetails_imoregistryplace_location_unlocode,
    craftdetails_imoregistryplace_location_coordinates_latitude,
    craftdetails_imoregistryplace_location_coordinates_longitude,
    craftdetails_imoregistryplace_location_address_addressline,
    craftdetails_imoregistryplace_location_address_postcode,
    craftdetails_imoregistryplace_location_address_country,
    craftdetails_imoregistryplace_location_description,
    craftdetails_ownername_firstname,
    craftdetails_ownername_middlename,
    craftdetails_ownername_surname,
    craftdetails_registrationcountrycode,
    craftdetails_registrationno,
    craftdetails_sailmarkings,
    craftdetails_tonnage,
    craftdetails_portofregistration_location_unlocode,
    craftdetails_transporttype,
    craftdetails_type,
    craftdetails_vesselname,
    craftdetails_yearbuilt,
    craftdetails_portofregistration_location_address_addressline,
    craftdetails_portofregistration_location_address_postcode,
    craftdetails_portofregistration_location_address_country,
    craftdetails_portofregistration_location_description,
    flightdetails_arrivalairport,
    flightdetails_arrivalairportextended_address_addressline,
    flightdetails_arrivalairportextended_address_country,
    flightdetails_arrivalairportextended_address_postcode,
    flightdetails_arrivalairportextended_coordinates_latitude,
    flightdetails_arrivalairportextended_coordinates_longitude,
    flightdetails_arrivalairportextended_description,
    flightdetails_arrivalairportextended_iatacode,
    flightdetails_arrivalairportextended_icaocode,
    flightdetails_arrivalairportextended_unlocode,
    flightdetails_arrivaldatetime,
    flightdetails_arrivaldatetimeutc,
    flightdetails_cargo,
    flightdetails_carrier,
    flightdetails_carriertype,
    flightdetails_craftid,
    flightdetails_crewcount,
    flightdetails_datetimesent,
    flightdetails_departureairport,
    flightdetails_departureairportextended_address_addressline,
    flightdetails_departureairportextended_address_country,
    flightdetails_departureairportextended_address_postcode,
    flightdetails_departureairportextended_coordinates_latitude,
    flightdetails_departureairportextended_coordinates_longitude,
    flightdetails_departureairportextended_description,
    flightdetails_departureairportextended_iatacode,
    flightdetails_departureairportextended_icaocode,
    flightdetails_departureairportextended_unlocode,
    flightdetails_departuredatetime,
    flightdetails_departuredatetimeutc,
    flightdetails_eventcode,
    flightdetails_exception,
    flightdetails_flightid,
    flightdetails_hireorcharter,
    flightdetails_hireorcharterdetails,
    flightdetails_manifesttype,
    flightdetails_operatoraddress_addressline,
    flightdetails_operatoraddress_country,
    flightdetails_operatoraddress_postcode,
    flightdetails_operatorname_firstname,
    flightdetails_operatorname_middlename,
    flightdetails_operatorname_surname,
    flightdetails_passengercount,
    flightdetails_rawflightid,
    flightdetails_route,
    flightdetails_subsequentport,
    flightitinerary_departure_locationnamecode,
    flightitinerary_departure_locationfunctioncode,
    flightitinerary_departuredatetime,
    flightitinerary_departure_locationnameextended_iatacode,
    flightitinerary_departure_locationnameextended_icaocode,
    flightitinerary_arrival_locationnamecode,
    flightitinerary_arrival_locationfunctioncode,
    flightitinerary_arrivaldatetime,
    flightitinerary_arrival_locationnameextended_iatacode,
    flightitinerary_arrival_locationnameextended_icaocode,
    passengerdetails_officeofclearance,
    passengerdetails_passengeridentifier,
    passengerdetails_age,
    passengerdetails_dateofbirth,
    passengerdetails_firstname,
    passengerdetails_secondname,
    passengerdetails_surname,
    passengerdetails_gender,
    passengerdetails_homeaddress_addressline,
    passengerdetails_homeaddress_postcode,
    passengerdetails_homeaddress_country,
    passengerdetails_intransitflag,
    passengerdetails_nationality,
    passengerdetails_countryofresidence,
    passengerdetails_country,
    passengerdetails_postalcode,
    passengerdetails_rankrating,
    passengerdetails_placeofbirth,
    passengerdetails_state,
    passengerdetails_passengertype,
    passengerdetails_pnrlocator,
    passengerdetails_street,
    passengerdetails_city,
    passengerdetails_portofdisembarkationextended_iatacode,
    passengerdetails_portofdisembarkationextended_icaocode,
    passengerdetails_portofdisembarkationextended_unlocode,
    passengerdetails_portofdisembarkationextended_coordinates_lati,
    passengerdetails_portofdisembarkationextended_coordinates_long,
    passengerdetails_portofdisembarkationextended_address_addressl,
    passengerdetails_portofdisembarkationextended_address_postcode,
    passengerdetails_portofdisembarkationextended_address_country,
    passengerdetails_vehicledetails_registrationnumber,
    passengerdetails_vehicledetails_vehicletype,
    passengerdetails_vehicledetails_make,
    passengerdetails_vehicledetails_model,
    passengerdetails_vehicledetails_registrationcountry,
    passengerdetails_vehicledetails_vin,
    passengerdetails_vehicledetails_year,
    passengerdetails_vehicledetails_colour,
    passengerdetails_portofembark,
    passengerdetails_portofdisembark,
    passengerdetails_crewallowance_goodstodeclare,
    passengerdetails_crewallowance_goodsdetail,
    passengerdetails_purposeofvisit,
    passengerdetails_lengthofstayinuk,
    passengerdetails_visaholder,
    passengerdetails_contactnumber_phonenumber,
    passengerdetails_contactnumber_phonenumbertype,
    passengerdetails_interactivedetail_passengeridentifier,
    passengerdetails_interactivedetail_redressno,
    passengerdetails_interactivedetail_knowntravellerno,
    passengerdetails_documentdetails_documenttype,
    passengerdetails_documentdetails_documentno,
    passengerdetails_documentdetails_docissuedate,
    passengerdetails_documentdetails_docexpirationdate,
    passengerdetails_documentdetails_countryofissue,
    passengerdetails_documentdetails_cityofissue,
    sendingpartydetails_contactid,
    sendingpartydetails_contactname,
    sendingpartydetails_firstcommsaddresscode,
    sendingpartydetails_firstcommsaddressid,
    sendingpartydetails_secondcommsaddresscode,
    sendingpartydetails_secondcommsaddressid,
    dcsdetails_flightsummary_airlinecode,
    dcsdetails_flightsummary_flightarrivalairport,
    dcsdetails_flightsummary_flightarrivaldate,
    dcsdetails_flightsummary_flightarrivaltime,
    dcsdetails_flightsummary_flightcode,
    dcsdetails_flightsummary_flightdepartureairport,
    dcsdetails_flightsummary_flightdeparturedate,
    dcsdetails_flightsummary_flightdeparturetime,
    dcsdetails_flightsummary_rawflightcode,
    dcsdetails_dcsdata_dcsrecord_baggagedetail,
    dcsdetails_dcsdata_dcsrecord_cabinclass,
    dcsdetails_dcsdata_dcsrecord_carryoncount,
    dcsdetails_dcsdata_dcsrecord_checkedincount,
    dcsdetails_dcsdata_dcsrecord_checkedinweight,
    dcsdetails_dcsdata_dcsrecord_checkinagent,
    dcsdetails_dcsdata_dcsrecord_checkindatetime,
    dcsdetails_dcsdata_dcsrecord_checkinlocation,
    dcsdetails_dcsdata_dcsrecord_destination,
    dcsdetails_dcsdata_dcsrecord_firstname,
    dcsdetails_dcsdata_dcsrecord_frequentflyernumber,
    dcsdetails_dcsdata_dcsrecord_passengerseq,
    dcsdetails_dcsdata_dcsrecord_pnrlocator,
    dcsdetails_dcsdata_dcsrecord_pooledto,
    dcsdetails_dcsdata_dcsrecord_seatnumber,
    dcsdetails_dcsdata_dcsrecord_securitynumber,
    dcsdetails_dcsdata_dcsrecord_sequencenumber,
    dcsdetails_dcsdata_dcsrecord_surname,
    dcsdetails_dcsdata_dcsrecord_ticketnumber,
    dcsdetails_dcsdata_dcsrecord_ticketstatus,
    dcsdetails_dcsdata_dcsrecord_traveldocument_traveldocnumber,
    dcsdetails_dcsdata_dcsrecord_traveldocument_traveldoctype,
    dcsdetails_dcsdata_dcsrecord_traveldocument_traveldoclocofissue,
    dcsdetails_dcsdata_dcsrecord_traveldocument_dateofbirth,
    dcsdetails_dcsdata_dcsrecord_traveldocument_gender,
    dcsdetails_dcsdata_dcsrecord_traveldocument_docissuedate,
    dcsdetails_dcsdata_dcsrecord_traveldocument_docexpirationdate,
    dcsdetails_dcsdata_dcsrecord_traveldocument_cityofissue,
    dcsdetails_dcsdata_dcsrecord_traveldocument_pnrpassengerref,
    pnrdetails_accompaniedbyinfant,
    pnrdetails_bookingdate,
    pnrdetails_creationdate,
    pnrdetails_masterpnrlocator,
    pnrdetails_modifieddate,
    pnrdetails_pnrlocator,
    pnrdetails_retrieveddate,
    pnrdetails_splitpnr,
    pnrdetails_travelagent,
    pnrdetails_unaccompaniedminor,
    sourcedata_component,
    sourcedata_interactivedata_commonaccessref,
    sourcedata_interactivedata_functionalgrouprefno,
    sourcedata_interactivedata_isinteractive,
    sourcedata_interactivedata_route,
    sourcedata_interactivedata_senderid,
    sourcedata_interactivedata_variant,
    sourcedata_source,
    sourcedata_subject,
    sourcedata_type,
    manifestdetails_datetimereceived,
    manifestdetails_manifestguid,
    manifestdetails_datatype,
    manifestdetails_protocol,
    cf_document_country_of_issue_not_blank_score,
    cf_document_expiration_not_blank_score,
    cf_document_number_not_blank_score,
    cf_document_type_not_blank_score,
    cf_person_dob_not_blank_score,
    cf_person_first_name_not_blank_score,
    cf_person_gender_not_blank_score,
    cf_person_last_name_not_blank_score,
    cf_person_nationality_not_blank_score,
    cf_person_passenger_type_not_blank_score,
    cf_person_second_name_not_blank_score,
    df_document_expiration_in_future_score,
    df_document_issuing_country_refdata_match_score,
    df_document_number_length_score,
    df_document_type_refdata_match_score,
    df_person_dob_not_default_score,
    df_person_dob_in_past_score,
    df_person_first_name_length_score,
    df_person_first_name_not_fnu_score,
    df_person_first_name_not_title_score,
    df_person_gender_refdata_match_score,
    df_person_last_name_length_score,
    df_person_nationality_refdata_match_score,
    df_person_passenger_pax_type_refdat_match_score,
    vf_document_expiration_is_date_score,
    vf_document_issuing_country_length_score,
    vf_document_issuing_country_char_score,
    vf_document_number_length_score,
    vf_document_number_alphanumeric_score,
    vf_person_dob_is_date_score,
    vf_first_name_length_score,
    vf_first_name_alpha_score,
    vf_person_gender_length_score,
    vf_person_gender_char_score,
    vf_last_name_length_score,
    vf_last_name_alpha_score,
    vf_person_nationality_length_score,
    vf_person_nationality_char_score,
    vf_person_passenger_pax_type_length_score,
    vf_person_passenger_pax_type_char_score,
    vf_second_name_length_score,
    vf_second_name_alpha_score,
    tp_passenger_check_in_std_score,
    tp_crew_check_in_std_score,
    tp_passenger_departure_std_score,
    tp_crew_departure_std_score,
    tp_passenger_check_in_atd_score,
    tp_crew_check_in_atd_score,
    tp_passenger_departure_atd_score,
    tp_crew_departure_atd_score,
    tp_passenger_check_in_std_delta,
    tp_crew_check_in_std_delta,
    tp_passenger_departure_std_delta,
    tp_crew_departure_std_delta,
    tp_passenger_check_in_atd_delta,
    tp_crew_check_in_atd_delta,
    tp_passenger_departure_atd_delta,
    tp_crew_departure_atd_delta,
    CASE WHEN voyageid IS NOT NULL AND voyageid != '' THEN voyageid
    ELSE api_voyageid END AS voyageid,
    -- COALESCE(voyageid, api_voyageid) as voyageid,
    std,
    etd,
    atd,
    sta,
    eta,
    ata,
    flight_type,
    pax_flight,
    atd_datetime_utc,
    atd_datetime_local,
    std_datetime_utc,
    std_datetime_local,
    person_iden_id,
    person_doc_id,
    person_id,
    carrier_md_code,
    carrier_type,
    dep_port_md_code,
    dep_port_country_md_code,
    arr_port_md_code,
    arr_port_country_md_code,
    voyage_number,
    voyage_number_trailing,
    api_std_datetime_utc,
    api_sta_datetime_utc,
    person_md_code,
    doc_type_md_code,
    gender_md_code,
    nationality_md_code,
    hub_parsed_message_sqn,
    hub_raw_message_sqn,
    -- override this for SEA vessels.
    CASE
    WHEN voyageid IS NOT NULL AND voyageid != '' AND (carrier_type != 'AIR' AND carrier_type != 'RAIL')
    THEN   TO_HEX(MD5(TO_UTF8(voyageid)))
    WHEN (voyageid IS NULL OR voyageid = '')  AND (carrier_type != 'AIR' AND carrier_type != 'RAIL')
    THEN   TO_HEX(MD5(TO_UTF8(api_voyageid)))
    ELSE hub_voyage_clean_sqn END AS hub_voyage_clean_sqn,
    -- hub_voyage_clean_sqn,
    hub_voyage_raw_sqn,
    hub_person_on_a_voyage_sqn,
    id,
    s3_location,
    xml_file_name,
    file_name,
    df_person_second_name_length_score,
    vf_document_type_length_score,
    vf_document_type_char_score
FROM
(SELECT
    craftdetails_make,
    craftdetails_model,
    craftdetails_ownerorganisation,
    craftdetails_imoregistryplace_type,
    craftdetails_imonumber,
    craftdetails_imodate,
    craftdetails_mmsinumber,
    craftdetails_callsign,
    craftdetails_hullcolour,
    craftdetails_metrelength,
    craftdetails_portofregistration_type,
    craftdetails_portofregistration_location_iatacode,
    craftdetails_portofregistration_location_icaocode,
    craftdetails_portofregistration_location_coordinates_latitude,
    craftdetails_portofregistration_location_coordinates_longitude,
    craftdetails_imoregistryplace_location_iatacode,
    craftdetails_imoregistryplace_location_icaocode,
    craftdetails_imoregistryplace_location_unlocode,
    craftdetails_imoregistryplace_location_coordinates_latitude,
    craftdetails_imoregistryplace_location_coordinates_longitude,
    craftdetails_imoregistryplace_location_address_addressline,
    craftdetails_imoregistryplace_location_address_postcode,
    craftdetails_imoregistryplace_location_address_country,
    craftdetails_imoregistryplace_location_description,
    craftdetails_ownername_firstname,
    craftdetails_ownername_middlename,
    craftdetails_ownername_surname,
    craftdetails_registrationcountrycode,
    craftdetails_registrationno,
    craftdetails_sailmarkings,
    craftdetails_tonnage,
    craftdetails_portofregistration_location_unlocode,
    craftdetails_transporttype,
    craftdetails_type,
    craftdetails_vesselname,
    craftdetails_yearbuilt,
    craftdetails_portofregistration_location_address_addressline,
    craftdetails_portofregistration_location_address_postcode,
    craftdetails_portofregistration_location_address_country,
    craftdetails_portofregistration_location_description,
    flightdetails_arrivalairport,
    flightdetails_arrivalairportextended_address_addressline,
    flightdetails_arrivalairportextended_address_country,
    flightdetails_arrivalairportextended_address_postcode,
    flightdetails_arrivalairportextended_coordinates_latitude,
    flightdetails_arrivalairportextended_coordinates_longitude,
    flightdetails_arrivalairportextended_description,
    flightdetails_arrivalairportextended_iatacode,
    flightdetails_arrivalairportextended_icaocode,
    flightdetails_arrivalairportextended_unlocode,
    flightdetails_arrivaldatetime,
    flightdetails_arrivaldatetimeutc,
    flightdetails_cargo,
    flightdetails_carrier,
    flightdetails_carriertype,
    flightdetails_craftid,
    flightdetails_crewcount,
    flightdetails_datetimesent,
    flightdetails_departureairport,
    flightdetails_departureairportextended_address_addressline,
    flightdetails_departureairportextended_address_country,
    flightdetails_departureairportextended_address_postcode,
    flightdetails_departureairportextended_coordinates_latitude,
    flightdetails_departureairportextended_coordinates_longitude,
    flightdetails_departureairportextended_description,
    flightdetails_departureairportextended_iatacode,
    flightdetails_departureairportextended_icaocode,
    flightdetails_departureairportextended_unlocode,
    flightdetails_departuredatetime,
    flightdetails_departuredatetimeutc,
    flightdetails_eventcode,
    flightdetails_exception,
    flightdetails_flightid,
    flightdetails_hireorcharter,
    flightdetails_hireorcharterdetails,
    flightdetails_manifesttype,
    flightdetails_operatoraddress_addressline,
    flightdetails_operatoraddress_country,
    flightdetails_operatoraddress_postcode,
    flightdetails_operatorname_firstname,
    flightdetails_operatorname_middlename,
    flightdetails_operatorname_surname,
    flightdetails_passengercount,
    flightdetails_rawflightid,
    flightdetails_route,
    flightdetails_subsequentport,
    flightitinerary_departure_locationnamecode,
    flightitinerary_departure_locationfunctioncode,
    flightitinerary_departuredatetime,
    flightitinerary_departure_locationnameextended_iatacode,
    flightitinerary_departure_locationnameextended_icaocode,
    flightitinerary_arrival_locationnamecode,
    flightitinerary_arrival_locationfunctioncode,
    flightitinerary_arrivaldatetime,
    flightitinerary_arrival_locationnameextended_iatacode,
    flightitinerary_arrival_locationnameextended_icaocode,
    passengerdetails_officeofclearance,
    passengerdetails_passengeridentifier,
    passengerdetails_age,
    passengerdetails_dateofbirth,
    passengerdetails_firstname,
    passengerdetails_secondname,
    passengerdetails_surname,
    passengerdetails_gender,
    passengerdetails_homeaddress_addressline,
    passengerdetails_homeaddress_postcode,
    passengerdetails_homeaddress_country,
    passengerdetails_intransitflag,
    passengerdetails_nationality,
    passengerdetails_countryofresidence,
    passengerdetails_country,
    passengerdetails_postalcode,
    passengerdetails_rankrating,
    passengerdetails_placeofbirth,
    passengerdetails_state,
    passengerdetails_passengertype,
    passengerdetails_pnrlocator,
    passengerdetails_street,
    passengerdetails_city,
    passengerdetails_portofdisembarkationextended_iatacode,
    passengerdetails_portofdisembarkationextended_icaocode,
    passengerdetails_portofdisembarkationextended_unlocode,
    passengerdetails_portofdisembarkationextended_coordinates_lati,
    passengerdetails_portofdisembarkationextended_coordinates_long,
    passengerdetails_portofdisembarkationextended_address_addressl,
    passengerdetails_portofdisembarkationextended_address_postcode,
    passengerdetails_portofdisembarkationextended_address_country,
    passengerdetails_vehicledetails_registrationnumber,
    passengerdetails_vehicledetails_vehicletype,
    passengerdetails_vehicledetails_make,
    passengerdetails_vehicledetails_model,
    passengerdetails_vehicledetails_registrationcountry,
    passengerdetails_vehicledetails_vin,
    passengerdetails_vehicledetails_year,
    passengerdetails_vehicledetails_colour,
    passengerdetails_portofembark,
    passengerdetails_portofdisembark,
    passengerdetails_crewallowance_goodstodeclare,
    passengerdetails_crewallowance_goodsdetail,
    passengerdetails_purposeofvisit,
    passengerdetails_lengthofstayinuk,
    passengerdetails_visaholder,
    passengerdetails_contactnumber_phonenumber,
    passengerdetails_contactnumber_phonenumbertype,
    passengerdetails_interactivedetail_passengeridentifier,
    passengerdetails_interactivedetail_redressno,
    passengerdetails_interactivedetail_knowntravellerno,
    passengerdetails_documentdetails_documenttype,
    passengerdetails_documentdetails_documentno,
    passengerdetails_documentdetails_docissuedate,
    passengerdetails_documentdetails_docexpirationdate,
    passengerdetails_documentdetails_countryofissue,
    passengerdetails_documentdetails_cityofissue,
    sendingpartydetails_contactid,
    sendingpartydetails_contactname,
    sendingpartydetails_firstcommsaddresscode,
    sendingpartydetails_firstcommsaddressid,
    sendingpartydetails_secondcommsaddresscode,
    sendingpartydetails_secondcommsaddressid,
    dcsdetails_flightsummary_airlinecode,
    dcsdetails_flightsummary_flightarrivalairport,
    dcsdetails_flightsummary_flightarrivaldate,
    dcsdetails_flightsummary_flightarrivaltime,
    dcsdetails_flightsummary_flightcode,
    dcsdetails_flightsummary_flightdepartureairport,
    dcsdetails_flightsummary_flightdeparturedate,
    dcsdetails_flightsummary_flightdeparturetime,
    dcsdetails_flightsummary_rawflightcode,
    dcsdetails_dcsdata_dcsrecord_baggagedetail,
    dcsdetails_dcsdata_dcsrecord_cabinclass,
    dcsdetails_dcsdata_dcsrecord_carryoncount,
    dcsdetails_dcsdata_dcsrecord_checkedincount,
    dcsdetails_dcsdata_dcsrecord_checkedinweight,
    dcsdetails_dcsdata_dcsrecord_checkinagent,
    dcsdetails_dcsdata_dcsrecord_checkindatetime,
    dcsdetails_dcsdata_dcsrecord_checkinlocation,
    dcsdetails_dcsdata_dcsrecord_destination,
    dcsdetails_dcsdata_dcsrecord_firstname,
    dcsdetails_dcsdata_dcsrecord_frequentflyernumber,
    dcsdetails_dcsdata_dcsrecord_passengerseq,
    dcsdetails_dcsdata_dcsrecord_pnrlocator,
    dcsdetails_dcsdata_dcsrecord_pooledto,
    dcsdetails_dcsdata_dcsrecord_seatnumber,
    dcsdetails_dcsdata_dcsrecord_securitynumber,
    dcsdetails_dcsdata_dcsrecord_sequencenumber,
    dcsdetails_dcsdata_dcsrecord_surname,
    dcsdetails_dcsdata_dcsrecord_ticketnumber,
    dcsdetails_dcsdata_dcsrecord_ticketstatus,
    dcsdetails_dcsdata_dcsrecord_traveldocument_traveldocnumber,
    dcsdetails_dcsdata_dcsrecord_traveldocument_traveldoctype,
    dcsdetails_dcsdata_dcsrecord_traveldocument_traveldoclocofissue,
    dcsdetails_dcsdata_dcsrecord_traveldocument_dateofbirth,
    dcsdetails_dcsdata_dcsrecord_traveldocument_gender,
    dcsdetails_dcsdata_dcsrecord_traveldocument_docissuedate,
    dcsdetails_dcsdata_dcsrecord_traveldocument_docexpirationdate,
    dcsdetails_dcsdata_dcsrecord_traveldocument_cityofissue,
    dcsdetails_dcsdata_dcsrecord_traveldocument_pnrpassengerref,
    pnrdetails_accompaniedbyinfant,
    pnrdetails_bookingdate,
    pnrdetails_creationdate,
    pnrdetails_masterpnrlocator,
    pnrdetails_modifieddate,
    pnrdetails_pnrlocator,
    pnrdetails_retrieveddate,
    pnrdetails_splitpnr,
    pnrdetails_travelagent,
    pnrdetails_unaccompaniedminor,
    sourcedata_component,
    sourcedata_interactivedata_commonaccessref,
    sourcedata_interactivedata_functionalgrouprefno,
    sourcedata_interactivedata_isinteractive,
    sourcedata_interactivedata_route,
    sourcedata_interactivedata_senderid,
    sourcedata_interactivedata_variant,
    sourcedata_source,
    sourcedata_subject,
    sourcedata_type,
    manifestdetails_datetimereceived,
    manifestdetails_manifestguid,
    manifestdetails_datatype,
    manifestdetails_protocol,
    cf_document_country_of_issue_not_blank_score,
    cf_document_expiration_not_blank_score,
    cf_document_number_not_blank_score,
    cf_document_type_not_blank_score,
    cf_person_dob_not_blank_score,
    cf_person_first_name_not_blank_score,
    cf_person_gender_not_blank_score,
    cf_person_last_name_not_blank_score,
    cf_person_nationality_not_blank_score,
    cf_person_passenger_type_not_blank_score,
    cf_person_second_name_not_blank_score,
    df_document_expiration_in_future_score,
    df_document_issuing_country_refdata_match_score,
    df_document_number_length_score,
    df_document_type_refdata_match_score,
    df_person_dob_not_default_score,
    df_person_dob_in_past_score,
    df_person_first_name_length_score,
    df_person_first_name_not_fnu_score,
    df_person_first_name_not_title_score,
    df_person_gender_refdata_match_score,
    df_person_last_name_length_score,
    df_person_nationality_refdata_match_score,
    df_person_passenger_pax_type_refdat_match_score,
    vf_document_expiration_is_date_score,
    vf_document_issuing_country_length_score,
    vf_document_issuing_country_char_score,
    vf_document_number_length_score,
    vf_document_number_alphanumeric_score,
    vf_person_dob_is_date_score,
    vf_first_name_length_score,
    vf_first_name_alpha_score,
    vf_person_gender_length_score,
    vf_person_gender_char_score,
    vf_last_name_length_score,
    vf_last_name_alpha_score,
    vf_person_nationality_length_score,
    vf_person_nationality_char_score,
    vf_person_passenger_pax_type_length_score,
    vf_person_passenger_pax_type_char_score,
    vf_second_name_length_score,
    vf_second_name_alpha_score,
    -- Calculate STD scores using the manifestdetails datetime received so the carrier cannot falsify this, and the api STD information so that it does not matter if ACL/OAG information is available
    CASE
        WHEN api.flightDetails_eventCode = 'CI' AND api.person_md_code = 'P' AND carrier_type = 'AIR'
            THEN
                CASE
                    WHEN DATE_DIFF('SECOND', api.manifestdetails_datetimereceived_utc, api.api_std_datetime_utc) >= (25*60) THEN 1
                    ELSE 0
                END
        WHEN api.flightDetails_eventCode = 'CI' AND api.person_md_code = 'P' AND carrier_type != 'AIR'
              THEN
                  CASE
                      WHEN DATE_DIFF('SECOND', api.manifestdetails_datetimereceived_utc, api.api_std_datetime_utc) >= (15*60)
                      AND  DATE_DIFF('SECOND', api.manifestdetails_datetimereceived_utc, api.api_std_datetime_utc) <= (24*60*60)
                      THEN 1
                      ELSE 0
                END
    END AS tp_passenger_check_in_std_score,
    CASE
        WHEN api.flightDetails_eventCode = 'CI' AND api.person_md_code = 'C' AND carrier_type = 'AIR'
             THEN
                 CASE
                      WHEN DATE_DIFF('SECOND', api.manifestdetails_datetimereceived_utc, api.api_std_datetime_utc) >= (55*60) THEN 1
                      ELSE 0
                END
         WHEN api.flightDetails_eventCode = 'CI' AND api.person_md_code = 'C' AND carrier_type != 'AIR'
              THEN
                  CASE
                        WHEN DATE_DIFF('SECOND', api.manifestdetails_datetimereceived_utc, api.api_std_datetime_utc) >= (45*60)
                        AND  DATE_DIFF('SECOND', api.manifestdetails_datetimereceived_utc, api.api_std_datetime_utc) <= (48*60*60)
                        THEN 1
                        ELSE 0
                  END
    END AS tp_crew_check_in_std_score,
    CASE
        WHEN api.flightDetails_eventCode IN ('DC','DE','NE')
             AND (api.person_md_code = 'P' OR api.flightDetails_manifestType = 'P')
             AND carrier_type = 'AIR'
             THEN
                  CASE
                      WHEN DATE_DIFF('SECOND', api.api_std_datetime_utc, api.manifestdetails_datetimereceived_utc) <= (30*60) THEN 1
                      ELSE 0
                  END
        WHEN api.flightDetails_eventCode IN ('DC','DE','NE')
             AND (api.person_md_code = 'P' OR api.flightDetails_manifestType = 'P')
             AND carrier_type != 'AIR'
             THEN
                  CASE
                      WHEN DATE_DIFF('SECOND', api.api_std_datetime_utc, api.manifestdetails_datetimereceived_utc) <= (30*60) THEN 1
                      ELSE 0
                  END
    END AS tp_passenger_departure_std_score,

    CASE
        WHEN api.flightDetails_eventCode IN ('DC','DE','NE')
        AND (api.person_md_code = 'C' OR api.flightDetails_manifestType = 'C')
        AND carrier_type = 'AIR'
            THEN
                CASE
                    WHEN DATE_DIFF('SECOND', api.api_std_datetime_utc, api.manifestdetails_datetimereceived_utc) <= (30*60) THEN 1
                    ELSE 0
                END
        WHEN api.flightDetails_eventCode IN ('DC','DE','NE')
        AND (api.person_md_code = 'C' OR api.flightDetails_manifestType = 'C')
        AND carrier_type != 'AIR'
            THEN
                CASE
                    WHEN DATE_DIFF('SECOND', api.api_std_datetime_utc, api.manifestdetails_datetimereceived_utc) <= (30*60) THEN 1
                    ELSE 0
                END
    END AS tp_crew_departure_std_score,
    -- ATD scores are calculated dynamically in reporting because ATD information may not be available at scoring time
    CAST(null AS integer) AS tp_passenger_check_in_atd_score,
    CAST(null AS integer) AS tp_crew_check_in_atd_score,
    CAST(null AS integer) AS tp_passenger_departure_atd_score,
    CAST(null AS integer) AS tp_crew_departure_atd_score,
    -- Calculate deltas in seconds
    CASE
        WHEN api.flightDetails_eventCode = 'CI' AND api.person_md_code = 'P' THEN TRY(CAST(DATE_DIFF('SECOND', api.manifestdetails_datetimereceived_utc, api.api_std_datetime_utc) AS integer))
    END AS tp_passenger_check_in_std_delta,
    CASE
        WHEN api.flightDetails_eventCode = 'CI' AND api.person_md_code = 'C' THEN TRY(CAST(DATE_DIFF('SECOND', api.manifestdetails_datetimereceived_utc, api.api_std_datetime_utc) AS integer))
    END AS tp_crew_check_in_std_delta,
    CASE
        WHEN api.flightDetails_eventCode IN ('DC','DE','NE') AND (api.person_md_code = 'P' OR api.flightDetails_manifestType = 'P') THEN TRY(CAST(DATE_DIFF('SECOND', api.api_std_datetime_utc, api.manifestdetails_datetimereceived_utc) AS integer))
    END AS tp_passenger_departure_std_delta,
    CASE
        WHEN api.flightDetails_eventCode IN ('DC','DE','NE') AND (api.person_md_code = 'C' OR api.flightDetails_manifestType = 'C') THEN TRY(CAST(DATE_DIFF('SECOND', api.api_std_datetime_utc, api.manifestdetails_datetimereceived_utc) AS integer))
    END AS tp_crew_departure_std_delta,
    -- ATD deltas are calculated dynamically consistent with scoring
    CAST(null AS integer) AS tp_passenger_check_in_atd_delta,
    CAST(null AS integer) AS tp_crew_check_in_atd_delta,
    CAST(null AS integer) AS tp_passenger_departure_atd_delta,
    CAST(null AS integer) AS tp_crew_departure_atd_delta,
    -- voyageid from CS
    voyageid,
    std,
    etd,
    atd,
    sta,
    eta,
    ata,
    flight_type,
    pax_flight,
    atd_datetime_utc,
    atd_datetime_local,
    std_datetime_utc,
    std_datetime_local,
    person_iden_id,
    person_doc_id,
    person_id,
    carrier_md_code,
    carrier_type,
    dep_port_md_code,
    dep_port_country_md_code,
    arr_port_md_code,
    arr_port_country_md_code,
    voyage_number,
    voyage_number_trailing,
    api_std_datetime_utc,
    api_sta_datetime_utc,
    person_md_code,
    doc_type_md_code,
    gender_md_code,
    nationality_md_code,
    TO_HEX(MD5(TO_UTF8(UPPER(TRIM(xml_file_name))))) AS hub_parsed_message_sqn,
    TO_HEX(MD5(TO_UTF8(UPPER(TRIM(manifestdetails_manifestguid))))) AS hub_raw_message_sqn,
    TO_HEX(MD5(TO_UTF8(UPPER(TRIM(carrier_md_code))||':'||UPPER(TRIM(dep_port_md_code))||':'||UPPER(TRIM(arr_port_md_code))||':'||UPPER(TRIM(voyage_number))||':'||
       COALESCE(UPPER(TRIM(CAST(TRY(CAST(COALESCE(CAST(TRY(DATE_PARSE(api.flightdetails_departureDateTime, '%Y-%m-%d %H:%i:%s')) AS TIMESTAMP),
                                                  std_datetime_local,
                                                  CAST(TRY(DATE_PARSE(api.manifestdetails_datetimereceived, '%Y-%m-%dT%H:%i:%sZ')) AS TIMESTAMP)
                                                  ) AS DATE )) AS VARCHAR(10) ))), '') ))) AS hub_voyage_clean_sqn,
    TO_HEX(MD5(TO_UTF8(UPPER(TRIM(api.flightdetails_flightid))||':'||UPPER(TRIM(api.flightdetails_departureairport))||':'||UPPER(TRIM(api.flightdetails_arrivalairport))||':'||
       COALESCE(UPPER(TRIM(CAST(TRY(CAST(COALESCE(CAST(TRY(DATE_PARSE(api.flightdetails_departureDateTime, '%Y-%m-%d %H:%i:%s')) AS TIMESTAMP),
                                                  std_datetime_local,
                                                  CAST(TRY(DATE_PARSE(api.manifestdetails_datetimereceived, '%Y-%m-%dT%H:%i:%sZ')) AS TIMESTAMP)
                                                  ) AS DATE )) AS VARCHAR(10) ))), '') ))) AS hub_voyage_raw_sqn,
    CASE
	WHEN SUBSTRING(CAST(TRY(DATE_PARSE(api.manifestdetails_datetimereceived, '%Y-%m-%dT%H:%i:%sZ')) AS VARCHAR(30)), 1, 10) >= '2019-04-01' THEN
    		TO_HEX(MD5(TO_UTF8(CASE WHEN person_iden_id <> '' THEN person_iden_id WHEN person_iden_id = '' AND person_doc_id <> ':' THEN person_doc_id END||':'||UPPER(TRIM(carrier_md_code))||':'||UPPER(TRIM(dep_port_md_code))||':'||UPPER(TRIM(arr_port_md_code))||':'||UPPER(TRIM(voyage_number))||':'||
       COALESCE(UPPER(TRIM(CAST(TRY(CAST(COALESCE(CAST(TRY(DATE_PARSE(api.flightdetails_departureDateTime, '%Y-%m-%d %H:%i:%s')) AS TIMESTAMP),
                                                  std_datetime_local,
                                                  CAST(TRY(DATE_PARSE(api.manifestdetails_datetimereceived, '%Y-%m-%dT%H:%i:%sZ')) AS TIMESTAMP)
                                                  ) AS DATE )) AS VARCHAR(10) ))), '') )))
	ELSE
		TO_HEX(MD5(TO_UTF8(CASE WHEN person_iden_id <> '' THEN person_iden_id WHEN person_iden_id = '' AND person_doc_id <> ':' THEN person_doc_id WHEN person_iden_id = '' AND person_doc_id = ':' THEN person_id END||':'||UPPER(TRIM(carrier_md_code))||':'||UPPER(TRIM(dep_port_md_code))||':'||UPPER(TRIM(arr_port_md_code))||':'||UPPER(TRIM(voyage_number))||':'||
       COALESCE(UPPER(TRIM(CAST(TRY(CAST(COALESCE(CAST(TRY(DATE_PARSE(api.flightdetails_departureDateTime, '%Y-%m-%d %H:%i:%s')) AS TIMESTAMP),
                                                  std_datetime_local,
                                                  CAST(TRY(DATE_PARSE(api.manifestdetails_datetimereceived, '%Y-%m-%dT%H:%i:%sZ')) AS TIMESTAMP)
                                                  ) AS DATE )) AS VARCHAR(10) ))), '') )))
	END AS hub_person_on_a_voyage_sqn,
    TO_HEX(MD5(TO_UTF8(UPPER(TRIM(xml_file_name))))) AS id,
    s3_location,
    xml_file_name,
    file_name,
    df_person_second_name_length_score,
    vf_document_type_length_score,
    vf_document_type_char_score,

    CASE
    WHEN carrier_type = 'AIR' OR carrier_type = 'RAIL' THEN
  		(	UPPER(TRIM(dep_port_md_code)) ||
  			UPPER(TRIM(arr_port_md_code)) ||
  			CAST(
  			CASE
  				  WHEN api_inbound_outbound_ind = 'IN' THEN flightdetails_arrivaldatetime_formatted
  				  ELSE flightdetails_departureDateTime_formatted
  			END AS VARCHAR(20)) ||
  			CAST(UPPER(TRIM(carrier_md_code)) AS VARCHAR(5)) ||
  			CAST(voyage_number AS VARCHAR(4)) ||
        CAST(
  			CASE
  				  WHEN api_inbound_outbound_ind = 'IN' THEN 'A'
  				  ELSE 'D'
  			END AS VARCHAR(1))
  		)
      ELSE
      (
        UPPER(TRIM(carrier_md_code)) || '-' ||
        UPPER(TRIM(dep_port_md_code)) || '-' ||
        UPPER(TRIM(arr_port_md_code)) || '-' ||
        api.flightDetails_departureDateTime

      )
  	END as api_voyageid,
  ROW_NUMBER() OVER(PARTITION BY xml_file_name ORDER BY file_name) AS rnum
FROM
(
SELECT
    api.craftDetails_make,
    api.craftDetails_model,
    api.craftDetails_ownerOrganisation,
    api.craftDetails_imoRegistryPlace_type,
    api.craftDetails_imoNumber,
    api.craftDetails_imoDate,
    api.craftDetails_mmsiNumber,
    api.craftDetails_callSign,
    api.craftDetails_hullColour,
    api.craftDetails_metreLength,
    api.craftDetails_portOfRegistration_type,
    api.craftDetails_portOfRegistration_location_iataCode,
    api.craftDetails_portOfRegistration_location_icaoCode,
    api.craftDetails_portOfRegistration_location_coordinates_latitude,
    api.craftDetails_portOfRegistration_location_coordinates_longitude,
    api.craftDetails_imoRegistryPlace_location_iataCode,
    api.craftDetails_imoRegistryPlace_location_icaoCode,
    api.craftDetails_imoRegistryPlace_location_unloCode,
    api.craftDetails_imoRegistryPlace_location_coordinates_latitude,
    api.craftDetails_imoRegistryPlace_location_coordinates_longitude,
        api.craftDetails_imoRegistryPlace_location_address_addressline,
        api.craftDetails_imoRegistryPlace_location_address_postcode,
        api.craftDetails_imoRegistryPlace_location_address_country,
        api.craftDetails_imoRegistryPlace_location_description,
        api.craftDetails_ownerName_firstName,
        api.craftDetails_ownerName_middleName,
        api.craftDetails_ownerName_surname,
        api.craftDetails_registrationCountryCode,
        api.craftDetails_registrationNo,
        api.craftDetails_sailMarkings,
        api.craftDetails_tonnage,
        api.craftDetails_portOfRegistration_location_unloCode,
        api.craftDetails_transportType,
        api.craftDetails_type,
        api.craftDetails_vesselName,
        api.craftDetails_yearBuilt,
        api.craftDetails_portOfRegistration_location_address_addressLine,
        api.craftDetails_portOfRegistration_location_address_postCode,
        api.craftDetails_portOfRegistration_location_address_country,
        api.craftDetails_portOfRegistration_location_description,
        api.flightDetails_arrivalAirport,
        api.flightDetails_arrivalAirportExtended_Address_addressLine,
        api.flightDetails_arrivalAirportExtended_Address_country,
        api.flightDetails_arrivalAirportExtended_Address_postCode,
        api.flightDetails_arrivalAirportExtended_coordinates_latitude,
        api.flightDetails_arrivalAirportExtended_coordinates_longitude,
        api.flightDetails_arrivalAirportExtended_description,
        api.flightDetails_arrivalAirportExtended_iataCode,
        api.flightDetails_arrivalAirportExtended_icaoCode,
        api.flightDetails_arrivalAirportExtended_unloCode,
        api.flightDetails_arrivalDateTime,
        api.flightDetails_arrivalDateTimeUTC,
        api.flightDetails_cargo,
        api.flightDetails_carrier,
        api.flightDetails_carrierType,
        api.flightDetails_craftId,
        api.flightDetails_crewCount,
        api.flightDetails_dateTimeSent,
        api.flightDetails_departureAirport,
        api.flightDetails_departureAirportExtended_Address_addressLine,
        api.flightDetails_departureAirportExtended_Address_country,
        api.flightDetails_departureAirportExtended_Address_postCode,
        api.flightDetails_departureAirportExtended_coordinates_latitude,
        api.flightDetails_departureAirportExtended_coordinates_longitude,
        api.flightDetails_departureAirportExtended_description,
        api.flightDetails_departureAirportExtended_iataCode,
        api.flightDetails_departureAirportExtended_icaoCode,
        api.flightDetails_departureAirportExtended_unloCode,
        api.flightDetails_departureDateTime,
        api.flightDetails_departureDateTimeUTC,
        api.flightDetails_eventCode,
        api.flightDetails_exception,
        api.flightDetails_flightId,
        api.flightDetails_hireOrCharter,
        api.flightDetails_hireOrCharterDetails,
        api.flightDetails_manifestType,
        api.flightDetails_operatorAddress_addressLine,
        api.flightDetails_operatorAddress_country,
        api.flightDetails_operatorAddress_postCode,
        api.flightDetails_operatorName_firstName,
        api.flightDetails_operatorName_middleName,
        api.flightDetails_operatorName_surname,
        api.flightDetails_passengerCount,
        api.flightDetails_rawFlightId,
        api.flightDetails_route,
        api.flightDetails_subsequentPort,
        api.flightItinerary_departure_locationNameCode,
        api.flightItinerary_departure_locationFunctionCode,
        api.flightItinerary_departureDateTime,
        api.flightItinerary_departure_locationNameExtended_iataCode,
        api.flightItinerary_departure_locationNameExtended_icaoCode,
        api.flightItinerary_arrival_locationNameCode,
        api.flightItinerary_arrival_locationFunctionCode,
        api.flightItinerary_arrivalDateTime,
        api.flightItinerary_arrival_locationNameExtended_iataCode,
        api.flightItinerary_arrival_locationNameExtended_icaoCode,
        api.passengerDetails_officeOfClearance,
        api.passengerDetails_passengerIdentifier,
        api.passengerDetails_age,
        api.passengerDetails_dateOfBirth,
        api.passengerDetails_firstName,
        api.passengerDetails_secondName,
        api.passengerDetails_surname,
        api.passengerDetails_gender,
        api.passengerDetails_homeAddress_addressLine,
        api.passengerDetails_homeAddress_postCode,
        api.passengerDetails_homeAddress_country,
        api.passengerDetails_inTransitFlag,
        api.passengerDetails_nationality,
        api.passengerDetails_countryOfResidence,
        api.passengerDetails_country,
        api.passengerDetails_postalCode,
        api.passengerDetails_rankRating,
        api.passengerDetails_placeOfBirth,
        api.passengerDetails_state,
        api.passengerDetails_passengerType,
        api.passengerDetails_pnrLocator,
        api.passengerDetails_street,
        api.passengerDetails_city,
        api.passengerDetails_portOfDisembarkationExtended_iataCode,
        api.passengerDetails_portOfDisembarkationExtended_icaoCode,
        api.passengerDetails_portOfDisembarkationExtended_unloCode,
        api.passengerDetails_portOfDisembarkationExtended_coordinates_lati,
        api.passengerDetails_portOfDisembarkationExtended_coordinates_long,
        api.passengerDetails_portOfDisembarkationExtended_address_addressL,
        api.passengerDetails_portOfDisembarkationExtended_address_postcode,
        api.passengerDetails_portOfDisembarkationExtended_address_country,
        api.passengerDetails_vehicleDetails_registrationNumber,
        api.passengerDetails_vehicleDetails_vehicleType,
        api.passengerDetails_vehicleDetails_make,
        api.passengerDetails_vehicleDetails_model,
        api.passengerDetails_vehicleDetails_registrationCountry,
        api.passengerDetails_vehicleDetails_vin,
        api.passengerDetails_vehicleDetails_year,
        api.passengerDetails_vehicleDetails_colour,
        api.passengerDetails_portOfEmbark,
        api.passengerDetails_portOfDisembark,
        api.passengerDetails_crewAllowance_goodsToDeclare,
        api.passengerDetails_crewAllowance_goodsDetail,
        api.passengerDetails_purposeOfVisit,
        api.passengerDetails_lengthOfStayInUK,
        api.passengerDetails_visaHolder,
        api.passengerDetails_contactNumber_phoneNumber,
        api.passengerDetails_contactNumber_phoneNumberType,
        api.passengerDetails_interactiveDetail_passengerIdentifier,
        api.passengerDetails_interactiveDetail_redressNo,
        api.passengerDetails_interactiveDetail_knownTravellerNo,
        api.passengerDetails_DocumentDetails_documentType,
        api.passengerDetails_DocumentDetails_documentNo,
        api.passengerDetails_DocumentDetails_docIssueDate,
        api.passengerDetails_DocumentDetails_docExpirationDate,
        api.passengerDetails_DocumentDetails_countryOfIssue,
        api.passengerDetails_DocumentDetails_cityOfIssue,
        api.sendingPartyDetails_contactId,
        api.sendingPartyDetails_contactName,
        api.sendingPartyDetails_firstCommsAddressCode,
        api.sendingPartyDetails_firstCommsAddressId,
        api.sendingPartyDetails_secondCommsAddressCode,
        api.sendingPartyDetails_secondCommsAddressId,
        api.dcsDetails_flightSummary_airlineCode,
        api.dcsDetails_flightSummary_flightArrivalAirport,
        api.dcsDetails_flightSummary_flightArrivalDate,
        api.dcsDetails_flightSummary_flightArrivalTime,
        api.dcsDetails_flightSummary_flightCode,
        api.dcsDetails_flightSummary_flightDepartureAirport,
        api.dcsDetails_flightSummary_flightDepartureDate,
        api.dcsDetails_flightSummary_flightDepartureTime,
        api.dcsDetails_flightSummary_rawFlightCode,
        api.dcsDetails_dcsData_dcsRecord_baggageDetail,
        api.dcsDetails_dcsData_dcsRecord_cabinClass,
        api.dcsDetails_dcsData_dcsRecord_carryOnCount,
        api.dcsDetails_dcsData_dcsRecord_checkedInCount,
        api.dcsDetails_dcsData_dcsRecord_checkedInWeight,
        api.dcsDetails_dcsData_dcsRecord_checkinAgent,
        api.dcsDetails_dcsData_dcsRecord_checkinDateTime,
        api.dcsDetails_dcsData_dcsRecord_checkinLocation,
        api.dcsDetails_dcsData_dcsRecord_destination,
        api.dcsDetails_dcsData_dcsRecord_firstname,
        api.dcsDetails_dcsData_dcsRecord_frequentFlyerNumber,
        api.dcsDetails_dcsData_dcsRecord_passengerSeq,
        api.dcsDetails_dcsData_dcsRecord_pnrLocator,
        api.dcsDetails_dcsData_dcsRecord_pooledTo,
        api.dcsDetails_dcsData_dcsRecord_seatNumber,
        api.dcsDetails_dcsData_dcsRecord_securityNumber,
        api.dcsDetails_dcsData_dcsRecord_sequenceNumber,
        api.dcsDetails_dcsData_dcsRecord_surname,
        api.dcsDetails_dcsData_dcsRecord_ticketNumber,
        api.dcsDetails_dcsData_dcsRecord_ticketStatus,
        api.dcsDetails_dcsData_dcsRecord_travelDocument_travelDocNumber,
        api.dcsDetails_dcsData_dcsRecord_travelDocument_travelDocType,
        api.dcsDetails_dcsData_dcsRecord_travelDocument_travelDocLocOfIssue,
        api.dcsDetails_dcsData_dcsRecord_travelDocument_dateOfBirth,
        api.dcsDetails_dcsData_dcsRecord_travelDocument_gender,
        api.dcsDetails_dcsData_dcsRecord_travelDocument_docIssueDate,
        api.dcsDetails_dcsData_dcsRecord_travelDocument_docExpirationDate,
        api.dcsDetails_dcsData_dcsRecord_travelDocument_cityOfIssue,
        api.dcsDetails_dcsData_dcsRecord_travelDocument_pnrPassengerRef,
        api.pnrDetails_accompaniedByInfant,
        api.pnrDetails_bookingDate,
        api.pnrDetails_creationDate,
        api.pnrDetails_masterPNRLocator,
        api.pnrDetails_modifiedDate,
        api.pnrDetails_pnrLocator,
        api.pnrDetails_retrievedDate,
        api.pnrDetails_splitPNR,
        api.pnrDetails_travelAgent,
        api.pnrDetails_unaccompaniedMinor,
        api.SourceData_Component,
        api.SourceData_interactiveData_commonAccessRef,
        api.SourceData_interactiveData_functionalGroupRefNo,
        api.SourceData_interactiveData_isInteractive,
        api.SourceData_interactiveData_route,
        api.SourceData_interactiveData_senderId,
        api.SourceData_interactiveData_variant,
        api.SourceData_Source,
        api.SourceData_Subject,
        api.sourcedata_type,
        api.ManifestDetails_datetimeReceived,
        api.ManifestDetails_manifestGUID,
        api.ManifestDetails_dataType,
        api.ManifestDetails_protocol,
        api.cf_document_country_of_issue_not_blank_score,
        api.cf_Document_expiration_not_blank_score,
        api.cf_document_number_not_blank_score,
        api.cf_document_type_not_blank_score,
        api.cf_person_dob_not_blank_score,
        api.cf_person_first_name_not_blank_score,
        api.cf_person_gender_not_blank_score,
        api.cf_person_last_name_not_blank_score,
        api.cf_person_nationality_not_blank_score,
        api.cf_person_passenger_type_not_blank_score,
        api.cf_person_second_name_not_blank_score,
        api.df_document_expiration_in_future_score,
        api.df_document_issuing_country_refdata_match_score,
        api.df_document_number_length_score,
        api.df_document_type_refdata_match_score,
        api.df_person_dob_not_default_score,
        api.df_person_dob_in_past_score,
        api.df_person_first_name_length_score,
        api.df_person_first_name_not_FNU_score,
        api.df_person_first_name_not_title_score,
        api.df_person_gender_refdata_match_score,
        api.df_person_last_name_length_score,
        api.df_person_nationality_refdata_match_score,
        api.df_person_passenger_pax_type_refdat_match_score,
        api.vf_document_expiration_is_date_score,
        api.vf_document_issuing_country_length_score,
        api.vf_document_issuing_country_char_score,
        api.vf_document_number_length_score,
        api.vf_document_number_alphanumeric_score,
        api.vf_person_dob_is_date_score,
        api.vf_first_name_length_score,
        api.vf_first_name_alpha_score,
        api.vf_person_gender_length_score,
        api.vf_person_gender_char_score,
        api.vf_last_name_length_score,
        api.vf_last_name_alpha_score,
        api.vf_person_nationality_length_score,
        api.vf_person_nationality_char_score,
        api.vf_person_passenger_pax_type_length_score,
        api.vf_person_passenger_pax_type_char_score,
        api.vf_second_name_length_score,
        api.vf_second_name_alpha_score,
        cs.voyageid,
        cs.std,
        cs.etd,
        cs.atd,
        cs.sta,
        cs.eta,
        cs.ata,
        cs.flight_type,
        cs.pax_flight,
        cs.atd_datetime_utc,
        cs.atd_datetime_local,
        cs.std_datetime_utc,
        cs.std_datetime_local,
        COALESCE(carrierICAO.master_carrier_md_code, carrierICAO.carrier_md_code, carrierIATA.master_carrier_md_code) AS parent_carrier_md_code,
        UPPER(TRIM(api.passengerDetails_passengerIdentifier)) AS person_iden_id,
        UPPER(TRIM(api.passengerDetails_DocumentDetails_documentNo))||':'||UPPER(TRIM(api.passengerDetails_DocumentDetails_countryOfIssue)) AS person_doc_id,
        UPPER(TRIM(api.passengerDetails_firstName))||':'||UPPER(TRIM(api.passengerDetails_surname))||':'||UPPER(TRIM(api.passengerDetails_dateOfBirth))||':'||UPPER(TRIM(api.passengerDetails_gender))||':'||UPPER(TRIM(api.passengerDetails_nationality)) AS person_id,
        CASE
            WHEN carrierIATA.master_carrier_md_code IS NULL AND carrierICAO.master_carrier_md_code IS NULL THEN COALESCE(carrierIATA.carrier_md_code, carrierICAO.carrier_md_code)
            ELSE COALESCE(carrierIATA.master_carrier_md_code, carrierICAO.master_carrier_md_code)
        END AS carrier_md_code,
        CASE WHEN carrierICAO.carrier_type IS NOT NULL AND carrierICAO.carrier_type != '' THEN carrierICAO.carrier_type
        ELSE carrierIATA.carrier_type END AS carrier_type,
        -- COALESCE(carrierIATA.carrier_type, carrierICAO.carrier_type) AS carrier_type,
        COALESCE(dep_iata_port.port_md_code,dep_icao_port.port_md_code) AS dep_port_md_code,
        COALESCE(dep_iata_port.country_md_code,dep_icao_port.country_md_code) AS dep_port_country_md_code,
        COALESCE(arr_iata_port.port_md_code,arr_icao_port.port_md_code) AS arr_port_md_code,
        COALESCE(arr_iata_port.country_md_code,arr_icao_port.country_md_code) AS arr_port_country_md_code,
        CASE
            WHEN api.flightId_ga <> '' THEN REPLACE(api.flightid_ga,'_GA','')
            WHEN api.flightid_rm <> '' and regexp_like(SUBSTRING(api.flightid_rm,LENGTH(api.flightid_rm)-9,3),'IMO') THEN
SUBSTRING(api.flightid_rm,LENGTH(api.flightid_rm)-9,11)
            WHEN api.flightid_rm <> '' and regexp_like(SUBSTRING(api.flightid_rm,1,10),'Eurotunnel') THEN
SUBSTRING(api.flightid_rm,LENGTH(api.flightid_rm)-3,4)
            WHEN api.flightid_rm <> '' and regexp_like(SUBSTRING(api.flightid_rm,LENGTH(api.flightid_rm)-8,10),'Undefined') THEN '0000'
            WHEN api.flightid_rm <> '' and regexp_like(api.flightid_rm, '\d{7}') THEN regexp_extract(api.flightid_rm, '\d{7}')
            WHEN api.flightid_rm <> '' THEN SUBSTRING(api.flightid_rm,LENGTH(api.flightid_rm)-10,11)
            WHEN regexp_like(SUBSTRING(api.flightDetails_flightId,LENGTH(api.flightDetails_flightId)-9,3),'IMO') THEN SUBSTRING(api.flightDetails_flightId,LENGTH(api.flightDetails_flightId)-9,11)
            WHEN regexp_like(SUBSTRING(api.flightDetails_flightId,LENGTH(api.flightDetails_flightId)-8,10),'Undefined') THEN '0000'
            WHEN regexp_like(api.flightDetails_flightId, '\d{7}') THEN regexp_extract(api.flightDetails_flightId, '\d{7}')
            WHEN regexp_like(SUBSTRING(api.flightDetails_flightId,3,1), '^[a-zA-Z]+$') THEN LPAD(regexp_replace(SUBSTRING(TRIM(api.flightDetails_flightId),4,4),'[^0-9]'),4,'0')
            ELSE LPAD(regexp_replace(SUBSTRING(TRIM(api.flightDetails_flightId),3,4),'[^0-9]'),4,'0')
        END AS voyage_number,
        CASE
            WHEN api.flightId_ga <> '' THEN ''
            WHEN api.flightid_rm <> '' THEN ''
            WHEN regexp_like(SUBSTRING(TRIM(api.flightDetails_flightId),LENGTH(TRIM(api.flightDetails_flightId)),1), '^[a-zA-Z]+$') THEN SUBSTRING(TRIM(api.flightDetails_flightId),LENGTH(TRIM(api.flightDetails_flightId)),1)
        END AS voyage_number_trailing,
        CAST(TRY(AT_TIMEZONE(TRY(CAST(api.flightDetails_departureDateTime||COALESCE(dep_iata_port.port_tz,dep_icao_port.port_tz) AS TIMESTAMP)),'UTC')) AS TIMESTAMP) AS api_std_datetime_utc,
        CAST(TRY(AT_TIMEZONE(TRY(CAST(api.flightDetails_arrivalDateTime||COALESCE(arr_iata_port.port_tz,arr_icao_port.port_tz) AS TIMESTAMP)),'UTC')) AS TIMESTAMP) AS api_sta_datetime_utc,
        CAST(TRY(DATE_PARSE(api.manifestdetails_datetimereceived, '%Y-%m-%dT%H:%i:%sZ')) AS TIMESTAMP) AS manifestdetails_datetimereceived_utc,
        api.person_md_code,
        api.doc_type_md_code,
        api.gender_md_code,
        api.nationality_md_code,
        api.s3_location,
        api.xml_file_name,
        api.file_name,
        api.df_person_second_name_length_score,
        api.vf_document_type_length_score,
        api.vf_document_type_char_score,
		/* Additional flags for VoyageId from API feed to help with coalesce if not found in airport schedule dataset */

		CAST(date_format(CAST(flightdetails_arrivaldatetime AS TIMESTAMP) , '%Y%m%d') AS CHAR(8)) as flightdetails_arrivaldatetime_formatted,
		CAST(date_format(CAST(flightDetails_departureDateTime AS TIMESTAMP) , '%Y%m%d') AS CHAR(8)) as flightDetails_departureDateTime_formatted,
		CASE
			WHEN COALESCE(dep_iata_port.country_md_code, dep_icao_port.country_md_code) = 'GBR' AND COALESCE(arr_iata_port.country_md_code, arr_icao_port.country_md_code) = 'GBR' THEN 'DOM'
			WHEN COALESCE(dep_iata_port.country_md_code, dep_icao_port.country_md_code) = 'GBR' AND COALESCE(arr_iata_port.country_md_code, arr_icao_port.country_md_code) != 'GBR' THEN 'OUT'
			WHEN COALESCE(dep_iata_port.country_md_code, dep_icao_port.country_md_code) != 'GBR' AND COALESCE(arr_iata_port.country_md_code, arr_icao_port.country_md_code) = 'GBR' THEN 'IN'
			WHEN COALESCE(dep_iata_port.country_md_code, dep_icao_port.country_md_code) != 'GBR' AND COALESCE(arr_iata_port.country_md_code, arr_icao_port.country_md_code) != 'GBR' THEN 'FOR'
		END AS api_inbound_outbound_ind

    FROM
        (
        SELECT
            api.craftDetails_make,
            api.craftDetails_model,
            api.craftDetails_ownerOrganisation,
            api.craftDetails_imoRegistryPlace_type,
            api.craftDetails_imoNumber,
            api.craftDetails_imoDate,
            api.craftDetails_mmsiNumber,
            api.craftDetails_callSign,
            api.craftDetails_hullColour,
            api.craftDetails_metreLength,
            api.craftDetails_portOfRegistration_type,
            api.craftDetails_portOfRegistration_location_iataCode,
            api.craftDetails_portOfRegistration_location_icaoCode,
            api.craftDetails_portOfRegistration_location_coordinates_latitude,
            api.craftDetails_portOfRegistration_location_coordinates_longitude,
            api.craftDetails_imoRegistryPlace_location_iataCode,
            api.craftDetails_imoRegistryPlace_location_icaoCode,
            api.craftDetails_imoRegistryPlace_location_unloCode,
            api.craftDetails_imoRegistryPlace_location_coordinates_latitude,
            api.craftDetails_imoRegistryPlace_location_coordinates_longitude,
            api.craftDetails_imoRegistryPlace_location_address_addressline,
            api.craftDetails_imoRegistryPlace_location_address_postcode,
            api.craftDetails_imoRegistryPlace_location_address_country,
            api.craftDetails_imoRegistryPlace_location_description,
            api.craftDetails_ownerName_firstName,
            api.craftDetails_ownerName_middleName,
            api.craftDetails_ownerName_surname,
            api.craftDetails_registrationCountryCode,
            api.craftDetails_registrationNo,
            api.craftDetails_sailMarkings,
            api.craftDetails_tonnage,
            api.craftDetails_portOfRegistration_location_unloCode,
            api.craftDetails_transportType,
            api.craftDetails_type,
            api.craftDetails_vesselName,
            api.craftDetails_yearBuilt,
            api.craftDetails_portOfRegistration_location_address_addressLine,
            api.craftDetails_portOfRegistration_location_address_postCode,
            api.craftDetails_portOfRegistration_location_address_country,
            api.craftDetails_portOfRegistration_location_description,
            api.flightDetails_arrivalAirport,
            api.flightDetails_arrivalAirportExtended_Address_addressLine,
            api.flightDetails_arrivalAirportExtended_Address_country,
            api.flightDetails_arrivalAirportExtended_Address_postCode,
            api.flightDetails_arrivalAirportExtended_coordinates_latitude,
            api.flightDetails_arrivalAirportExtended_coordinates_longitude,
            api.flightDetails_arrivalAirportExtended_description,
            api.flightDetails_arrivalAirportExtended_iataCode,
            api.flightDetails_arrivalAirportExtended_icaoCode,
            api.flightDetails_arrivalAirportExtended_unloCode,
            api.flightDetails_arrivalDateTime,
            api.flightDetails_arrivalDateTimeUTC,
            api.flightDetails_cargo,
            api.flightDetails_carrier,
            api.flightDetails_carrierType,
            api.flightDetails_craftId,
            api.flightDetails_crewCount,
            api.flightDetails_dateTimeSent,
            api.flightDetails_departureAirport,
            api.flightDetails_departureAirportExtended_Address_addressLine,
            api.flightDetails_departureAirportExtended_Address_country,
            api.flightDetails_departureAirportExtended_Address_postCode,
            api.flightDetails_departureAirportExtended_coordinates_latitude,
            api.flightDetails_departureAirportExtended_coordinates_longitude,
            api.flightDetails_departureAirportExtended_description,
            api.flightDetails_departureAirportExtended_iataCode,
            api.flightDetails_departureAirportExtended_icaoCode,
            api.flightDetails_departureAirportExtended_unloCode,
            api.flightDetails_departureDateTime,
            api.flightDetails_departureDateTimeUTC,
            api.flightDetails_eventCode,
            api.flightDetails_exception,
            api.flightDetails_flightId,
            api.flightDetails_hireOrCharter,
            api.flightDetails_hireOrCharterDetails,
            api.flightDetails_manifestType,
            api.flightDetails_operatorAddress_addressLine,
            api.flightDetails_operatorAddress_country,
            api.flightDetails_operatorAddress_postCode,
            api.flightDetails_operatorName_firstName,
            api.flightDetails_operatorName_middleName,
            api.flightDetails_operatorName_surname,
            api.flightDetails_passengerCount,
            api.flightDetails_rawFlightId,
            api.flightDetails_route,
            api.flightDetails_subsequentPort,
            api.flightItinerary_departure_locationNameCode,
            api.flightItinerary_departure_locationFunctionCode,
            api.flightItinerary_departureDateTime,
            api.flightItinerary_departure_locationNameExtended_iataCode,
            api.flightItinerary_departure_locationNameExtended_icaoCode,
            api.flightItinerary_arrival_locationNameCode,
            api.flightItinerary_arrival_locationFunctionCode,
            api.flightItinerary_arrivalDateTime,
            api.flightItinerary_arrival_locationNameExtended_iataCode,
            api.flightItinerary_arrival_locationNameExtended_icaoCode,
            api.passengerDetails_officeOfClearance,
            api.passengerDetails_passengerIdentifier,
            api.passengerDetails_age,
            api.passengerDetails_dateOfBirth,
            api.passengerDetails_firstName,
            api.passengerDetails_secondName,
            api.passengerDetails_surname,
            api.passengerDetails_gender,
            api.passengerDetails_homeAddress_addressLine,
            api.passengerDetails_homeAddress_postCode,
            api.passengerDetails_homeAddress_country,
            api.passengerDetails_inTransitFlag,
            api.passengerDetails_nationality,
            api.passengerDetails_countryOfResidence,
            api.passengerDetails_country,
            api.passengerDetails_postalCode,
            api.passengerDetails_rankRating,
            api.passengerDetails_placeOfBirth,
            api.passengerDetails_state,
            api.passengerDetails_passengerType,
            api.passengerDetails_pnrLocator,
            api.passengerDetails_street,
            api.passengerDetails_city,
            api.passengerDetails_portOfDisembarkationExtended_iataCode,
            api.passengerDetails_portOfDisembarkationExtended_icaoCode,
            api.passengerDetails_portOfDisembarkationExtended_unloCode,
            api.passengerDetails_portOfDisembarkationExtended_coordinates_lati,
            api.passengerDetails_portOfDisembarkationExtended_coordinates_long,
            api.passengerDetails_portOfDisembarkationExtended_address_addressL,
            api.passengerDetails_portOfDisembarkationExtended_address_postcode,
            api.passengerDetails_portOfDisembarkationExtended_address_country,
            api.passengerDetails_vehicleDetails_registrationNumber,
            api.passengerDetails_vehicleDetails_vehicleType,
            api.passengerDetails_vehicleDetails_make,
            api.passengerDetails_vehicleDetails_model,
            api.passengerDetails_vehicleDetails_registrationCountry,
            api.passengerDetails_vehicleDetails_vin,
            api.passengerDetails_vehicleDetails_year,
            api.passengerDetails_vehicleDetails_colour,
            api.passengerDetails_portOfEmbark,
            api.passengerDetails_portOfDisembark,
            api.passengerDetails_crewAllowance_goodsToDeclare,
            api.passengerDetails_crewAllowance_goodsDetail,
            api.passengerDetails_purposeOfVisit,
            api.passengerDetails_lengthOfStayInUK,
            api.passengerDetails_visaHolder,
            api.passengerDetails_contactNumber_phoneNumber,
            api.passengerDetails_contactNumber_phoneNumberType,
            api.passengerDetails_interactiveDetail_passengerIdentifier,
            api.passengerDetails_interactiveDetail_redressNo,
            api.passengerDetails_interactiveDetail_knownTravellerNo,
            apidoc.passengerDetails_DocumentDetails_documentType,
            apidoc.passengerDetails_DocumentDetails_documentNo,
            apidoc.passengerDetails_DocumentDetails_docIssueDate,
            apidoc.passengerDetails_DocumentDetails_docExpirationDate,
            apidoc.passengerDetails_DocumentDetails_countryOfIssue,
            apidoc.passengerDetails_DocumentDetails_cityOfIssue,
            api.sendingPartyDetails_contactId,
            api.sendingPartyDetails_contactName,
            api.sendingPartyDetails_firstCommsAddressCode,
            api.sendingPartyDetails_firstCommsAddressId,
            api.sendingPartyDetails_secondCommsAddressCode,
            api.sendingPartyDetails_secondCommsAddressId,
            api.dcsDetails_flightSummary_airlineCode,
            api.dcsDetails_flightSummary_flightArrivalAirport,
            api.dcsDetails_flightSummary_flightArrivalDate,
            api.dcsDetails_flightSummary_flightArrivalTime,
            api.dcsDetails_flightSummary_flightCode,
            api.dcsDetails_flightSummary_flightDepartureAirport,
            api.dcsDetails_flightSummary_flightDepartureDate,
            api.dcsDetails_flightSummary_flightDepartureTime,
            api.dcsDetails_flightSummary_rawFlightCode,
            api.dcsDetails_dcsData_dcsRecord_baggageDetail,
            api.dcsDetails_dcsData_dcsRecord_cabinClass,
            api.dcsDetails_dcsData_dcsRecord_carryOnCount,
            api.dcsDetails_dcsData_dcsRecord_checkedInCount,
            api.dcsDetails_dcsData_dcsRecord_checkedInWeight,
            api.dcsDetails_dcsData_dcsRecord_checkinAgent,
            api.dcsDetails_dcsData_dcsRecord_checkinDateTime,
            api.dcsDetails_dcsData_dcsRecord_checkinLocation,
            api.dcsDetails_dcsData_dcsRecord_destination,
            api.dcsDetails_dcsData_dcsRecord_firstname,
            api.dcsDetails_dcsData_dcsRecord_frequentFlyerNumber,
            api.dcsDetails_dcsData_dcsRecord_passengerSeq,
            api.dcsDetails_dcsData_dcsRecord_pnrLocator,
            api.dcsDetails_dcsData_dcsRecord_pooledTo,
            api.dcsDetails_dcsData_dcsRecord_seatNumber,
            api.dcsDetails_dcsData_dcsRecord_securityNumber,
            api.dcsDetails_dcsData_dcsRecord_sequenceNumber,
            api.dcsDetails_dcsData_dcsRecord_surname,
            api.dcsDetails_dcsData_dcsRecord_ticketNumber,
            api.dcsDetails_dcsData_dcsRecord_ticketStatus,
            api.dcsDetails_dcsData_dcsRecord_travelDocument_travelDocNumber,
            api.dcsDetails_dcsData_dcsRecord_travelDocument_travelDocType,
            api.dcsDetails_dcsData_dcsRecord_travelDocument_travelDocLocOfIssue,
            api.dcsDetails_dcsData_dcsRecord_travelDocument_dateOfBirth,
            api.dcsDetails_dcsData_dcsRecord_travelDocument_gender,
            api.dcsDetails_dcsData_dcsRecord_travelDocument_docIssueDate,
            api.dcsDetails_dcsData_dcsRecord_travelDocument_docExpirationDate,
            api.dcsDetails_dcsData_dcsRecord_travelDocument_cityOfIssue,
            api.dcsDetails_dcsData_dcsRecord_travelDocument_pnrPassengerRef,
            api.pnrDetails_accompaniedByInfant,
            api.pnrDetails_bookingDate,
            api.pnrDetails_creationDate,
            api.pnrDetails_masterPNRLocator,
            api.pnrDetails_modifiedDate,
            api.pnrDetails_pnrLocator,
            api.pnrDetails_retrievedDate,
            api.pnrDetails_splitPNR,
            api.pnrDetails_travelAgent,
            api.pnrDetails_unaccompaniedMinor,
            api.SourceData_Component,
            api.SourceData_interactiveData_commonAccessRef,
            api.SourceData_interactiveData_functionalGroupRefNo,
            api.SourceData_interactiveData_isInteractive,
            api.SourceData_interactiveData_route,
            api.SourceData_interactiveData_senderId,
            api.SourceData_interactiveData_variant,
            api.SourceData_Source,
            api.SourceData_Subject,
            api.sourcedata_type,
            api.ManifestDetails_datetimeReceived,
            api.ManifestDetails_manifestGUID,
            api.ManifestDetails_dataType,
            api.ManifestDetails_protocol,
            CASE
              WHEN  (pt.person_md_code = 'C' OR pt.person_md_code = 'P') THEN pt.person_md_code
              WHEN  (api.flightDetails_Manifesttype = 'C' OR api.flightDetails_Manifesttype = 'P') THEN api.flightDetails_Manifesttype
              ELSE COALESCE(pt.person_md_code, api.flightDetails_manifestType)
            END AS person_md_code,
            apidoc.doc_type_md_code,
            gn.md_code AS gender_md_code,
            nt.code AS nationality_md_code,
            --Field Level Completeness - CF
            apidoc.cf_document_country_of_issue_not_blank_score,
            apidoc.cf_Document_expiration_not_blank_score,
            apidoc.cf_document_number_not_blank_score,
            apidoc.cf_document_type_not_blank_score,
            CASE
                WHEN api.passengerDetails_dateOfBirth IS NOT NULL AND api.passengerDetails_dateOfBirth <> '' THEN 1
                ELSE 0
            END AS cf_person_dob_not_blank_score,
            CASE
                WHEN api.passengerDetails_firstName IS NOT NULL AND api.passengerDetails_firstName <> '' THEN 1
                ELSE 0
            END AS cf_person_first_name_not_blank_score,
            CASE
                WHEN api.passengerDetails_gender IS NOT NULL AND api.passengerDetails_gender <> '' THEN 1
                ELSE 0
            END AS cf_person_gender_not_blank_score,
            CASE
                WHEN api.passengerDetails_surname IS NOT NULL AND api.passengerDetails_surname <> '' THEN 1
                ELSE 0
            END AS cf_person_last_name_not_blank_score,
            CASE
                WHEN api.passengerDetails_nationality IS NOT NULL AND api.passengerDetails_nationality <> '' THEN 1
                ELSE 0
            END AS cf_person_nationality_not_blank_score,
            CASE
                WHEN api.passengerDetails_passengerType IS NOT NULL AND api.passengerDetails_passengerType <> '' THEN 1
                ELSE 0
            END AS cf_person_passenger_type_not_blank_score,
            CASE
                WHEN api.passengerDetails_secondName IS NOT NULL AND api.passengerDetails_secondName <> '' THEN 1
                ELSE 0
            END AS cf_person_second_name_not_blank_score,
            --Field Level Definition - DF
            apidoc.df_document_expiration_in_future_score,
            apidoc.df_document_issuing_country_refdata_match_score,
            apidoc.df_document_number_length_score,
            apidoc.df_document_type_refdata_match_score,
            CASE
                WHEN (api.passengerDetails_dateOfBirth IS NULL OR api.passengerDetails_dateOfBirth = '') OR
                      NOT regexp_like(api.passengerDetails_dateOfBirth, '^((((19[0-9][0-9])|(2[0-9][0-9][0-9]))([-])(0[13578]|10|12)([-])(0[1-9]|[12][0-9]|3[01]))|(((19[0-9][0-9])|(2[0-9][0-9][0-9]))([-])(0[469]|11)([-])([0][1-9]|[12][0-9]|30))|(((19[0-9][0-9])|(2[0-9][0-9][0-9]))([-])(02)([-])(0[1-9]|1[0-9]|2[0-8]))|(([02468][048]00)([-])(02)([-])(29))|(([13579][26]00)([-])(02)([-])(29))|(([0-9][0-9][0][48])([-])(02)([-])(29))|(([0-9][0-9][2468][048])([-])(02)([-])(29))|(([0-9][0-9][13579][26])([-])(02)([-])(29)))$') OR
                     CAST(api.passengerDetails_dateOfBirth AS VARCHAR(10)) > '1900-01-01' THEN 1
                ELSE 0
            END AS df_person_dob_not_default_score,
            CASE
                WHEN (api.passengerDetails_dateOfBirth IS NULL OR api.passengerDetails_dateOfBirth = '') OR
                     NOT regexp_like(api.passengerDetails_dateOfBirth, '^((((19[0-9][0-9])|(2[0-9][0-9][0-9]))([-])(0[13578]|10|12)([-])(0[1-9]|[12][0-9]|3[01]))|(((19[0-9][0-9])|(2[0-9][0-9][0-9]))([-])(0[469]|11)([-])([0][1-9]|[12][0-9]|30))|(((19[0-9][0-9])|(2[0-9][0-9][0-9]))([-])(02)([-])(0[1-9]|1[0-9]|2[0-8]))|(([02468][048]00)([-])(02)([-])(29))|(([13579][26]00)([-])(02)([-])(29))|(([0-9][0-9][0][48])([-])(02)([-])(29))|(([0-9][0-9][2468][048])([-])(02)([-])(29))|(([0-9][0-9][13579][26])([-])(02)([-])(29)))$') OR
                     CAST(api.passengerDetails_dateOfBirth AS VARCHAR(10)) <= CAST(TRY(DATE_FORMAT(TRY(DATE_PARSE(api.manifestdetails_datetimereceived, '%Y-%m-%dT%H:%i:%sZ')), '%Y-%m-%d')) AS VARCHAR(10)) THEN 1
                ELSE 0
            END AS df_person_dob_in_past_score,
            CASE
                WHEN (api.passengerDetails_firstName IS NULL OR api.passengerDetails_firstName = '') OR
                      LENGTH(api.passengerDetails_firstName) > 1 THEN 1
                ELSE 0
            END AS df_person_first_name_length_score,
            CASE
                WHEN api.passengerDetails_firstName <> 'FNU' THEN 1
                ELSE 0
            END AS df_person_first_name_not_FNU_score,
            CASE
                WHEN sal.md_title IS NULL THEN 1
                ELSE 0
            END AS df_person_first_name_not_title_score,
            CASE
                WHEN (api.passengerDetails_gender IS NULL OR api.passengerDetails_gender = '') OR
                      gn.md_code IS NOT NULL THEN 1
                ELSE 0
            END AS df_person_gender_refdata_match_score,
            CASE
                WHEN (api.passengerDetails_surname IS NULL OR api.passengerDetails_surname = '') OR
                      LENGTH(api.passengerDetails_surname) > 1 THEN 1
                ELSE 0
            END AS df_person_last_name_length_score,
            CASE
                WHEN (api.passengerDetails_nationality IS NULL OR api.passengerDetails_nationality = '') OR
                      nt.code IS NOT NULL THEN 1
                ELSE 0
            END AS df_person_nationality_refdata_match_score,
            CASE
                WHEN (api.passengerDetails_passengerType IS NULL OR api.passengerDetails_passengerType = '') OR
                      pt.code IS NOT NULL THEN 1
                ELSE 0
            END AS df_person_passenger_pax_type_refdat_match_score,
            --Field Level Validity - VF
            apidoc.vf_document_expiration_is_date_score,
            apidoc.vf_document_issuing_country_length_score,
            apidoc.vf_document_issuing_country_char_score,
            apidoc.vf_document_number_length_score,
            apidoc.vf_document_number_alphanumeric_score,
            CASE
                WHEN (api.passengerDetails_dateOfBirth IS NULL OR api.passengerDetails_dateOfBirth = '') OR
                      regexp_like(api.passengerDetails_dateOfBirth, '^((((19[0-9][0-9])|(2[0-9][0-9][0-9]))([-])(0[13578]|10|12)([-])(0[1-9]|[12][0-9]|3[01]))|(((19[0-9][0-9])|(2[0-9][0-9][0-9]))([-])(0[469]|11)([-])([0][1-9]|[12][0-9]|30))|(((19[0-9][0-9])|(2[0-9][0-9][0-9]))([-])(02)([-])(0[1-9]|1[0-9]|2[0-8]))|(([02468][048]00)([-])(02)([-])(29))|(([13579][26]00)([-])(02)([-])(29))|(([0-9][0-9][0][48])([-])(02)([-])(29))|(([0-9][0-9][2468][048])([-])(02)([-])(29))|(([0-9][0-9][13579][26])([-])(02)([-])(29)))$') THEN 1
                ELSE 0
            END AS vf_person_dob_is_date_score,
            CASE
                WHEN (api.passengerDetails_firstName IS NULL OR api.passengerDetails_firstName = '') OR
                    LENGTH(api.passengerDetails_firstName) BETWEEN 1 AND 35 THEN 1
                ELSE 0
            END AS vf_first_name_length_score,
            CASE
                WHEN (api.passengerDetails_firstName IS NULL OR api.passengerDetails_firstName = '') OR
                      regexp_like(api.passengerDetails_firstName, '^[a-zA-Z\-\._'' ]+$') THEN 1
                ELSE 0
            END AS vf_first_name_alpha_score,
            CASE
                WHEN (api.passengerDetails_gender IS NULL OR api.passengerDetails_gender = '') OR
                      LENGTH(api.passengerDetails_gender) = 1 THEN 1
                ELSE 0
            END AS vf_person_gender_length_score,
            CASE
                WHEN (api.passengerDetails_gender IS NULL OR api.passengerDetails_gender = '') OR
                      regexp_like(api.passengerDetails_gender, '^[a-zA-Z]+$') THEN 1
                ELSE 0
            END AS vf_person_gender_char_score,
            CASE
                WHEN (api.passengerDetails_surname IS NULL OR api.passengerDetails_surname = '') OR
                      LENGTH(api.passengerDetails_surname) BETWEEN 1 AND 35 THEN 1
                ELSE 0
            END AS vf_last_name_length_score,
            CASE
                WHEN (api.passengerDetails_surname IS NULL OR api.passengerDetails_surname = '') OR
                      regexp_like(api.passengerDetails_surname, '^[a-zA-Z\-\._'' ]+$') THEN 1
                ELSE 0
            END AS vf_last_name_alpha_score,
            CASE
                WHEN (api.passengerDetails_nationality IS NULL OR api.passengerDetails_nationality = '') OR
                      LENGTH(api.passengerDetails_nationality) = 3 THEN 1
                ELSE 0
            END AS vf_person_nationality_length_score,
            CASE
                WHEN (api.passengerDetails_nationality IS NULL OR api.passengerDetails_nationality = '') OR
                      regexp_like(api.passengerDetails_nationality, '^[a-zA-Z]+$') THEN 1
                ELSE 0
            END AS vf_person_nationality_char_score,
            CASE
                WHEN (api.passengerDetails_passengerType IS NULL OR api.passengerDetails_passengerType = '') OR
                      LENGTH(api.passengerDetails_passengerType) BETWEEN 1 AND 3 THEN 1
                ELSE 0
            END AS vf_person_passenger_pax_type_length_score,
            CASE
                WHEN (api.passengerDetails_passengerType IS NULL OR api.passengerDetails_passengerType = '') OR
                      regexp_like(api.passengerDetails_passengerType, '^[a-zA-Z]+$') THEN 1
                ELSE 0
            END AS vf_person_passenger_pax_type_char_score,
            CASE
                WHEN (api.passengerDetails_secondName IS NULL OR api.passengerDetails_secondName = '') OR
                      LENGTH(api.passengerDetails_secondName) BETWEEN 1 AND 35 THEN 1
                ELSE 0
            END AS vf_second_name_length_score,
            CASE
                WHEN (api.passengerDetails_secondName IS NULL OR api.passengerDetails_secondName = '') OR
                      regexp_like(api.passengerDetails_secondName, '^[a-zA-Z\-\._'' ]+$') THEN 1
                ELSE 0
            END AS vf_second_name_alpha_score,
            CASE
                WHEN api.flightitinerary_departure_locationfunctioncode = '125' AND (LENGTH(TRIM(api.flightDetails_flightId)) > 11 OR substring(api.flightDetails_flightId,1,3) = '_GA') AND api.flightDetails_departureAirport = 'IATA' THEN api.flightitinerary_departure_locationNameExtended_iataCode
                WHEN api.flightitinerary_departure_locationfunctioncode = '125' AND (LENGTH(TRIM(api.flightDetails_flightId)) > 11 OR substring(api.flightDetails_flightId,1,3) = '_GA') AND api.flightDetails_departureAirport = 'ICAO' THEN api.flightitinerary_departure_locationNameExtended_icaoCode
                ELSE api.flightDetails_departureAirport
            END AS flightDetails_departureAirport_cal,
            CASE
                WHEN api.flightitinerary_arrival_locationfunctioncode = '87' AND (LENGTH(TRIM(api.flightDetails_flightId)) > 11 OR substring(api.flightDetails_flightId,1,3) = '_GA') AND api.flightDetails_arrivalAirport = 'IATA' THEN api.flightItinerary_arrival_locationNameExtended_iataCode
                WHEN api.flightitinerary_arrival_locationfunctioncode = '87' AND (LENGTH(TRIM(api.flightDetails_flightId)) > 11 OR substring(api.flightDetails_flightId,1,3) = '_GA') AND api.flightDetails_arrivalAirport = 'ICAO' THEN api.flightItinerary_arrival_locationNameExtended_icaoCode
                ELSE api.flightDetails_arrivalAirport
            END AS flightDetails_arrivalAirport_cal,
            CASE
                WHEN LENGTH(TRIM(api.flightDetails_flightId)) > 11 THEN REPLACE(api.flightDetails_flightId,'EC_','')
                ELSE ''
            END flightid_rm,
            CASE
                WHEN SUBSTRING(api.flightDetails_flightId,1,3) = '_GA' THEN api.flightDetails_flightId
                ELSE ''
            END flightid_ga,
            api.s3_location,
            api.xml_file_name,
            api.file_name,
            CASE
                WHEN LENGTH(api.passengerDetails_secondName) > 1 THEN 1
                ELSE 0
            END AS df_person_second_name_length_score,
    	    apidoc.vf_document_type_length_score,
    	    apidoc.vf_document_type_char_score
        FROM
            api_input_{namespace}.input_file_api api
	    LEFT OUTER JOIN api_record_level_score_{namespace}.api_working_transformed_document_details_{instance} apidoc ON TO_HEX(MD5(TO_UTF8(UPPER(TRIM(api.xml_file_name))))) = apidoc.hub_parsed_message_sqn AND apidoc.doc_type_Row_Number = 1
            LEFT OUTER JOIN reference_data_{namespace}.salutation sal ON UPPER(api.passengerDetails_firstName) = UPPER(sal.md_title)
            LEFT OUTER JOIN reference_data_{namespace}.gender gn ON UPPER(api.passengerDetails_gender) = UPPER(gn.md_code)
            LEFT OUTER JOIN reference_data_{namespace}.nationalities nt ON UPPER(api.passengerDetails_nationality) = UPPER(nt.code)
            LEFT OUTER JOIN reference_data_{namespace}.person_type pt ON UPPER(api.passengerDetails_passengerType) = UPPER(pt.code)
      WHERE
	    api.path_name = '{path-name}'
	    AND api.extra_rec_type = 'main'
        )api
        LEFT OUTER JOIN reference_data_{namespace}.ports dep_iata_port ON UPPER(api.flightDetails_departureAirport_cal) = UPPER(dep_iata_port.port_iata) AND length(api.flightDetails_departureAirport_cal) > 0
        LEFT OUTER JOIN reference_data_{namespace}.ports dep_icao_port ON UPPER(api.flightDetails_departureAirport_cal) = UPPER(dep_icao_port.port_icao) AND length(api.flightDetails_departureAirport_cal) > 0
        LEFT OUTER JOIN reference_data_{namespace}.ports arr_iata_port ON UPPER(api.flightDetails_arrivalAirport_cal) = UPPER(arr_iata_port.port_iata) AND length(api.flightDetails_arrivalAirport_cal) > 0
        LEFT OUTER JOIN reference_data_{namespace}.ports arr_icao_port ON UPPER(api.flightDetails_arrivalAirport_cal) = UPPER(arr_icao_port.port_icao) AND length(api.flightDetails_arrivalAirport_cal) > 0
        LEFT OUTER JOIN reference_data_{namespace}.carriers carrierIATA ON UPPER(CASE
                                                                  WHEN api.flightId_ga <> '' THEN '_GA'
                                                                  WHEN api.flightid_rm <> '' and regexp_like(SUBSTRING(api.flightid_rm,LENGTH(api.flightid_rm)-9,3),'IMO') THEN
                                                      SUBSTRING(api.flightid_rm,1,LENGTH(api.flightid_rm)-10)
                                                                  WHEN api.flightid_rm <> '' and regexp_like(SUBSTRING(api.flightid_rm,1,10),'Eurotunnel') THEN
                                          SUBSTRING(api.flightid_rm,1,10)
                                                                  WHEN api.flightId_rm <> '' THEN SUBSTRING(flightId_rm,1,LENGTH(flightId_rm) - 11)
                                                                  WHEN regexp_like(SUBSTRING(api.flightDetails_flightId,3,1), '^[a-zA-Z]+$') THEN SUBSTRING(api.flightDetails_flightId,1,3)
                                                                  ELSE SUBSTRING(api.flightDetails_flightId,1,2)
                                                              END) = UPPER(carrierIATA.carrier_iata_code)
        LEFT OUTER JOIN reference_data_{namespace}.carriers carrierICAO ON UPPER(CASE
                                                                  WHEN api.flightId_ga <> '' THEN '_GA'
                                                                  WHEN api.flightid_rm <> '' and regexp_like(SUBSTRING(api.flightid_rm,LENGTH(api.flightid_rm)-9,3),'IMO') THEN
                                                      SUBSTRING(api.flightid_rm,1,LENGTH(api.flightid_rm)-10)
                                                                  WHEN api.flightid_rm <> '' and regexp_like(SUBSTRING(api.flightid_rm,1,10),'Eurotunnel') THEN
                                          SUBSTRING(api.flightid_rm,1,10)
                                                                  WHEN api.flightid_rm <> '' and regexp_like(SUBSTRING(api.flightid_rm,LENGTH(api.flightid_rm)-8,10),'Undefined') THEN SUBSTRING(api.flightid_rm,1,LENGTH(api.flightid_rm)-9)
                                                                  WHEN api.flightid_rm <> '' and regexp_like(api.flightid_rm, '\d{7}') THEN
                                                                  regexp_split(api.flightid_rm,'\d{7}')[1]
                                                                  WHEN api.flightId_rm <> '' THEN SUBSTRING(flightId_rm,1,LENGTH(flightId_rm) - 11)
                                                                  WHEN regexp_like(SUBSTRING(api.flightDetails_flightId,LENGTH(api.flightDetails_flightId)-9,3),'IMO') THEN SUBSTRING(api.flightDetails_flightId,1,LENGTH(api.flightDetails_flightId)-10)
                                                                  WHEN regexp_like(SUBSTRING(api.flightDetails_flightId,LENGTH(api.flightDetails_flightId)-8,10),'Undefined') THEN SUBSTRING(api.flightDetails_flightId,1,LENGTH(api.flightDetails_flightId)-9)
                                                                  WHEN regexp_like(api.flightDetails_flightId, '\d{7}') THEN regexp_split(api.flightDetails_flightId,'\d{7}')[1]
                                                                  WHEN regexp_like(SUBSTRING(api.flightDetails_flightId,3,1), '^[a-zA-Z]+$') THEN SUBSTRING(api.flightDetails_flightId,1,3)
                                                                  ELSE SUBSTRING(api.flightDetails_flightId,1,2)
                                                              END)  = UPPER(carrierICAO.carrier_icao_code)
        LEFT OUTER JOIN (SELECT * FROM working_cs_{instance} ) cs ON
		    (( cs.carrier_type != 'SEA' AND
          UPPER(CASE
                        WHEN api.flightId_ga <> '' THEN REPLACE(api.flightid_ga,'_GA','')
                        WHEN api.flightid_rm <> '' and regexp_like(SUBSTRING(api.flightid_rm,LENGTH(api.flightid_rm)-9,3),'IMO') THEN
            SUBSTRING(api.flightid_rm,LENGTH(api.flightid_rm)-9,11)
                        WHEN api.flightid_rm <> '' and regexp_like(SUBSTRING(api.flightid_rm,1,10),'Eurotunnel') THEN
SUBSTRING(api.flightid_rm,LENGTH(api.flightid_rm)-3,4)
                        WHEN api.flightid_rm <> '' THEN SUBSTRING(api.flightid_rm,LENGTH(api.flightid_rm)-10,11)
                        WHEN regexp_like(SUBSTRING(api.flightDetails_flightId,3,1), '^[a-zA-Z]+$') THEN LPAD(regexp_replace(SUBSTRING(TRIM(api.flightDetails_flightId),4,4),'[^0-9]'),4,'0')
                        ELSE LPAD(regexp_replace(SUBSTRING(TRIM(api.flightDetails_flightId),3,4),'[^0-9]'),4,'0')
                    END) = UPPER(cs.voyage_number))
                    OR
                    (cs.carrier_type = 'SEA'
                    )
                  )

                    AND UPPER(CASE
                                 WHEN carrierIATA.master_carrier_md_code IS NULL AND carrierICAO.master_carrier_md_code IS NULL THEN COALESCE(carrierIATA.carrier_md_code, carrierICAO.carrier_md_code)
                                 ELSE COALESCE(carrierIATA.master_carrier_md_code, carrierICAO.master_carrier_md_code)
                    END) = UPPER(cs.carrier_md_code)
                    AND ((
                      	UPPER(cs.inbound_outbound) = 'OUT'
                        AND cs.carrier_type != 'SEA'
                      	AND CAST(TRY(CAST(api.flightDetails_departureDateTime AS TIMESTAMP)) AS DATE) = TRY(CAST(cs.std_datetime_local AS DATE))
                      	AND UPPER(COALESCE(dep_iata_port.port_md_code,dep_icao_port.port_md_code)) = UPPER(cs.departure_port_md_code)
                    	)
                    	OR
                    	(
                      	UPPER(cs.inbound_outbound) = 'IN'
                        AND cs.carrier_type != 'SEA'
                      	AND CAST(TRY(CAST(api.flightDetails_arrivalDateTime AS TIMESTAMP)) AS DATE) = TRY(CAST(cs.sta_datetime_local AS DATE))
                      	AND UPPER(COALESCE(arr_iata_port.port_md_code,arr_icao_port.port_md_code)) = UPPER(cs.arrival_port_md_code)
			                  )
                      OR
                      (
                        cs.carrier_type = 'SEA'
                        AND CAST(TRY(CAST(api.flightDetails_departureDateTime AS TIMESTAMP)) AS DATE) = TRY(CAST(cs.std_datetime_local AS DATE))
                        AND CAST(TRY(CAST(api.flightDetails_departureDateTime AS TIMESTAMP)) AS TIME) = TRY(CAST(cs.std_datetime_local AS TIME))
                      	AND UPPER(COALESCE(dep_iata_port.port_md_code,dep_icao_port.port_md_code)) = UPPER(cs.departure_port_md_code)
                        AND UPPER(COALESCE(arr_iata_port.port_md_code,arr_icao_port.port_md_code)) = UPPER(cs.arrival_port_md_code)
                      )
                    	)
    )api
) all
WHERE rnum = 1;
