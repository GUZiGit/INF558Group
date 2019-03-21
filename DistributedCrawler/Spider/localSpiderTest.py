from subprocess import run, PIPE, Popen,check_output
import re
# import sys
import os

os.system('python3 runLocalSpider.py https://classes.usc.edu/term-20191/classes/buad/')
# import unicode
# byteResult = check_output(['python3','runLocalSpider.py','http://baidu.com'])
# print(byteResult)

# print(sys.getdefaultencoding())
# print(str(byteResult,'utf-8'))

# exec('runLocalSpider.py','http://baidu.com')

# p =  Popen(['python3','runLocalSpider.py','http://baidu.com'],stdout=PIPE,encoding='ascii')
# # stdout = p.communicate('http://baidu.com')
# print(stdout)

# p.stdin.write('http://baidu.com')
# p.stdin.close()
# p.decode('utf-8')
# result = p.stdout.read()
# result = p.check_output()

# p.stdout.encoding='ascii'
# print(p.stdout.encoding)
# print(result)
# print(type(result))
# print(result)
# print(str(result[2:-2],'utf-8'))

# content = p.communicate(input='http://baidu.com')[0]

# p = run('python3 runLocalSpider.py',stdout=PIPE, check=True,shell=True,universal_newlines=True,input='http://baidu.com',encoding='ascii')
# content = str(p.stdout)
# print(content)
# print(type(content))
# print(content)
# print(content[2:-2].encode('UTF-8'))
# print("output end")
# reResult = re.findall(r'(<MyContent>)(.*)(</MyContent>)',content)
# print(reResult)
# for o in reResult:
	# print(o[1])


# for url in p.stdout.split('\\n'):
# 	print('output: '+url)
# 	print('')
