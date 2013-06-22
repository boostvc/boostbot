
from botinator import botinator
from functools import partial
import datetime
import json
import urllib

def remaining(type, matches, messenger, state):
	end_date = datetime.datetime(2013, 9, 24)
	d = end_date - datetime.datetime.now()
	suffix = " remaining in the incubator"
	if type is 'seconds':
		return str(d.total_seconds()) + " seconds" + suffix
	elif type is 'weeks':
		return str(d.days / 7) + " weeks" + suffix
	elif type is 'minutes':
		return str(d.total_seconds() / 60) + " minutes" + suffix
	else:
		return str(d.days) + " days" + suffix

# Bitcoin functions

def market_api(matches, messenger, state):
	markets = json.loads(urllib.urlopen("http://api.bitcoincharts.com/v1/markets.json").read())
	print(markets[0])
	print(matches[0][:-1])
	market = filter(lambda x: x['symbol'] == matches[0][:-1], markets)
	if market:
		market = market[0]
		return str(market['symbol']) + ": [High: " + str(market['high']) + "], [Low: " + str(market['low']) + "], [Last trade: " + str(market['latest_trade']) + "], [Bid: " + str(market['bid']) + "], [Volume: " + str(market['volume']) + "], [Ask: " + str(market['ask']) + "], [Average: " + str(market['avg']) + "]"
	else:
		return 'unknown market'

def weighted_prices(matches, messenger, state):
	prices = json.loads(urllib.urlopen("http://api.bitcoincharts.com/v1/weighted_prices.json").read())
	entry = prices.get(matches[0][:-1].upper())
	if entry:
		return "7 days: " + entry['7d'] + ", 30 days: " + entry['30d'] + ", 24 hours: " + entry['24h']
	else:
		return 'unknown currency'
	

chan = '#botparty'
boostbot = botinator.Bot('irc.freenode.net')
boostbot.nick('boostbot')
boostbot.user_and_ircname('bot', 'Winston Churchill')
boostbot.join(chan)

boostbot.listen('boostbot: remaining seconds', partial(remaining, 'seconds'))
boostbot.listen('boostbot: remaining minutes', partial(remaining, 'minutes'))
boostbot.listen('boostbot: remaining weeks', partial(remaining, 'weeks'))
boostbot.listen('boostbot: remaining', partial(remaining, 'days'))

# Bitcoin stuff
boostbot.listen('boostbot: bitcoin (.*)', weighted_prices)
boostbot.listen('boostbot: market (.*)', market_api)

boostbot.cron((None, 12, None, None, None), partial(remaining, 'days'), chan)

boostbot.live()
