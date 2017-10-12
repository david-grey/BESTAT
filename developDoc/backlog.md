#Project backlog
##User module (Owner Dan Hou)
..*Registration: The users should be able to register with their email and verify its email.
..*Sign in: The users can sign in with their email.
..*Forget password: The users can reset password.
..*Log out: logged-in users can sign out.
..*User can log in with their google account.
..*User need to use Captcha

##Data Service module (Owner Ziqi Liu)
..*Obtain demographic data from US censors.
..*Obtain place data from Google place API. The API call need to be run periodically to update.
..*Obtain data from spot crime API. The API call need to be run periodically to update.
..*Obtain data real time from Google map API
..*Map the data in different granulite to the neighborhood we define.

##Map Service module (Owner Dan Hou)
..*Users can choose city
..*Users can see a map after choosing a city
..*Users can see the neighborhood in the city they choose.
..*Users can place pin on the map
..*Users can see the living index of the point they choose
..*Users can choose multiple places and check the living index without reloading the page(AJAX)

##Dashboard Service module (Owner Ziqi Liu)
..*Users can check details measurements of the place they choose
..*Users can check the user reviews on this neighborhood
..*Users can post reviews in this neighborhood
..*Users can check the trend of a particular neighborhood

##Recommendation Service module (Owner Wei Dai)
..*Users can fill in preferences form.
..*Users can edit preferences form.
..*Users can check the recommended region in the city.
..*Users can check the neighborhood details by clicking the top recommendations.
..*Users can give feed backs on the recommendation (like, dislike)
..*The system will use the user generated contents (comments, feedbacks)

##Testing (Owner: Wei Dai)
..*Unit test: every version will be tested automatically before deploying
..*Continuous Integration: The project will be integrated with Travis to automate the testing.

