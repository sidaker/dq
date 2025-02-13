CREATE OR REPLACE VIEW "view_datadrop_summary_combined" AS
SELECT
"row_number"() OVER (ORDER BY 1 ASC) row
, CASE WHEN (("internal_storage_table_history".dep_port_country_md_code = 'GBR') AND ("internal_storage_table_history".arr_port_country_md_code = 'GBR')) THEN 'Domestic'
        WHEN (("internal_storage_table_history".dep_port_country_md_code = 'GBR') AND ("internal_storage_table_history".arr_port_country_md_code <> 'GBR')) THEN 'Outbound'
        WHEN (("internal_storage_table_history".dep_port_country_md_code <> 'GBR') AND ("internal_storage_table_history".arr_port_country_md_code = 'GBR')) THEN 'Inbound'
        WHEN (("internal_storage_table_history".dep_port_country_md_code <> 'GBR') AND ("internal_storage_table_history".arr_port_country_md_code <> 'GBR')) THEN 'International-International'
        WHEN (("internal_storage_table_history".dep_port_country_md_code IS NULL) AND ("internal_storage_table_history".arr_port_country_md_code IS NULL)) THEN 'Unknown' END inbound_outbound
, "internal_storage_table_history".flightdetails_arrivalairport Arrival_port
, "internal_storage_table_history".flightdetails_arrivaldatetime Arrival_datetime
, "internal_storage_table_history".flightdetails_carrier Carrier_code
, "internal_storage_table_history".flightdetails_datetimesent Submission_datetime
, "internal_storage_table_history".manifestdetails_datetimereceived Receipt_datetime
, "internal_storage_table_history".flightdetails_departureairport Departure_port
, "internal_storage_table_history".flightdetails_departuredatetime Departure_datetime
, CASE WHEN ("internal_storage_table_history".flightdetails_departuredatetime IS NOT NULL)
    THEN "concat"("substr"("internal_storage_table_history".flightdetails_departuredatetime, 9, 2), '/', "substr"("internal_storage_table_history".flightdetails_departuredatetime, 6, 2), '/', "substr"("internal_storage_table_history".flightdetails_departuredatetime, 1, 4), ' ', "substr"("internal_storage_table_history".flightdetails_departuredatetime, 12, 2), ':', "substr"("internal_storage_table_history".flightdetails_departuredatetime, 15, 2)) ELSE null END "departure_date/time"
, CASE WHEN ("internal_storage_table_history".flightdetails_arrivaldatetime IS NOT NULL)
    THEN "concat"("substr"("internal_storage_table_history".flightdetails_arrivaldatetime, 9, 2), '/', "substr"("internal_storage_table_history".flightdetails_arrivaldatetime, 6, 2), '/', "substr"("internal_storage_table_history".flightdetails_arrivaldatetime, 1, 4), ' ', "substr"("internal_storage_table_history".flightdetails_arrivaldatetime, 12, 2), ':', "substr"("internal_storage_table_history".flightdetails_arrivaldatetime, 15, 2)) ELSE null END "arrival_date/time"
, CASE WHEN ("internal_storage_table_history".manifestdetails_datetimereceived IS NOT NULL)
    THEN "concat"("substr"("internal_storage_table_history".manifestdetails_datetimereceived, 9, 2), '/', "substr"("internal_storage_table_history".manifestdetails_datetimereceived, 6, 2), '/', "substr"("internal_storage_table_history".manifestdetails_datetimereceived, 1, 4), ' ', "substr"("internal_storage_table_history".manifestdetails_datetimereceived, 12, 2), ':', "substr"("internal_storage_table_history".manifestdetails_datetimereceived, 15, 2)) ELSE null END "receipt_date/time"
, CASE WHEN ("internal_storage_table_history".flightdetails_datetimesent IS NOT NULL)
    THEN "concat"("substr"("internal_storage_table_history".flightdetails_datetimesent, 9, 2), '/', "substr"("internal_storage_table_history".flightdetails_datetimesent, 6, 2), '/', "substr"("internal_storage_table_history".flightdetails_datetimesent, 1, 4), ' ', "substr"("internal_storage_table_history".flightdetails_datetimesent, 12, 2), ':', "substr"("internal_storage_table_history".flightdetails_datetimesent, 15, 2)) ELSE null END "submission_date/time"
, "internal_storage_table_history".flightdetails_eventcode message_type
, CASE WHEN "regexp_like"("substring"("internal_storage_table_history".flightDetails_flightId, 3, 1), '^[a-zA-Z]+$') THEN "concat"("internal_storage_table_history".flightdetails_carrier, "lpad"("regexp_replace"("substring"("trim"("internal_storage_table_history".flightDetails_flightId), 4, 4), '[^0-9]'), 4, '0')) ELSE "concat"("internal_storage_table_history".flightdetails_carrier, "lpad"("regexp_replace"("substring"("trim"("internal_storage_table_history".flightDetails_flightId), 3, 4), '[^0-9]'), 4, '0')) END Voyage_code
, "internal_storage_table_history".flightdetails_manifesttype manifest_type
, "internal_storage_table_history".carrier_type
, "internal_storage_table_history".sourcedata_interactivedata_isinteractive
, localtimestamp extract_date
,"Carriers"."carrier_iata_code"
,"Carriers"."carrier_icao_code"
,"Carriers"."carrier_md_code"
,"Carriers"."name" AS carrier_name
FROM
  internal_storage_table_history
LEFT JOIN "reference_data_{namespace}"."Carriers" ON "internal_storage_table_history"."flightdetails_carrier" = "Carriers"."Carrier_md_code"
WHERE (("internal_storage_table_history".path_name > "concat"(CAST((current_date + INTERVAL  '-61' DAY) AS varchar(10)), '-history'))
AND ("internal_storage_table_history".carrier_type = 'AIR'))
AND (("date"("substring"(flightdetails_departuredatetime, 1, 10)) >= (current_date - INTERVAL  '31' DAY)) AND ("date"("substring"(flightdetails_departuredatetime, 1, 10)) < current_date))
;
