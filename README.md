# Bitcoin Dashboard

Example of CI/CD pipeline for an [interactive dashboard](https://boiling-taiga-96904.herokuapp.com/).

## CONCLUSION:
The goal of this interactive app is to evaluate the performance of a simple rule-based trading algorithm. No forecast, learning or anything : very simple. After playing with its various parameters you will see that the algorithm is very performant when volatility increases. The idea can be used in practice to limit the risks associated with order fancy algorithms trading in parallel (diversification).

## INTRO:
Here is the idea: I believe Bitcoin is a chaotic system of second order. It means that correctly guessing the future of Bitcoin AND making money on it is a loss of time. For example if I know Bitcoin's price will increase tomorrow I buy today which increases the price today. And it changes the conditions a chaotic system is very sensitive to. By correctly guessing the future I act on it which prevents it from happening. I think this is one of the reasons why Bitcoin is acting like a random walk.

## MATERIAL AND METHOD:
Instead of losing my time guessing the future, I only focus on historical prices. BUY/SELL orders are based on strict rules. These rules are dependent on the number of days (today included) we look in the past and the proportion we BUY/SELL:

- If today Bitcoin's price is HIGHER than previous daily prices I SELL a proportion of my Bitcoin
- If today Bitcoin's price is LOWER than previous daily prices I BUY with a proportion of my Money

![alt text](https://github.com/seaslug95/testbitcoin/blob/master/pics/Schema_Algo.PNG?raw=true)
