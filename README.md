# crvSTETHMonitor

This tasty dish of spaghetti a la bolognesa is designed to provide more detailed information about the current value of your Curve stETH/ETH pool and track & display 
it's real value, simulating withdrawing your curve pool tokens as either 100% ETH or stETH, instead of multiplying by the price of the curve tokens. 
IMO this provides a more valid result since it's literally what you would do when you would convert your curve tokens to dollars, you'd unstake them and then sell the 
number you got. It also uses chainlink as price oracle, mainly because I'm lazy.

There are two parts:

grab_data.py is is designed to be run by a job scheduler, and saves the current values to a .csv file

display_data.py is designed to be run to display the data in a graph and table.

You  probably need to create a Brownie environment in the folder where you run this (brownie init --force), I'm not 100% sure.

### Oh, you can also set it to automatically **claim** your LDO reward tokens should both conditions be met: minimum $value of tokens, maximum gas price.
The idea here isn't to dump those and somehow reinvest them (which is a silly thing to do), but to take advantage of low gas prices and be able to sell the LDO tokens
when you think they're at a high. Again, it's **OPTIONAL**.

![alt text](https://i.imgur.com/AZyYei8.png)
