#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# You can start this by executing it in python:
# python server.py
#
# remember to:
#     pip install flask


import flask
from flask import Flask, request, redirect, url_for, Response
import json
import uuid
app = Flask(__name__)
app.debug = True
anonymous_user = 0

# An example world
# {
#    'a':{'x':1, 'y':2},
#    'b':{'x':2, 'y':3}
# }

class World:
    def __init__(self):
        self.clear()
        
    def update(self, entity, key, value): # allows us to update values in a pre-existing entity
        entry = self.space.get(entity,dict())
        entry[key] = value
        self.space[entity] = entry

    def set(self, entity, data):
        self.space[entity] = data # create a new entity

    def clear(self):
        self.space = dict()

    def get(self, entity):
        return self.space.get(entity,dict())
    
    def world(self):
        return self.space
    
    def replace(self, space):
        self.space = space

# you can test your webservice from the commandline
# curl -v   -H "Content-Type: application/json" -X PUT http://127.0.0.1:5000/entity/X -d '{"x":1,"y":1}' 

myWorld = World()

# I give this to you, this is how you get the raw body/data portion of a post in flask
# this should come with flask but whatever, it's not my project.
def flask_post_json():
    '''Ah the joys of frameworks! They do so much work for you
       that they get in the way of sane operation!'''
    if (request.json != None):
        return request.json
    elif (request.data != None and request.data.decode("utf8") != u''):
        return json.loads(request.data.decode("utf8"))
    else:
        return json.loads(request.form.keys()[0])

@app.route("/")
def hello():
    '''Return something coherent here.. perhaps redirect to /static/index.html '''
    return (redirect(url_for('static', filename='index.html')))

@app.route("/entity/<entity>", methods=['POST','PUT'])
def update(entity):
    '''update the entities via this interface'''
    if request.method == 'POST': #update an existing entity?
        entity_body = flask_post_json()
        for key in entity_body:
            myWorld.update(entity, key, entity_body) #update each key to match the value. If the entity doesn't exist it creates it -> what is the point? allows only a few keys to get updated?

        return Response(json.dumps(myWorld.get(entity)), status=200, mimetype='application/json')
    elif request.method == 'PUT': #add a new entity
        entity_body = flask_post_json()
        myWorld.set(entity, entity_body)
        return Response(json.dumps(myWorld.get(entity)), status=200, mimetype='application/json')

    return Response(status=405)

@app.route("/world", methods=['POST','GET'])    
def world():
    '''you should probably return the world here'''
    if request.method == 'GET':
        return Response(json.dumps(myWorld.world()), status=200, mimetype='application/json')
    elif request.method == 'POST':
        #updates the world object? -> unsure what to do with this
        space = flask_post_json()
        myWorld.replace(space)
        return Response(status=200)
    return Response(status=405)

@app.route("/entity/<entity>")
def get_entity(entity):
    '''This is the GET version of the entity interface, return a representation of the entity'''
    if request.method == 'GET':
        return Response(json.dumps(myWorld.get(entity)), status=200, mimetype='application/json')
    return Response(status=405)

@app.route("/clear", methods=['POST','GET'])
def clear():
    print('HERE')
    '''Clear the world out!'''
    if request.method == 'POST':
        myWorld.clear()
        return Response(json.dumps(myWorld.world()), status=200, mimetype='application/json')
    
    return Response(status=405)

@app.route("/user", methods=['GET'])
def user():
    '''GET the current user val'''
    if request.method == 'GET':
        return Response(json.dumps({"id": str(uuid.uuid4())}), status=200, mimetype='application/json')
    
    return Response(status=405)

if __name__ == "__main__":
    app.run(port=8000)