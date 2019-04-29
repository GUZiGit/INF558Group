# Group 17 Course Knowledge Graphs Report

**Zi Gu zigu@usc.edu**

**Haili Wang hailiwan@usc.edu**



## Contents



**1. Building Knowledge Graphs**

1.  Web Crawling - USC, UCLA, UCB
2. Ontology
3. HTMLs to Json-LD
4. Entity Matching - Instructor Matching
5. PDF Extraction - Syllabus => email & office hour



**2. Elasticsearch & GUI App**

1. Elasticsearch

 	2. Python GUI - Tkinter, Json Viewer, dot, graphviz

​		

## 1. Building Knowledge Graphs



### 1.1 Web Crawling - USC, UCLA, UCB



**Base URL**

USC: https://classes.usc.edu/term-20191/

UCLA: https://www.registrar.ucla.edu/Academics/Course-Descriptions

UCB: http://guide.berkeley.edu/courses/



**Extraction Details - USC**

![1556260582566](C:\Users\Rice\AppData\Roaming\Typora\typora-user-images\1556260582566.png)

![1556260623853](C:\Users\Rice\AppData\Roaming\Typora\typora-user-images\1556260623853.png)



**Extraction Details - UCLA**



![1556260669562](C:\Users\Rice\AppData\Roaming\Typora\typora-user-images\1556260669562.png)

![1556260683822](C:\Users\Rice\AppData\Roaming\Typora\typora-user-images\1556260683822.png)



**Extraction Details - UCB**



![1556260727904](C:\Users\Rice\AppData\Roaming\Typora\typora-user-images\1556260727904.png)

![1556260793306](C:\Users\Rice\AppData\Roaming\Typora\typora-user-images\1556260793306.png)



### 1.2 Ontology



**Overview**

Use three main objects with attributes and links to each other. Implement by Protege. 



![1556262096148](C:\Users\Rice\AppData\Roaming\Typora\typora-user-images\1556262096148.png)



**Object Details**

Course: Course Abbreviation, Course Name, Description, Program Name, University Name, Section IDs

Section: Time, Location, Syllabus Link, Email, Session Type, Office Hour, Instructor ID

Instructor: Instructor, Name, Instructor Link



### 1.3 HTMLs to Json-LD

Build python scripts convert html files to Json-LD format.

```json
{
	"@context": {
		"ckb": "http://www.semanticweb.org/rice/ontologies/2019/3/CourseKB",
		"xsd": "http://www.w3.org/2001/XMLSchema"
  	},
  	@graph:[
  		// list of Course, Section Objects so far. Instructors are added later.
  	]
}
```



### 1.4 Entity Matching - Instructor Matching

Each section in previous Json-LD contains a individual Instructor object. This step matches Instructors by similarity of Instructor name. Extract Instructor object from Section object, add unique IDs, and put in @graph list. Use InstructorID in Section object as linkage. Here, three main objects, Course, Section, Instructor are listed properly in @graph.

Similarity function of Instructor name is based on edit distance.



### 1.5 PDF Extraction - Syllabus => email & office hour

Instructor Email and office hour are extracted from PDF syllabus. PyPDF2 is used to convert PDF files to text. Then apply regular expression to extract email and office hour.



```python
# office hour regular expression
r'(?i)office hour[s]?[:]?[\s\n]*?([\d\w\-\.\,\:\t]+[\d]*'

# email
r'[e|E][-]?[m|M]ail[:]?[\s]*?([\w\.-]+@[\w\.-]+
```



![1556292392126](C:\Users\Rice\AppData\Roaming\Typora\typora-user-images\1556292392126.png)



## Elasticsearch & GUI App



### 2.1 Elasticsearch



**Data Deployment**

Based on previous Json-LD structure, we build a python script to extract objects in @graph and build index in Elasticsearch. Objects from three universities are list together. So finally, there is an index which contains a list of Course, Section, Instructor objects from three universities.



### 2.2 Python GUI - Tkinter, Json Viewer, dot, graphviz



**Screen Shots - Search Window**

![1556296461592](C:\Users\Rice\AppData\Roaming\Typora\typora-user-images\1556296461592.png)



**Screen Shots - Search Result - Json Viewer**

![1556296498824](C:\Users\Rice\AppData\Roaming\Typora\typora-user-images\1556296498824.png)



**Screen Shots - Search Result - Tree Graph**

![1556296524059](C:\Users\Rice\AppData\Roaming\Typora\typora-user-images\1556296524059.png)

![1556296567214](C:\Users\Rice\AppData\Roaming\Typora\typora-user-images\1556296567214.png)



**Implementation Details**

Basic search window is built by tkinter. 

Json Viewer is an open source github repo from https://github.com/ashwin/json-viewer. 

Tree graphs is built based on graphviz and dot language. With query result, rebuilt that into a dot file and generate image by graphviz.



**Query Details - Breadth Search**

Breadth search locates all results that are relevant to user query. Rank results by similarity score. Result shows a list of one object.

Query in code is formed as follow. Two matches restrict @type and search keyword.

```python
basicBody = {
      'query': {
          'bool':{
              'must':[
                  {'match':{}},
                  {'match':{}}
              ]
          }
      }
    }
```



**Query Details - Depth Search**

Depth search locate one result which is most relevant to user query. Then it search related parent nodes and child nodes and combine them together as Json object result.

For example, this is a result from depth search, which search course name 'knowledge graphs'.

![1556297405044](C:\Users\Rice\AppData\Roaming\Typora\typora-user-images\1556297405044.png)

Query in code is a nested for loop structure, which iteratively detect parent nodes and child nodes.



**3. Distributed Web Crawler**

1. Overall Structure

2. Spider Logic
3. Master Logic

## Distributed Web Crawler

**This part is built before midterm progress report, so content here will be similar to previous report**



### 3.1 Overall Structure

![GeneralConnection](C:\Users\Rice\Desktop\INF558Group\Documents\GeneralConnection.png)

- Master program
  - Distribute URLs(jobs) to Spiders with care of priority and politeness
  - Only one Master program in total.
- Spiders
  - Listen to Master program, receive jobs, fetch data from Internet, parse data and save data in Redis and Mongo DB.
  - Number of spider almost has no limitation.
- Redis Cluster
  - A in-memory distributed database used to maintain URLs and document fingerprints.
- Mongo DB Cluster
  - A normal distributed No-SQL database used to maintain crawled data from web.
- Kafka Cluster
  - A distributed message queue application used to maintain message connection among individual components.
  - All solid arrows are connection based on Kafka Cluster. Hollow arrows are direct Internet connection.

**Steps to Run**

1. Run component Master program with configuration of crawling speed, priority information, start URLs.
2. Run component Spider with a unique ID.
3. Spider will send message through Kafka to Master as a registration process.
4. Master distributes jobs to spiders with care of priority and politeness.
5. Spiders receive jobs, analysis content, save new URLs into Redis, save other useful data into Mongo DB.
6. Master will fetch new URLs from Redis and distribute them to spiders again.



### 3.2 Master Logic



![MasterLogic](C:\Users\Rice\Desktop\INF558Group\Documents\MasterLogic.png)





### 3.3 Spider Logic

![SpiderLogic](C:\Users\Rice\Desktop\INF558Group\Documents\SpiderLogic.png)



