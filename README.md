
# README
## Deployment instructions
1. Open command prompt, go to desire directory and run the following command to clone the repository:
```
git clone https://github.com/ak2253/E2EE-project
```
2. Change to directory E2EE-project.
3. Make sure that npm and pip is already installed into your computer
4. Run the following commands
```
npm install
pip install -r requirements.txt
flask db upgrade
```
5.  Create an account on Heroku using the following [link](https://dashboard.heroku.com/).
6. After creating an account, you should be at the app menu. Click on the new button towards the top right and click `create new app`. Name it what ever you want.
7. You should be at the overview menu for your project. Click on the `Configure Add-ons` and type `Heorku Postgres` and confirm to the free option. You should not be paying anything.
8. Once the database has been created, you should be at the page where the database has been created. Click on `Settings` and then `View Credientials...` and there should be a URI link. Keep note of that link for a future step.
9. In the root of the repository, create an .env file and make sure the following variables are in the file
```
DATABASE_URL=[Enter url recieved from step 8]
SECREY_KEY=[Enter long and unguessable key]
```
## Running the App on Heroku
1. Go to your Heroku dashboard and click on the project made from the deployment instructions
2. Add in the apps environment variables by navigating back to Heroku's settings
3. Find 'Config Vars' section and click on  `Reveal Config Vars`
4. Transfer all variables and values from .env file respectively
5. Find 'Buildpacks' on the same page
6. Click on `Add buildpack` and add the following buildpacks in the respective order
```
heroku/python
heroku/nodejs
```
7. Open terminal and go to the directory where the repository is located.
8. Enter the following commands:
```
heroku login -i
heroku git:remote -a [name of project from deployment instructions]
git push heroku master
```
9. Once the last command is finished, there should be a link provided for you to navigate to see your app.
## Running the App Locally
If for some reason the app needs to be ran locally or for testing the app do the following steps:
1.  Have to separate command lines open located the the root directory of the repository.
2. One one command line run `npm start`
3. One the other run `python app.py`
4. Step 2 should lead you to a page where the apps runs
## TODO
- Make webpage responsive to user receiving messages from other users.
- Debug any unexpected issues
- Webpage Styling
