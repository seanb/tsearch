#! /usr/bin/env python
"""Command-line twitter search tool

Copyright (c) 2010 Ehsan (Sean) Baseri

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE."""

import sys, urllib, json, HTMLParser, re
from optparse import OptionParser

def twitter_search(query, language, results_per_page, results_page):
	url = "http://search.twitter.com/search.json?" + "q=" + urllib.quote(query) + "&lang=" + language + "&rpp=" + str(results_per_page) + "&page=" + str(results_page)
	
	response = urllib.urlopen(url)
	data = json.load(response)
	response.close()
	
	return data

def print_results(results, encoding_format):
#	print "Completed in: %ss" % results["completed_in"]
	parser = HTMLParser.HTMLParser()
	
	try:
		print "Error from twitter API: " + results["error"]
	except KeyError:
		for tweet in results["results"]:
			text = re.sub(r'( |\t)*\n( |\t)*',r' \\n ',parser.unescape(tweet["text"])) 
			# print "%-21s : %-144s" % (tweet["from_user"], text) 
			text_print = u'{0:<21} : {1:<144}'.format(tweet["from_user"], text) 
			
			if encoding_format == 'auto':
				print text_print
			else:
				print text_print.encode(encoding_format, 'ignore')


if __name__ == "__main__":
	parser = OptionParser(usage="usage: %prog [options] SEARCH_STRING")
	
	parser.add_option("-l", "--language", type="string", dest="language", default="all", 
		help="Language of tweets (i.e. en, es, de, fr, fa) (default=all)")
	parser.add_option("-n", "--rpp", type="int", dest="results_per_page", default=20, 
		help="Tweets per search result (default=20)")
	parser.add_option("-p", "--page", type="int", dest="results_page", default=1,
		help="Page of search results (default=1)")
	parser.add_option("-e", "--encoding", type="string", dest="encoding_format", default="auto",
		help="Output encoding format (i.e. ascii, utf-8, auto) (default=auto)")

	try:	
		(options, args) = parser.parse_args()
		results = twitter_search(args[0], options.language, options.results_per_page, 
															options.results_page)
		print_results(results, options.encoding_format)
	except IndexError:
		print "Error: Need a search string"
		parser.print_help()
