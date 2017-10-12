# API wrapper

## factfinder wrapper
`	def fetch(zip_code):`

* :param zip_code:
* :return: dict

#### field of dict
* POPULATION // population number
* AGE // avg age
* EDUCATION // Educational Attainment: Percent high school graduate or higher
* HOUSING // Total housing units
* INCOME // avg income
* POVERTY // Individuals below poverty level


## spotcrime wrapper

### 0. type of crime

* Theft
* Robbery
* Burglary
* Vandalism
* Shooting
* Arson
* Arrest
* Assault
* Other


### 1. neighborhood

`neighbor = Neiborhood(name='Garfield',
                 url='/pa/pittsburgh/garfield')`
#### field
* `neighbor.name`
* `neighbor.data` # *dict containing crime data in last six month, where key is type of crime*


### 2. city
`city = City(state='pa', city='pittsburgh')`

* `city.state`
* `city.city`
* `city.neighbors` # *list of neighborhood instance*


### 3. crime
`class Crime:`

`def fetch(self, lat, lon, radius=0.006):` # *return a list of crime records, each crime records is a dict*

* cdid
* type
* date
* address
* link
* lat
* lon

`def crime_index(self, lat, lon, radius=0.06):` # *return crime_index, caculated by crime. the higher the worse*
    
## Google Place
`googleplace = GooglePlace()`

`def search_place(self, lat, lon, place_type, radius=1000):` *# return a list of dict*

    