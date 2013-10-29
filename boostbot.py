from botinator import botinator
from functools import partial
import random
import datetime
import json
import urllib
import urllib2
import time

## Boostbot functions

# Predict who will win at smash bros using what character

def smash_bros_prediction():
	characters = ['Captain Falcon', 'Donkey Kong', 'Fox', 'Jigglypuff', 'Kirby', 'Link', 'Luigi', 'Mario', 'Ness', 'Pikachu', 'Samus', 'Yoshi']
	people = ['Adam', 'Brayton', 'Ross']
	character.shuffle()
	people.shuffle()
	person0 = people.pop()
	person1 = people.pop()
	char = characters.pop()
	return "I foresee that " + person0 + " will beat " + person1 + " using " + char

# Get remaining time in the incubator program

def remaining(type, matches, messenger, state):
	end_date = datetime.datetime(2014, 1, 27)
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

# Return a cat picture, ignoring the various required parameters

def get_cat(matches, messenger, state):
	return cat_of_the_day()

# Use thecatapi.com to get a random cat picture

def cat_of_the_day():
	req = urllib2.Request('http://thecatapi.com/api/images/get')
	res = urllib2.urlopen(req)
	finalurl = res.geturl()
	return 'randomcat yay -> ' + finalurl

## Bitcoin API stuff

# Return data about a bitcoin exchange

def get_market(symbol):
	markets = json.loads(urllib.urlopen("http://api.bitcoincharts.com/v1/markets.json").read())
	market = filter(lambda x: x['symbol'] == symbol, markets)
	if market:
		market = market[0]
		return str(market['symbol']) + ": [High: " + str(market['high']) + "], [Low: " + str(market['low']) + "], [Last trade: " + time.strftime("%D %H:%M", time.localtime(int(market['latest_trade']))) + "], [Bid: " + str(market['bid']) + "], [Volume: " + str(market['volume']) + "], [Ask: " + str(market['ask']) + "], [Average: " + str(market['avg']) + "]"
	else:
		return 'unknown market'

# Get data about a user-supplied market

def market_api(matches, messenger, state):
	return get_market(matches[0][:-1])

# Get the weighted price of bitcoin in any currency

def get_weighted_price(currency):
	prices = json.loads(urllib.urlopen("http://api.bitcoincharts.com/v1/weighted_prices.json").read())
	entry = prices.get(currency)
	if entry:
		return "7 days: " + entry['7d'] + ", 30 days: " + entry['30d'] + ", 24 hours: " + entry['24h']
	else:
		return 'unknown currency'

# Return the weighted price of bitcoin from the user-supplied currency

def weighted_prices(matches, messenger, state):
	return get_weighted_price(matches[0][:-1].upper())


# Initialize boostbot

chan = '#boostvc'
boostbot = botinator.Bot('irc.freenode.net')
boostbot.nick('boostbot')
boostbot.user_and_ircname('bot', 'Brobot 9000')
boostbot.join(chan)

# Listen for requests to say the remaining time in incubator
boostbot.listen('boostbot: remaining seconds', partial(remaining, 'seconds'))
boostbot.listen('boostbot: remaining minutes', partial(remaining, 'minutes'))
boostbot.listen('boostbot: remaining weeks', partial(remaining, 'weeks'))
boostbot.listen('boostbot: remaining', partial(remaining, 'days'))

# Bitcoin stuff
boostbot.listen('boostbot: bitcoin (.*)', weighted_prices)
boostbot.listen('boostbot: market (.*)', market_api)

# random cats
boostbot.listen('randomcat', get_cat)

boostbot.cron((None, 12, None, None, None), partial(remaining, 'days'), chan)
boostbot.cron((None, 0, None, None, None), partial(remaining, 'seconds'), chan)
boostbot.cron((None, 1, None, None, None), partial(get_weighted_price, 'usd'), chan)
boostbot.cron((None, 2, None, None, None), partial(get_weighted_price, 'usd'), chan)
boostbot.cron((None, 3, None, None, None), partial(get_market, 'mtgoxUSD'), chan)
boostbot.cron((None, 4, None, None, None), partial(get_market, 'bitstampUSD'), chan)
boostbot.cron((None, 5, None, None, None), partial(remaining, 'weeks'), chan)
boostbot.cron((None, 6, None, None, None), cat_of_the_day, chan)
boostbot.cron((None, 7, None, None, None), smash_bros_prediction, chan)

boostbot.live()
