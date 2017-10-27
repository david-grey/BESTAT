## User service (In charge: Dan Hou)

1. Sign up page *Implemented by Dan*

	- Have completed static content
	- Milestone: complete all sign up function with css, js
	- cost: 2h 
	- Estimated finished date: 10.31

2. Login page *Implemented by Dan*

	- Have completed static content
	- Milestone: complete all login function with css, js
	- cost: 2h 
	- Estimated finished date: 10.31

3. Home page *Implemented by Dan*

	- Have completed static content
	- Milestone: complete all search city function with css, js
	- cost: 2h 
	- Estimated finished date: 10.31

4. views functions about user interactions (login, comment, like, favorite list, etc.) *Implemented by Ziqi, Dan*

	- timeline: under processing, 
	- cost: 5h (coding + testing)
	- Estimated finished date: 11.5
	
## Data service (In charge: ziqi liu)
### detail
due to performance reason and some api calling constrain, we decide to cache some data in database (i.e, pre-fetch the data using scrapy).

Basically, our data consist of three categories: 

* block statistic (population, education, income, etc.)
* crime statistic
* google places data.

Also, we need to design an algorithm to calculate the scores for recommendation according to user's preference.

### Task

1. pre-fetch block statistic data from factfinder. *Implemented by Ziqi*

	- timeline: completed
	- cost: 2h for coding. running on GCP about 1 day

2. pre-fetch crime statistic data from spotcrime *Implemented by Ziqi*

	- timeline: still under processing
	- cost: 2h for coding. running time depends on API call constrain
	- additional info: due to the api calling constrain, the scrapy runs slowly, and we need to double check the data isn't corrupted.
	- Estimated finished date: 11.2

3. pre-fetch google places data *Implemented by Ziqi*

	- timeline: haven't started yet, will begin next week
	- cost: 1h for coding. running time depends on API call constrain
	- additional info: we need to discuss how to feed api data according to map area split
	- Estimated finished date: 11.2

4. ranking scores algorithm design *Implemented by Ziqi*

	-  timeline: completed
	-  cost: 2h
	-  additional info: might be adjusted afterwards

5. algorithm mapping radius-based api data into block area in map *Implemented by Ziqi, David*

	- timeline: still under processing
	- cost: estimated 10h
	- additional info: work together with David
	- Estimated finished date 11.6

### issue
the main challenge we're facing now is that how to map radius-based api data into block area in the map. Can only make a approximation, but we want to do it as reasonble as possible.

## Dashboard Service (In charge: ziqi liu)

### detail
provide basic backend views to enable user interaction. and dashboard data stream

### Task

1. views functions provide dash board data stream *Implemented by David, Ziqi*

	- timeline: under processing
	- cost: 8h (estimated, coding + testing)
	- additional info: need further discussion about map area split
	- Estimated finished date: 11.10

## Map Service (In charge: Dan Hou)
### detail

Show the map to the user and allow user place pin. Show the score to the user

1. Map page *Implemented by Dan, David*
	- Have completed basic wireframe
	- Milestone: complete showing block function with css, js
	- cost: 4h 
	- Estimated finished date: 11.4

2. views functions to identifuy the region user click *Implemented by David*

	- timeline: under processing, 
	- Milestone: receive the user click and translate the cordinate to the region
	- cost: 8h (estimated, coding + testing)
   - Estimated finished date: 10.31
  
## Recommendation Service (In charge: Wai Dai)

1. Recommendation page *Implemented by Dan*
	- Have completed basic framework
	- Milestone: complete prototype with css, js. Users can set their preference
	- cost: 4h 
	- Estimated finished date: 11.4
	
## Testing (In charge: Wai Dai)
### detail

Support the unit test and continupus integration

1. Travis Integration *Implemented by David*

	- Integrate github project with Travis-CI
	- Milestone: Finish integration
	- cost: 4h 
	- Estimated finished date: 10.31


