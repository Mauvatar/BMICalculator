# BMICalculator
#### Video Demo:  <https://youtu.be/NWf2zgcSzYI>
#### Description:
This is my final project called "BMICalculator". This project is a web page which purpose is to calculate your BMI and assign a workout plan depending if your BMI was lower, at, or above a healthy number.
This project contains the main folder called project and within it are 2 subfolders called templates and static aswell as the python files called "app" and "helpers" plus the project database, this readme file and requirements text file.
The static folder contains an ico file that contains a flexing arm emoji that gives the tab a little style for the user experience and the styles.css file which contains some rules of css such as giving style to the navbar; it also gives the picture background for the body
, it also gives an outline to the text in the web page that way it can be read through the changing colors of the background picture it applies to all paragraphs, bold texts, headers 1 through 3 etc.

The templates folder contains all the html used in the web page. It contains layout.html which is the foundation of the html, meaning that the rest of the htmls extend this one to avoid rewriting html code.
Apology.html is used the display the user the respective message of what it is that they did wrong such as an invalid username or password.
There is also the BMI.html which extends layout.html and contains a form which purpose is to accept weight and height as user input and it returns a post request to the /BMI route once the form is submitted.
The index.html is the welcoming part of the web page. It first dynamically welcomes the user by the name which they registered with plus a warm little welcome and introduction to the page right below.
After that it shows a "What you should know?" about the page what is the purpose what just happened and how you can use it. Lastly it thanks the user and shows an image with what is (hopefully) an inspiring message to start the workout.

The login.html is pretty straightforward and similar to the BMI.html because it too accepts two user inputs using a form. It accepts the username and password and sends a post request to the /login route.
Myplan.html is the personalized part of the page which only shows the user the plan/workout that they got depending on the result of their BMI. Using jinja notation it uses an if conditional to check a variable called "Myplan".
This variable changes using some python code (more on that later) and it compares it to three different values: "Stay fit", "Fat loss", "Muscle gain". That way the user will only be shown the workout which corresponds to them.
All the ifs are pretty similar. They contain a different title and video which is clickable and watchable right there on the page instead of redirecting the user to youtube.
Then we have the plan.html which is almost the same as the Myplan.html because this shows the users all of the available workouts/plans there are instead of just the one that they "should" be doing. This allows the users to try or just see the other options.

Moving on to register.html accepts three user inputs. Username, password, and confirm password. On submit it sends a post request to the /register route so that the user registers.
Finally success.html is what the user sees once they have calculated their BMI succefully. it's basically just text letting know the user that their BMI has been succefully updated in the database
plus a text letting them know which plan they got with a link to Myplan.html.

app.py is the main python file for the web page firstly it imports different functions from different libraries such as SQL from cs50, Flask from flask, flask session, werkzeug.security etc. It also imports from another python file called helpers.py
It then starts configuring to make the app a flask app. It makes it so that templates are auto reloaded and it uses the file system instead of cookies for the session. Then it configures the sql from the cs50 library. Right after that it clears the cache from responses.
app.py has 7 routes "/", "/BMI", "/Myplan", "/plan", "/login", "/logout", and "/register". Lets go through them one by one.
"/" is the index route it redirects them to that html and keeps track which user is currently logged in to greet them appropiatley by their name. It only uses get requests.
"/BMI" is the core of the page since this is where the BMI of the user is registered. It accepts post and get requests. While on get it displays the BMI.html which allows the users to input their weight and height so that when they send the post request
this route registers their BMI to the database and picks which plan is best for the user. After that it renders the success.html.
"/Myplan" only accepts get requests and it checks for the users BMI so that Myplan.html shows the plan that was picked for them. It then renders the templat of Myplan.html.
"/plan" is the simplest of them all. It just renders the plan.html which shows the users all the available plans. Naturally it only accepts get requests.
"/login" accepts get and post methods. while on get it only renders the login.html so that the user can input the inputs. While on post it first goes step by step checking if the username and password were typed, if the user exists, and if the password matches the user.
it remembers the user in session and before redirecting to the index page it checks if it's the first time that the user uses the page by checking if there is a BMI value for that current user. If not then they are sent directly to BMI.html so that they enter their data.
otherwise it sends them to the main page.
"/logout" just clears the session and redirects them to the main page which in turn sends them to login.
lastly "/register.html" accepts get and post. While on get it renders the register.html template so that the user can input their data. While on post it checks that the user has actually typed their username and/or password aswell as checking if they
have confirmed their password sueccesfully. The password gets hashed using werkzeug and salted. If everything is fine the user gets registered in the database.

helpers.py has two functions apology and login_required. The apology function helps render the apology.html with the appropiate message of what the user did wrong. the login_required decorates the routes so that if the user has not logged in they cant be used because they will be redirected to the "/login" route.