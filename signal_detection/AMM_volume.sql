-- Description: This query calculates the volume of trades on AMMs on Dune
SELECT  
    date_trunc('day', block_time),                                                                 
    SUM(usd_amount) as usd_volume                                                                               
FROM dex."trades" t                                                                                    
WHERE block_time > '2022-01-01'::DATE                                                           
AND block_time < '2023-01-01'::DATE 
AND category = 'DEX'
AND (token_a_symbol = 'ETH' or token_a_symbol = 'WETH')
GROUP BY 1