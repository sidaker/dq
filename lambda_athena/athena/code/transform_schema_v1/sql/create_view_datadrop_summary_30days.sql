CREATE OR REPLACE VIEW "view_datadrop_summary_30days" AS
SELECT
"api_datadrops_30days".*
,"Carriers"."carrier_iata_code"
,"Carriers"."carrier_icao_code"
,"Carriers"."carrier_md_code"
,"Carriers"."name" AS carrier_name
FROM "api_record_level_score_prod"."api_datadrops_30days"
LEFT JOIN "reference_data_prod"."Carriers" ON "api_datadrops_30days"."carrier_code" = "Carriers"."Carrier_md_code"
;
