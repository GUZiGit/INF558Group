from subprocess import run, PIPE

p = run('python3 runLocalSpider.py',stdout = PIPE,input=('http://baidu.com$http://google.com'),encoding='ascii')
print('output from sender: '+p.stdout)

# for url in p.stdout.split('\\n'):
# 	print('output: '+url)
# 	print('')
