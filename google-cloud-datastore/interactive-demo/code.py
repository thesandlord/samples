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
import datetime

#The next few lines will set up your connection to Datastore
#Replace "YOUR_RPOEJCT_ID_HERE" with the correct value in code.py
projectID = "smart-spark-93622"

client = datastore.Client.from_service_account_json( json_credentials_path="key.json", dataset_id=projectID )

record_key = client.key('Record', 1234)
record_entity = datastore.Entity(key=record_key,exclude_from_indexes=('RandomFieldName',))

embedded_key = client.key('Data', 2345)
embedded_entity = datastore.Entity(key=embedded_key,exclude_from_indexes=('big_field',))
embedded_entity['field1']='1234'
with open ("code.py", "r") as myfile:
    embedded_entity['big_field']=myfile.read().replace('\n', '')

record_entity['RandomFieldName']=embedded_entity

print(record_entity.exclude_from_indexes)
print(record_entity['RandomFieldName'].exclude_from_indexes)
print(embedded_entity.exclude_from_indexes)
client.put(record_entity)
client.put(embedded_entity)

#Let us build a message board / news website

#First, create a fake email for our fake user
email = "me@fake.com"

#Now, create a 'key' for that user using the email
user_key = client.key('User', email)
print( user_key )

#Now create a entity using that key
new_user = datastore.Entity( key=user_key )
print( new_user )

#Add some fields to the entity

new_user["name"] = unicode("Iam Fake")
new_user["email"] = unicode(email)
print( new_user )

#Push entity to the Cloud Datastore
client.put( new_user )

#Get the user from datastore and print
print( client.get(user_key) )

#Make a new incomplete key for the story
#datastore will make a unique id automatically
story_key = client.key( "Story" )
new_story = datastore.Entity( key = story_key )

#Add some fields
new_story["url"] = unicode("cloud.google.com")
new_story["title"] = unicode("Google is an awesome cloud provider")
new_story["text"] = unicode("Check out this cool website I found for Cloud Stuff!")
new_story['timestamp'] = datetime.datetime.now()
print( new_story )

#Push entity to the Cloud Datastore
client.put( new_story )

#Query for the stories
#This query is eventually consistant
query = datastore.Query( client=client, kind='Story', order=["-timestamp"])
results = list( query.fetch() )
print( results )

#Make another story
new_story = datastore.Entity( key = client.key("Story") )
new_story["url"] = unicode("blog.sandeepdinesh.com")
new_story["title"] = unicode("Interesting Blog")
new_story["text"] = unicode("This is a pretty cool blog I write. Check it out!")
new_story['timestamp'] = datetime.datetime.now()
client.put( new_story )

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
comment_key = client.key('Comment', parent=user_key)
new_comment = datastore.Entity( key=comment_key )
new_comment['text'] = unicode("Cool story bro")
new_comment['storyid'] = unicode(story_id)
new_comment['timestamp'] = datetime.datetime.now()
print( new_comment )

#Push comment to datastore
client.put( new_comment )

#Get the id from the second story
story = results[1]
story_id = story.key.id_or_name
print( story_id )

#Create another comment
new_comment = datastore.Entity( key=client.key('Comment', parent=user_key) )
new_comment['text'] = unicode("Wow. Much Awesome. So Rad.")
new_comment['storyid'] = unicode(story_id)
new_comment['timestamp'] = datetime.datetime.now()
print( new_comment )

#Push comment to datastore
client.put( new_comment )

#Query for all comments
query = datastore.Query(client=client, kind='Comment', order=["timestamp"] )
results = list( query.fetch() )
print( results )

#Query for comments on a single story
query = datastore.Query(client=client, kind='Comment', filters=[( 'storyid', '=', unicode(story_id) )], order=["timestamp"] )

#Query will fail without a joint index on storyid and timestamp!

#Run Query
results = list( query.fetch() )
print( results )

#Let's make a new user and comment on the same story
email = "msfake@fake.com"
second_user = datastore.Entity( key=client.key('User', email) )
second_user["name"] = unicode("Shesa Fakealso")
second_user["email"] = unicode(email)
client.put( second_user )

new_comment = datastore.Entity( key=client.key('Comment', parent=client.key('User', email) ) )
new_comment['text'] = unicode("Boring story :( ")
new_comment['storyid'] = unicode(story_id)
new_comment['timestamp'] = datetime.datetime.now()
client.put( new_comment )

#Query again
query = datastore.Query(client=client, kind='Comment', filters=[( 'storyid', '=', unicode(story_id) )], order=["timestamp"] )
results = list( query.fetch() )
print( results )

#Perform strongly consistant query
#Use the user_key as the ancestor to get the users comments
query = datastore.Query(client=client, kind='Comment', ancestor=user_key )
results = list( query.fetch() )
print( results )

#Thats it!
