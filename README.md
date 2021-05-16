# binance-cashandcarry-tracker
AWS files to track contango premium on Binance

The Lambda Function files read Futures data from Binance, calculate the annual premium for open contracts and whenever any of these  premiums is above a pre determined threshold they send this information to a Telegram Chat. 
