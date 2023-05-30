SELECT vr.id as varietal_region, v.name, r.country, r.id
FROM whiterabbitapi_varietalregion vr
JOIN whiterabbitapi_varietal v on v.id = vr.varietal_id
JOIN whiterabbitapi_region r on r.id = vr.region_id

 SELECT vr.id as varietal_region, v.name, r.country, r.location
            FROM whiterabbitapi_varietalregion vr
            JOIN whiterabbitapi_varietal v on v.id = vr.varietal_id
            JOIN whiterabbitapi_region r on r.id = vr.region_id 