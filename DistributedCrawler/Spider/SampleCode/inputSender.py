from subprocess import run, PIPE

p = run('python3 inputReceiver.py',stdout = PIPE,input=(' urls a\\n  urls b'),encoding='ascii')
print('from sender: '+p.stdout)

for url in p.stdout.split('\\n'):
	print('a url: '+url)
	print('')

# chunkDataPiece = p.stdout
# p = run('crfsuite.exe tag -m %s' % modelDir,stdout = PIPE,input=(chunkDataPiece+'\n\n'),encoding='ascii')
# labels = p.stdout.split('\n')

