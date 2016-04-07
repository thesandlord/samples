/*
Copyright 2016 Google Inc. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

'use strict';

var express = require('express');
var fs = require('fs');
var util = require('util');
var mime = require('mime');
var multer = require('multer');
var upload = multer({dest: 'uploads/'});

// Set up auth
var gcloud = require('gcloud')({
  keyFilename: 'key.json',
  projectId: '<YOUR-PROJECT-ID-HERE>'
});

var vision = gcloud.vision();

var app = express();

// Simple upload form
var form = '<!DOCTYPE HTML><html><body>' +
  "<form method='post' action='/upload' enctype='multipart/form-data'>" +
  "<input type='file' name='image'/>" +
  "<input type='submit' /></form>" +
  '</body></html>';

app.get('/', function(req, res) {
  res.writeHead(200, {
    'Content-Type': 'text/html'
  });
  res.end(form);
});

// Get the uploaded image
// Image is uploaded to req.file.path
app.post('/upload', upload.single('image'), function(req, res, next) {

  // Choose what the Vision API should detect
  // Choices are: faces, landmarks, labels, logos, properties, safeSearch, texts
  var types = ['labels'];

  // Send the image to the Cloud Vision API
  vision.detect(req.file.path, types, function(err, detections, apiResponse) {
    if (err) {
      res.end('Cloud Vision Error');
    } else {
      res.writeHead(200, {
        'Content-Type': 'text/html'
      });
      res.write('<!DOCTYPE HTML><html><body>');

      // Base64 the image so we can display it on the page
      res.write('<img width=200 src="' + base64Image(req.file.path) + '"><br>');

      // Write out the JSON output of the Vision API
      res.write(JSON.stringify(detections, null, 4));

      // Delete file (optional)
      fs.unlinkSync(req.file.path);

      res.end('</body></html>');
    }
  });
});

app.listen(8080);
console.log('Server Started');

// Turn image into Base64 so we can display it easily

function base64Image(src) {
  var data = fs.readFileSync(src).toString('base64');
  return util.format('data:%s;base64,%s', mime.lookup(src), data);
}
