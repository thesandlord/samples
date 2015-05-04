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

from gcloud import datastore
from gcloud import exceptions
import curses
import os
import time

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"
os.environ["GCLOUD_TESTS_PROJECT_ID"] = "YOUR_RPOEJCT_ID_HERE"
os.environ["GCLOUD_TESTS_DATASET_ID"] = os.environ["GCLOUD_TESTS_PROJECT_ID"]
datastore.set_default_dataset_id(os.environ["GCLOUD_TESTS_DATASET_ID"])

screen = curses.initscr()
curses.noecho()
curses.curs_set(0)
screen.keypad(1)

user_email = ""

def get_stories(start_page = 0):
    stories_per_page = 5
    screen.clear()
    screen.addstr(1, 0, "Select which story you want by typing in the number, use the left and right arrow keys to navigate pages, or type 'q' to return to the main page")
    if user_email != "":
        screen.addstr(0, 0, "Logged In With Account: " + user_email)
    else:
        screen.addstr(0, 0, "Not Logged In")
    query = datastore.Query(kind='Story', order=["-timestamp"])
    stories = list(query.fetch(limit=stories_per_page, offset=start_page))
    links = {}
    for i in range(len(stories)):
        links[ord(str(i+1))] = stories[i].key.id_or_name
        screen.addstr(i+2, 0, str(i+1) + ") " + stories[i]["title"])
    screen.refresh()
    
    func_to_run = {}
    while True:
        event = screen.getch()
        if event == ord("q"):
            func_to_run["func"] = start
            func_to_run["params"] = None
            break
        elif links.get(event) != None:
            func_to_run["func"] = get_story
            func_to_run["params"] = {"id":links.get(event), "start_page":start_page, "start_comment":0}
            break
        elif event == curses.KEY_LEFT:
            func_to_run["func"] = get_stories
            func_to_run["params"] = max(0,start_page-stories_per_page)
        elif event == curses.KEY_RIGHT:
            func_to_run["func"] = get_stories
            if len(stories) == stories_per_page:
                func_to_run["params"] = start_page+stories_per_page
            else:
                func_to_run["params"] = start_page
    run_func(func_to_run)
        
def get_story(obj):
    comments_per_page = 5
    screen.clear()
    screen.addstr(0, 0, "Use the up and down arrow keys to navigate comments, type 'p' to post a new comment, or type 'q' to return to the list of stories")
    key = datastore.Key("Story", obj["id"])
    story = datastore.get([key])
    if len(story) > 0:
        screen.addstr(1, 0, "Title: " + story[0]['title'])
        screen.addstr(2, 0, "URL: " + story[0]['url'])
        screen.addstr(3, 0, story[0]['text'])
        screen.addstr(4, 0, "Comments: ")
        query = datastore.Query(kind='Comment', filters=[('storyid', '=', obj["id"])], order=['timestamp'])
        comments = list(query.fetch(limit=comments_per_page, offset=obj["start_comment"]))
        for i in range(len(comments)):
            screen.addstr(i+5, 0, str(i+1) + ". " + comments[i]["text"] + " - " + comments[i].key.parent.id_or_name)
        screen.refresh()
        
        func_to_run = {}
        while True:
            event = screen.getch()
            if event == ord("q"):
                func_to_run["func"] = get_stories
                func_to_run["params"] = obj["start_page"]
                break
            elif event == ord("p"):
                func_to_run["func"] = post_new_comment
                func_to_run["params"] = obj
                break
            elif event == curses.KEY_UP:
                func_to_run["func"] = get_story
                obj["start_comment"] = max(0, obj["start_comment"]-comments_per_page)
                func_to_run["params"] = obj
            elif event == curses.KEY_DOWN:
                func_to_run["func"] = get_story
                if len(comments) == comments_per_page:
                    obj["start_comment"] = obj["start_comment"]+comments_per_page
                func_to_run["params"] = obj
                break   
        run_func(func_to_run)
        
    else:
        start()
        
