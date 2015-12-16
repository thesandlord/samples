/*
Copyright 2015 Google Inc. All Rights Reserved.

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

//App Engine app for accessing project metadata
package main

import (
	"encoding/json"
	"fmt"
	"golang.org/x/net/context"
	"golang.org/x/oauth2/google"
	"google.golang.org/api/compute/v1"
	"google.golang.org/appengine"
	"google.golang.org/appengine/log"
	"net/http"
)

func init() {
	http.HandleFunc("/", handler)
}

func handler(w http.ResponseWriter, r *http.Request) {
	// Get the App Engine context
	ctx := appengine.NewContext(r)

	// Get and Print out the metadata
	metadata, err := getMetadata(ctx)
	if err != nil {
		fmt.Fprintf(w, "%s", err)
	} else {
		json.NewEncoder(w).Encode(metadata)
	}

}

// getMetadata will get all Project Metadata from the project
// that this App Engine program is running in. It returns a
// map that contains all the Project Metadata.
func getMetadata(ctx context.Context) (map[string]string, error) {

	// Get the OAuth Credentials for the Compute Engine scope
	hc, err := google.DefaultClient(ctx, compute.ComputeScope)

	// Connect to the Compute Engine service
	service, err := compute.New(hc)
	if err != nil {
		log.Errorf(ctx, "Could Not Connect to Compute Engine Service: %v", err)
		return nil, fmt.Errorf("Could Not Connect to Compute Engine Service: %v", err)
	}

	// Get list of all project metadata
	list, err := service.Projects.Get(appengine.AppID(ctx)).Do()
	if err != nil {
		log.Errorf(ctx, "Could Not Get Compute Engine Metadata: %v", err)
		return nil, fmt.Errorf("Could Not Get Compute Engine Metadata: %v", err)
	}
	metadata := list.CommonInstanceMetadata.Items

	// Convert metadata to a nice map
	metadataMap := make(map[string]string)
	for _, element := range metadata {
		metadataMap[element.Key] = element.Value
	}

	return metadataMap, nil
}
