to run the website do the following in the command line commands assuming the virtual enviroment is set up

pip install -U django-registration-redux==1.4

python manage.py makemigrations gradinator
python manage.py migrate

python populate_gradinator.py populate

to run admin you need to set up a superuser account so 

python manage.py createsuperuser

then 

python manage.py runserver



What still needs done? 21/03/2018 10.42

make the website look decent
unit tests
search functionality
slides for the presentation
anything else that comes up