def get_my_comments():
    screen.clear()
    if user_email != "":
        screen.addstr(0, 0, "Type 'q' to return to the main page")
        query = datastore.Query(kind='Comment', ancestor=datastore.Key("User", user_email))
        comments = list(query.fetch())
        links = {}
        for i in range(len(comments)):
            links[ord(str(i+1))] = comments[i]["storyid"]
            screen.addstr(i+2, 0, str(i+1) + ") " +comments[i]["text"])
        screen.refresh()
        
        func_to_run = {}
        while True:
            event = screen.getch()
            if event == ord("q"):
                func_to_run["func"] = start
                func_to_run["params"] = None
                break
            elif links.get(event) != None:
                func_to_run["func"] = get_story
                func_to_run["params"] = {"id":links.get(event), "start_page":0, "start_comment":0}
                break
        run_func(func_to_run)
        
    else:
        screen.addstr(0,0,"You Need To Be Logged In To View Your Comments!")
        screen.refresh()
        time.sleep(2)
        start()
        
def post_new_story():
    screen.clear()
    title = get_input(0, 0, "Title:")
    url = get_input(2, 0, "URL:")
    if user_email != "":
        if len(title) > 0 and len(url) > 0:
            text = get_input(4, 0, "Text:")
            new_story = datastore.Entity(key=datastore.Key('Story'))
            new_story['title'] = title
            new_story['url'] = url
            new_story['text'] = text
            new_story['timestamp'] = unicode(time.strftime("%s", time.gmtime()))
            datastore.put([new_story])
            screen.addstr(6,0,"Posted Story")
        else:
            screen.addstr(6,0,"Could Not Post Incomplete Story")
    else:
        screen.addstr(6,0,"You Need To Be Logged In To Post A Story")
    screen.refresh()
    time.sleep(2)
    start()
    return
    
def post_new_comment(obj):
    screen.clear()
    if user_email != "":
        comment = get_input(0, 0, "Comment:")
        if len(comment) > 0 :
            new_comment = datastore.Entity(key=datastore.Key('Comment', parent=datastore.Key('User',user_email)))
            new_comment['text'] = comment
            new_comment['storyid'] = obj["id"]
            new_comment['timestamp'] = unicode(time.strftime("%s", time.gmtime()))
            datastore.put([new_comment])
            screen.addstr(2,0,"Posted Comment")
        else:
            screen.addstr(2,0,"Could Not Post Incomplete Comment")
    else:
        screen.addstr(0,0,"You Need To Be Logged In To Post A Comment!")
    screen.refresh()
    time.sleep(2)
    get_story(obj)
    return

def login():
    screen.clear()
    email = get_input(0, 0, "Email:").lower()
    if len(email) > 0:
        key = datastore.Key('User', email)
        user = datastore.get([key])
        if len(user) > 0:
            global user_email
            user_email = user[0]['email']
            screen.addstr(2,0,"Login Complete " + user_email)
        else:
            screen.addstr(2,0,"Account Not Found, Please Create An Account!")
    screen.refresh()
    time.sleep(2)
    start()

def new_account():
    screen.clear()
    email = get_input(0, 0, "Type in your Email:").lower()
    if len(email) > 0:
        key = datastore.Key('User', email) #use the email as the key
        user = datastore.get([key])
        if len(user) < 1:
            name = get_input(2, 0, "Type in your Full Name:").lower()
            new_user = datastore.Entity(key=key)
            new_user['full_name'] = name
            new_user['email'] = email
            datastore.put([new_user])
            global user_email
            user_email = email
            screen.addstr(4,0,"Created Account For: " + email)
        else:
            screen.addstr(2,0,"Account Already Exists For " + email)
    screen.refresh()
    time.sleep(2)
    start()

def main():
    start()
    while True:
        event = screen.getch()
        if event == ord("q"): break
        elif event == ord("l"): login()
        elif event == ord("n"): new_account()
        elif event == ord("s"): get_stories()
        elif event == ord("p"): post_new_story()
        elif event == ord("m"): get_my_comments()
    curses.endwin()

def start():
    screen.clear()
    screen.addstr(0, 0, "Type 'l' to login, 'n' to make a new account, 's' to list stories, 'p' to post a new story, 'm' to see your comments, and 'q' to quit")

def get_input(r, c, prompt_string):
    curses.echo()
    screen.addstr(r, c, prompt_string)
    screen.refresh()
    input = screen.getstr(r + 1, c, 100)
    curses.noecho()
    return unicode(input)

def run_func(func_to_run):
    if func_to_run["params"] == None:
        func_to_run["func"]()
    else:
        func_to_run["func"](func_to_run["params"])

if __name__ == "__main__":
    main()