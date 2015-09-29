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

var GeoService = grpc.buildServer([proto.geo.GeoService.service]);

var server = new GeoService({
	'geo.GeoService': {
		distanceBetween: function(call, callback) {
			callback(null, getDistance(call.request));
		}
	}
});

function getDistance(points){
	return distance(points.origin.lat, points.origin.lng, points.destination.lat, points.destination.lng);
}

server.bind('0.0.0.0:50051');
server.listen();


// From http://stackoverflow.com/questions/27928/how-do-i-calculate-distance-between-two-latitude-longitude-points
// User: Salvador Dali - http://stackoverflow.com/users/1090562/salvador-dali
function distance(lat1,lon1,lat2,lon2) {
	var R = 6371; // Radius of the earth in km
	var a =
		0.5 - Math.cos((lat2 - lat1) * Math.PI / 180)/2 +
		Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
		(1 - Math.cos((lon2 - lon1) * Math.PI / 180))/2;
	return R * 2 * Math.asin(Math.sqrt(a));
}
////////////////////////////////////