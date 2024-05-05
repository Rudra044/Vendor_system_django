for setting up:
prerequisites:
 you should have my sql command downloaded in your system else change database seeting to the default django orm

 run following commands:
 virtualenv my_env
 source myenv/Scripts/activate
 install django
 install django_rest_framework
 install django_rest_framework_simplejwt
 install mysqlclient
 django admin startproject vendor_mangement .
 py  manage.py startapp vendor
 py manage.py startapp product(add both urls.py and serializer.py in both the folders)

 after this u can copy the code on your respective files
 u can run py manage.py test for checking the above code

 other u can check with the following command:
 py manage.py test





