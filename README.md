CollaTo Open source
=======

###CollaTo Project is an approach extending social network data model to promote participant collaboration an approach extending social network data model to promote participant collaboration through collaborative application execution and management.

#####CollaTo Project is developed with Python Django. Follow the steps to create your instance.

     sudo apt-get install python-pip python-dev
     sudo apt-get install python-mysqldb
     sudo apt-get install virtualenv
     sudo apt-get install libmysqlclient-dev
     virtualenv --no-site-packages CollaTo
     cd CollaTo/
     pip install django==1.5.1
     pip install django-endless-pagination  django-jsonfield django-model-utils django-extensions django-autocomplete-light BeautifulSoup django-tastypie mimeparse PIL simplejson
     pip install mysql-python 
     django-admin.py startproject esn
     
     **Change Path to 
          MEDIA_ROOT, STATIC_ROOT, STATICFILES_DIRS, TEMPLATE_DIRS, LOCALE_PATHS
          
     python manage.py syncdb
     python manage.py collectstatic
     
     python manage.py schemamigration roleapp --initial
     python manage.py migrate roleapp
     python manage.py schemamigration notifications --initial
     python manage.py migrate notifications
     python manage.py schemamigration cicu --initial
     python manage.py migrate cicu
     python manage.py schemamigration organizations --initial
     python manage.py migrate organizations
     python manage.py schemamigration responsibilities --initial
     python manage.py migrate responsibilities 
     python manage.py schemamigration applications --initial
     python manage.py migrate applications
     python manage.py schemamigration actstream --initial
     python manage.py migrate actstream 
     python manage.py schemamigration userprofiles --initial
     python manage.py migrate userprofiles 
     python manage.py collectstatic
     
     python manage.py runserver
     **Create users (auth_user/userprofile)
