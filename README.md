# [DEPRECATED] BLZ - US Congress Visibility App
This project is no longer actively maintained and is not live. The repository is preserved for reference and learning purposes.

<a href="https://www.python.org/" title="Python"><img src="https://github.com/tomchen/stack-icons/blob/master/logos/python.svg" alt="Python" width="21px" height="21px"></a> &nbsp;<a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript" title="JavaScript"><img src="https://github.com/tomchen/stack-icons/blob/master/logos/javascript.svg" alt="JavaScript" width="21px" height="21px"></a>&nbsp; <a href="https://git-scm.com/" title="Git"><img src="https://github.com/tomchen/stack-icons/blob/master/logos/git-icon.svg" alt="Git" width="21px" height="21px"></a>&nbsp; <a href="https://www.w3.org/TR/html5/" title="HTML5"><img src="https://github.com/tomchen/stack-icons/blob/master/logos/html-5.svg" alt="HTML5" width="21px" height="21px"></a>&nbsp; <a href="https://www.w3.org/TR/CSS/" title="CSS3"><img src="https://github.com/tomchen/stack-icons/blob/master/logos/css-3.svg" alt="CSS3" width="21px" height="21px"></a>&nbsp; <a href="https://code.visualstudio.com/" title="Visual Studio Code"><img src="https://github.com/tomchen/stack-icons/blob/master/logos/visual-studio-code.svg" alt="Visual Studio Code" width="21px" height="21px"></a> &nbsp;<a href="https://www.npmjs.com/package/axios" title="AXIOS"><img src="readme_files/axios.png" alt="AXIOS" width="21px" height="21px"></a> &nbsp;<a href="https://www.heroku.com/" title="Heroku"><img src="readme_files/heroku.jpeg" alt="Heroku" width="21px" height="21px"></a> &nbsp;<a href="https://www.postgresql.org/" title="Postgres"><img src="readme_files/postgres.png" alt="Postgres" width="21px" height="21px"></a> &nbsp;<a href="https://getbootstrap.com/" title="Bootstrap"><img src="https://github.com/tomchen/stack-icons/blob/master/logos/bootstrap.svg" alt="Bootstrap" width="21px" height="21px"></a> &nbsp;<a href="https://fontawesome.com/" title="FontAwesome"><img src="readme_files/fontawesome.png" alt="FontAwesome" width="21px" height="21px"></a> &nbsp;<a href="https://jquery.com/" title="jQuery"><img src="https://github.com/tomchen/stack-icons/blob/master/logos/jquery-icon.svg" alt="jQuery" width="21px" height="21px"></a> &nbsp;<a href="https://flask.palletsprojects.com/en/1.1.x/" title="Flask"><img src="readme_files/flask_logo_white_background.png" alt="Flask" width="40px" height="21px"></a> &nbsp;<a href="https://www.sqlalchemy.org/" title="Git"><img src="readme_files/sql_alchemy_logo.jpeg" alt="WTForms" width="70px" height="21px"></a> &nbsp;<a href="https://wtforms.readthedocs.io/en/2.3.x/#" title="WTForms"><img src="readme_files/wtforms.png" alt="SQLAlchemy" width="80px" height="21px"></a>


## Table of Contents

* [About](https://github.com/erikamanning/capstone1#about)
* [Installation](https://github.com/erikamanning/capstone1#installation)
* [User Flows](https://github.com/erikamanning/capstone1#user-flows)
* [API](https://github.com/erikamanning/capstone1#api)



## About

### <div align='center'>Did you know that every year US Congress introduces an average of 11,000 bills? <sup>[</sup>[<sup>1</sup>](https://www.ndpanalytics.com/45-years-of-congress-bills)<sup>,</sup>[<sup>2</sup>](congress.gov)<sup>]</sup></div>


<br>   

### <div align='center'>........ </div>  
<br>  

### <div align='center'>:mag: How many have you read? </div>  


### <div align='center'>........ </div>  

<br>  

It can be difficult to keep on top of all national legislation, but BLZ makes it easier. With the BLZ app, you can access a dashboard which shows you all your state's senators and representatives, so you can see what legislation they have sponsored recently. You can also browse legislation by policy area and specify a date range that you would like to search by. You can easily save bills to your dashboard so you can keep tabs on them, and quickly access information about their most recent updates. You can also move from any bill on the app, to the bill's page on the official congress website so you can learn more.


## Installation

#### Before You Begin
You will need python3 and pip3 installed for this project. You will also need to setup a Postgres Database for the app.


#### Installation Instructions

1. Get a free API key from ProPublica
    ```sh
    https://www.propublica.org/datastore/api/propublica-congress-api
    ```

2. Clone the repo.
    ```sh
    https://github.com/erikamanning/capstone1.git
    ```

3. Create a virtual environment in the project directory.
    ```sh 
    $ python3 -m venv venv
    ```

4. Start the virtual environment.
    ```sh
    $ source venv/bin/activate
    ```

5. Install required packages.
    ```sh
    $ pip3 install requirements.txt
    ```

6. Open the secrets.py file and add your API key and Flask Secret Key in the fields specified below. 
   _**Make sure to add secrets.py tp your .gitignore so your personal API key doesn't get shared accidentally.**_
   
    <sub> In *secrets.py*</sub>
    ```sh
    API_SECRET_KEY = os.environ.get('SECRET_API_KEY', '##NOT A KEY##')
    FLASK_SECRET_KEY = os.environ.get('SECRET_KEY', '##NOT A KEY##')
    ```
<br>  

_**You will need to set up a postgres database for this application. Once that is done you can move to the next step.**_

<br>  

7. Initialize the database.
    ```sh
    $ flask init_app
    ```

8. Set the environment to development mode.
    ```sh
    $ export FLASK_ENV=development 
    ```

9. Run the app.
    ```sh 
    $ flask run
    ```

10. Open web browser and run the app on the port for your server.


## User Flows

### Landing Page
![Landing Page](readme_files/landing_page_full_size.png)

---

### User Flow: View State Legislators and Sponsored Bills
![User Flow 3](readme_files/User_flow_3.png)

---

### User Flow: Browse and Save Bills to Dashboard.
![User Flow 1](readme_files/User_flow_1.png)

## API
This project owes much to [ProPublica's Congress API](https://projects.propublica.org/api-docs/congress-api/). All congressional data was obtained through the ProPublica Congress API.

![ProPublica Logo](readme_files/propublica_logo.jpg)


