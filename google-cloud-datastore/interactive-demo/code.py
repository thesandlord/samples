# Welcome to the Datastore Demo! (hit enter)
# We're going to walk through some of the basics...
# Don't worry though. You don't need to do anything, just keep hitting enter...

#	Copyright 2015, Google, Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#Import libraries
from gcloud import datastore
import os
import time

#The next few lines will set up your environment variables
#Replace "YOUR_RPOEJCT_ID_HERE" with the correct value in code.py
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"

projectID = "YOUR_RPOEJCT_ID_HERE"

os.environ["GCLOUD_TESTS_PROJECT_ID"] = projectID
os.environ["GCLOUD_TESTS_DATASET_ID"] = projectID
datastore.set_default_dataset_id(projectID)

#Let us build a message board / news website

#First, create a fake email for our fake user
email = "me@fake.com"

#Now, create a 'key' for that user using the email
user_key = datastore.Key('User', email)
print( user_key )

#Now create a entity using that key
new_user = datastore.Entity( key=user_key )
print( new_user )

#Add some fields to the entity

new_user["name"] = unicode("Iam Fake")
new_user["email"] = unicode(email)
print( new_user )

#Push entity to the Cloud Datastore
datastore.put( new_user )

#Get the user from datastore and print
print( datastore.get(user_key) )

#Make a new incomplete key for the story
#datastore will make a unique id automatically
story_key = datastore.Key( "Story" )
new_story = datastore.Entity( key = story_key )

#Add some fields
new_story["url"] = unicode("cloud.google.com")
new_story["title"] = unicode("Google is an awesome cloud provider")
new_story["text"] = unicode("Check out this cool website I found for Cloud Stuff!")
new_story['timestamp'] = unicode(time.strftime("%s", time.gmtime()))
print( new_story )

#Push entity to the Cloud Datastore
datastore.put( new_story )

#Query for the stories
#This query is eventually consistant
query = datastore.Query(kind='Story', order=["-timestamp"])
results = list( query.fetch() )
print( results )

#Make another story
new_story = datastore.Entity( key = datastore.Key("Story") )
new_story["url"] = unicode("blog.sandeepdinesh.com")
new_story["title"] = unicode("Interesting Blog")
new_story["text"] = unicode("This is a pretty cool blog I write. Check it out!")
new_story['timestamp'] = unicode(time.strftime("%s", time.gmtime()))
datastore.put( new_story )

#Query for the stories
results = list(query.fetch())
print( results )

#Lets add a comment to the first story

#Get the id from the first story
story = results[0]
story_id = story.key.id_or_name
print( story_id )

#Create the comment
#The ancestor (parent) is the user
comment_key = datastore.Key('Comment', parent=user_key)
new_comment = datastore.Entity( key=comment_key )
new_comment['text'] = unicode("Cool story bro")
new_comment['storyid'] = unicode(story_id)
new_comment['timestamp'] = unicode(time.strftime("%s", time.gmtime()))
print( new_comment )

#Push comment to datastore
datastore.put( new_comment )

#Get the id from the second story
story = results[1]
story_id = story.key.id_or_name
print( story_id )

#Create another comment
new_comment = datastore.Entity( key=datastore.Key('Comment', parent=user_key) )
new_comment['text'] = unicode("Wow. Much Awesome. So Rad.")
new_comment['storyid'] = unicode(story_id)
new_comment['timestamp'] = unicode(time.strftime("%s", time.gmtime()))
print( new_comment )

#Push comment to datastore
datastore.put( new_comment )

#Query for all comments
query = datastore.Query( kind='Comment', order=["timestamp"] )
results = list( query.fetch() )
print( results )

#Query for comments on a single story
query = datastore.Query( kind='Comment', filters=[( 'storyid', '=', unicode(story_id) )], order=["timestamp"] )

#Query will fail without a joint index on storyid and timestamp!

#Run Query
results = list( query.fetch() )
print( results )

#Let's make a new user and comment on the same story
email = "msfake@fake.com"
second_user = datastore.Entity( key=datastore.Key('User', email) )
second_user["name"] = unicode("Shesa Fakealso")
second_user["email"] = unicode(email)
datastore.put( second_user )

new_comment = datastore.Entity( key=datastore.Key('Comment', parent=datastore.Key('User', email) ) )
new_comment['text'] = unicode("Boring story :( ")
new_comment['storyid'] = unicode(story_id)
new_comment['timestamp'] = unicode(time.strftime("%s", time.gmtime()))
datastore.put( new_comment )

#Query again
query = datastore.Query( kind='Comment', filters=[( 'storyid', '=', unicode(story_id) )], order=["timestamp"] )
results = list( query.fetch() )
print( results )

#Perform strongly consistant query
#Use the user_key as the ancestor to get the users comments
query = datastore.Query( kind='Comment', ancestor=user_key )
results = list( query.fetch() )
print( results )

#Thats it!
