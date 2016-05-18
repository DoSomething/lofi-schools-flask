LOFI School Finder App
======================

Running on Heroku
----------------------------
Install the Heroku Toolbelt

Download and install the [Heroku Toolbelt](https://toolbelt.heroku.com/) or learn more about the Heroku Command Line Interface.

If you haven't already, log in to your Heroku account and follow the prompts to create a new SSH public key.

    $ heroku login

Clone the repository

Use Git to clone lofischools's source code to your local machine.

    $ heroku git:clone -a lofischools
    $ cd lofischools

Deploy your changes

Make some changes to the code you just cloned deploy them to Heroku using Git.

    $ git add .
    $ git commit -am "make it better"
    $ git push heroku master


