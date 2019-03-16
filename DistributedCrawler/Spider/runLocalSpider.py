from scrapy.crawler import CrawlerProcess
import logging
import sys
from LocalSpider import LocalSpider


def main():
	# disable stdout logging
	logging.getLogger('scrapy').propagate = False
	process = CrawlerProcess()
	process.crawl(LocalSpider,input=sys.argv[1])
	process.start()

if __name__ == '__main__':
	main()
