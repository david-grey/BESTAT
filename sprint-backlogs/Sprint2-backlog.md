## User service (In charge: Dan Hou)

1. Email server *Implemented by David*

	- Have completed static content
	- Milestone: callow user to receive email from our website
	- cost: 2h 
	- Estimated finished date: 11.10

2. Third party login *Implemented by David*
        - Allow user to login with Google
	- Milestone: finish the integrateion
	- cost: 2h 
	- Estimated finished date: 11.10
## Data service (In charge: ziqi liu)
### detail
in this phase, we've collect the data for 3 cities, Newyork, Chicago and Pittsburgh. Every thing works fines. So in next phase we will automate this process, i.e, building a data pipeline. 


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
	- cost: 3h for coding. running time depends on API call constrain

3. pre-fetch google places data *Implemented by Ziqi*

	- timeline: haven't started yet, will begin next week
	- cost: 2h for coding. running time depends on API call constrain

as mentioned above, crime and google place data are huge, and depend on the city. We're building the automated process. The estimated finish date is still unknown. But we coulud expect that we might collect data of most big city next phase.


## Dashboard Service (In charge: ziqi liu)

### detail
provide basic backend views to enable user interaction. and dashboard data stream

### Task

1. views functions provide dash board data stream *Implemented by David, Ziqi*

	- timeline: under processing
	- cost: 8h (estimated, coding + testing)
	- Estimated finished date: 11.15
2. Miscellaneous frontend enhancement such as picture and some score visulization  *Implemented by David, Dan*

	- timeline: under processing
	- cost: 4h 
	- Estimated finished date: 11.15
3. User input and validations  *Implemented by David, Dan*

	- timeline: under processing
	- cost: 4h 
	- Estimated finished date: 11.15
## Map Service (In charge: Dan Hou)
### detail

Show the map to the user and allow user place pin. Show the score to the user

1. Add the link to the dashboard page for the region *Implemented by Dan, David*
	- user can link to the dashboard
	- Milestone: complete the js and views 
	- cost: 4h 
	- Estimated finished date: 11.15

  
## Recommendation Service (In charge: Wei Dai)

### Task
1. ranking scores algorithm design *Implemented by Ziqi*

	-  timeline: completed
	-  cost: 2h
	-  additional info: might be adjusted afterwards

2. algorithm mapping radius-based api data into block area in map *Implemented by Ziqi, David*

	- timeline: finished
	- cost: estimated 10h
	- additional info: work together with David

3. user customized preference ranking  *Implemented by Ziqi, David*
	- timeline: under prcessing
	- cost: estimated 3h
	- estimated finished data: 11.11
	
4. user input and frontend  *Implemented by Dan, David*
	- timeline: under prcessing
	- cost: estimated 3h
	- estimated finished data: 11.20
	
## Testing (In charge: Wei Dai)
### detail

Support the unit test and continuous integration

1. Deployment Integration *Implemented by David*

	- Built auto deployment with Jenkins
	- Milestone: Finish integration
	- cost: 4h 
	- Estimated finished date: 11.15


