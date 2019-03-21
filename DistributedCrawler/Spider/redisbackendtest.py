from redisbackend import RedisBackend

r = RedisBackend()
print(r.pullUrls())

r.pushUrls(['abc','xxx'])

print(r.pullUrls())
