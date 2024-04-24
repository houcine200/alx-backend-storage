-- Select the country origin and calculate
-- the sum of fans for each origin
SELECT origin, SUM(fans) AS nb_fans
FROM metal_bands
GROUP BY origin
ORDER BY nb_fans DESC;
