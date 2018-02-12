# # django-paynow-exampe
This is an example of how to intergrate a django payment system with Paynow API (http://www.paynow.co.zw/)

I used the information found on the Paynow site in this [document](https://www.paynow.co.zw/Content/Paynow%203rd%20Party%20Site%20and%20Link%20Integration%20Documentation.pdf)


This application was implemented to run on [Heroku.com](https://heroku.com/) using the [Getting Started with Python on Heroku](https://devcenter.heroku.com/articles/getting-started-with-python) article - check it out.

## Running Locally

Make sure you have Python [installed properly](http://install.python-guide.org).  
```sh
$ git clone https://github.com/charle-k/django-paynow-example.git
$ cd django-paynow-example

$ pip install -r requirements.txt

$ python manage.py migrate

$ python manage.py runserver 
```

For you to start processing payments add your Paynow Id and Key to settings.py in paysys folder. Once you are done create a new user to login with.

```sh
$ python manage.py createsuperuser
```

You can now run the test server and login with hte details of the user u created.

```sh
$ python manage.py runserver 
```

You can now start processing payments by entering amount, celllphone number and ref in the form. Click "Make Payment" to start  the process.





Your app should now be running on [127.0.0.1:8000](http://127.0.0.1:8000/).

## Deploying to Heroku
Ensure you have installe the [Heroku Command Line Interface (CLI)](https://toolbelt.heroku.com/) 
To store information you have to provision a database. The Heroku Postgres Addon is a good option



## Documentation

For more information about using Python on Heroku, see these Dev Center articles:

- [Python on Heroku](https://devcenter.heroku.com/categories/python)


For more information about using Paynow you can visit the Developers page on their site

- [Paynow Developer Documentation](https://www.paynow.co.zw/Home/Developers)