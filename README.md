# INF558Group - Group Project

### Part 1. Distributed Web Crawler

##### Individual Components

- Master - fetch jobs, distribute jobs to spiders
- Spider - execute jobs
- DataBackend - receive spider outcome and save outcomes

##### Spider Logic

1. Registrate to master
   1. for master - create topic for this spider
2. Subscribe topic and wait until Kafka message come
3. Decode Kafka message
   1. Quit command
   2. urls to crawl
4. Execute command
   1. quit
   2. run crawler
5. (urls) Parse content
6. Save urls in redis
7. Send content to DataBackend