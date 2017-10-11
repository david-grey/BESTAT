## Implementation
our data models are implemented with django built-in models, with SQL as database.(This is only a draft design, we might shift to MongoDB if it has better performance regarding spatial data.)

## data and APIs
most of our data of models will be collected from different api or scrapy wrapper. Therefore the fields in models will correspond to our APIs. See api.md for more details