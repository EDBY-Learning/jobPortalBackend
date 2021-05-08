from django.test import TestCase
import requests
# Create your tests here.
# category_description, notice_heading, notice_text, notice_file
data = {"school":"authority",
       "city":"Late fees meeting check rollback",
       "positions":"blah blah",
       "subjects":"asfdgh",
       'token':"AKKA_3"}

file = open('urls.py','r')
res = requests.post('http://127.0.0.1:8000/job/add_job',data=data,files={'file':file})
print(res.content)