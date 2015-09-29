/*
	Copyright 2015, Google, Inc.
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
var url = require('url');
var grpc = require('grpc');

var proto = grpc.load('interface.proto');

var client = new proto.geo.GeoService('backend:50051');

function getDistance(response, query) {

	console.log(query);

	var lat1 = parseFloat((query.lat1) ? query.lat1 : 0);
	var lng1 = parseFloat((query.lng1) ? query.lng1 : 0);

	var lat2 = parseFloat((query.lat2) ? query.lat2 : 15);
	var lng2 = parseFloat((query.lng2) ? query.lng2 : 15);

	var request = {
		origin: {
			lat: lat1,
			lng: lng1
		},
		destination: {
			lat: lat2,
			lng: lng2
		},
	}

	client.distanceBetween(request, function(error, distance) {
		if (error) {
			response.end(JSON.stringify(error));
		} else {
			response.end("Distance = " + JSON.stringify(distance) + "\n");
		}
	});
}

var http = require('http');
var server = http.createServer(function(request, response) {
	response.writeHead(200, {
		"Content-Type": "text/plain"
	});
	getDistance(response, url.parse(request.url, true).query);
});
server.listen(3000);
