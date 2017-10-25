## Data service (in charge: ziqi liu)
### detail
due to performance reason and some api calling constrain, we decide to cache some data in database (i.e, pre-fetch the data using scrapy).

Basically, our data consist of three categories: 

* block statistic (population, education, income, etc.)
* crime statistic
* google places data.

Also, we need to design an algorithm to calculate the scores for recommendation according to user's preference.

### Task

1. pre-fetch block statistic data from factfinder.

	- timeline: completed

2. pre-fetch crime statistic data from spotcrime

	- timeline: still under processing, estimated finished time: 11.2
	- additional info: due to the api calling constrain, the scrapy runs slowly, and we need to double check the data isn't corrupted.

3. pre-fetch google places data

	- timeline: haven't started yet, will begin next week
	- additional info: we need to discuss how to feed api data according to map area split

	
4. rankning scores algorithm design

	-  timeline: completed
	-  additional info: might be adjusted afterwards

5. algorithm mapping radius-based api data into block area in map

	- timeline: still under processing
	- additional info: work together with David

6. dashboard

### issue
the main challenge we're facing now is that how to map radius-based api data into block area in the map. Can only make a approximation, but we want to do it as reasonble as possible.

## Dashboard Service and User module backend (in charge: ziqi liu)

### detail

provide basic backend views to enable user interaction. and dashboard data stream

### Task
1. views functions about user interactions (login, comment, like, favorite list, etc.)

	- timeline: under processing, estimated finished: 11.5

2. views functions provide dash board data stream

	- timeline: under processing, estimated finished: 11.10
	- additional info: need further discussion about map area split


