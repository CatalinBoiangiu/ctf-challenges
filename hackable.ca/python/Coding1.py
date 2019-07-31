import regex
import requests
from bs4 import BeautifulSoup

# define consts
server_name = 'https://hackable.ca'
ctf_url = 'http://coding.hackable.ca:8080'
email = 'EMAIL'
password = 'PASSWORD'

payload = {
    'email': email,
    'password': password
}

ctf_payload = {
    'sortedlist': ''
}

# login
with requests.Session() as sess:
    res = sess.get(server_name + '/login')
    signin = BeautifulSoup(res._content, 'html.parser')
    payload['_token'] = signin.find('input', {'name': '_token'})['value']
    res = sess.post(server_name + '/login', data=payload)
################# LOG #################
if res.status_code == 200:
    print('Login success!')
else:
    print('Login failed!')
#######################################

# solve ctf
res = sess.get(ctf_url)
page = BeautifulSoup(res._content, 'html.parser')
pageContent = str(page)
indexStart = pageContent.find('Unsorted:') + 10
indexEnd = pageContent.find('<br/>')
unsorted = pageContent[indexStart:indexEnd]
array = regex.findall(("[a-z]+"), unsorted)
array.sort()
array_prepared = str(array)
array_prepared = array_prepared.replace("'", '"')
array_prepared = array_prepared.replace(" ", '')
################# LOG #################
print('\n')
print('OG array:')
print(array)
print('\n')
print(array_prepared)
print('\n')
#######################################

# send answer
ctf_payload['sortedlist'] = array_prepared
res = sess.post(ctf_url, data=ctf_payload)
flag = res.content
################# LOG #################
print('Status code:')
print(res.status_code)
print('\n')
#######################################

# get flag
print('Flag:')
print(flag)
