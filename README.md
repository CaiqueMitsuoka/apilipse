# Apilipse
## A API REST do apolipse

First of all, thanks for the oportunity, I've learned a lot with the test. No doubt I'm other programmer after that

Let's get to work!

To build the application I've used Python 2.7, Flask, and MongoDB.

Why Python? Knowledge and philosophy. You guys are going to read my code, so it was on my duty be myself and do the best. Python allow me to do booth of these things.

Why Mongo? Simple, to try it out. I thought since this project is about know who I am, so this choice tells exactly what I'm living right now, trying everything to see what I like, where I can go and what can be done.

### About the code

As the zen of python says, basically the code should speak for itself, so in every line was mas with this in mind, so i've tried to not comment too.

### Run, Forest, Run !

If you use python on the machine where the code is going to run I recommend to create a Virtualenv, otherwise the frameworks shouldn't not conflict with anything.

##### Prepare environment:

Install MongoDB and a tutorial can be found [here](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/).

`$ sudo service mongod start
`

`$ mongoimport --db apilipse --collection survivors --drop --file survivors.json
`

`$ sudo pip install flask
`

`$ sudo pip install pymongo
`


##### Launch server:

`$ python __init__.py
`

##### Test:

`$ python UnitTest.py
`
