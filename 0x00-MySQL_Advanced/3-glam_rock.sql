-- Select band names and lifespans, filtering for "Glam rock"
-- style, and sorting by lifespan.
SELECT band_name, (IFNULL(split, 2022) - formed) AS lifespan
FROM metal_bands
WHERE style LIKE '%Glam rock%'
ORDER BY lifespan DESC;
