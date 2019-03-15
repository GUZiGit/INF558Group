import scrapy
from scrapy.crawler import CrawlerProcess

from subprocess import run, PIPE

class LocalSpider(scrapy.Spider):
	name = 'spiderName'
	debugMode = True

	def start_requests(self):
		urls = input()
		if self.debugMode:
			print('urls: '+urls)
		urls = urls.split('$')
		if self.debugMode:
			# print('urls: '+urls)
			for url in urls:
				print('LocalSpider.start_requests(): '+url)
		for url in urls:
			yield scrapy.Request(url = url, callback = self.parse)

	def parse(self,response):
		print('from LocalSpider.parse()')
		print(response.body)
		print('')

# p = run('python3 chunking.py',stdout = PIPE,input=(words+'\n\n'),encoding='ascii')
# chunkDataPiece = p.stdout
# p = run('crfsuite.exe tag -m %s' % modelDir,stdout = PIPE,input=(chunkDataPiece+'\n\n'),encoding='ascii')
# labels = p.stdout.split('\n')


def main():
	process = CrawlerProcess()
	process.crawl(LocalSpider,input = ' -s LOG_ENABLED=0')
	process.start()

if __name__ == '__main__':
	main()
