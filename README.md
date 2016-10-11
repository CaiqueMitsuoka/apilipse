# Apilipse
## A API REST do apolipse

First of all, thanks for the oportunity, I've learned a lot with the test. No doubt I'm other programmer after that

Let's get to work!

To build the application I've used Python 2.7, Flask, and MongoDB.

Why Python? Knowledge and philosophy. You guys are going to read my code, so it was on my duty be myself and do the best. Python allow me to do booth of these things.

Why Mongo? Simple, to try it out. I thought since this project is about know who I am, so this choice tells exactly what I'm living right now, trying everything to see what I like, where I can go and what can be done.

### About the code

As the zen of python says, basically the code should speak for itself, so in every line was mas with this in mind, so i've tried to not comment too.

If you have any observation please send me a feedback, I would like to hear, even if a "no" come together. I just want to get better! [Email](mailto:caique.mitsuoka@gmail.com)

### Run, Forest, Run !

If you use python on the machine where the code is going to run I recommend to create a Virtualenv, otherwise the frameworks shouldn't not conflict with anything.

##### Prepare environment:

Install MongoDB and a tutorial can be found [here](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/).

Populate with a test database:

`$ mongoimport --db apilipse --collection survivors --drop --file survivors.json
`

#####

##### Launch server and database:

`$ sudo service mongod start
`

`$ python app.py
`

##### Test:

For inputs and test I made tests on UnitTest.py file. Trade is covered 100%.
But then a friend showed to me Postman and then I've stopped to try to make the wheel again and used it as console.
My test routine was the two test, with postman iterating 20-30 times to make sure everything was stable.

So for inputs please use postman and import the tests.

`$ python UnitTest.py
`


[Miiiiiiaaaun](https://www.youtube.com/watch?v=fhkgNTmrXFY)
