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

// Package metadata_sample is an App Engine app that fetches project metadata.
package metadata_sample

import (
	"encoding/json"
	"fmt"
	"net/http"

	"golang.org/x/net/context"
	"golang.org/x/oauth2/google"

	"google.golang.org/api/compute/v1"

	"google.golang.org/appengine"
	"google.golang.org/appengine/log"
)

func init() {
	http.HandleFunc("/", handler)
}

func handler(w http.ResponseWriter, r *http.Request) {
	ctx := appengine.NewContext(r)

	// Get and Print out the metadata
	metadata, err := getMetadata(ctx)
	if err != nil {
		msg := fmt.Sprintf("Could not get metadata: %v", err)
		log.Errorf(ctx, "%s", msg)
		http.Error(w, msg, 500)
		return
	}
	json.NewEncoder(w).Encode(metadata)
}

// getMetadata fetches Project Metadata from the project that this App Engine program is running in.
func getMetadata(ctx context.Context) (map[string]string, error) {
	// Get the OAuth Credentials for the Compute Engine scope
	hc, err := google.DefaultClient(ctx, compute.ComputeScope)

	// Connect to the Compute Engine service
	service, err := compute.New(hc)
	if err != nil {
		return nil, err
	}

	// Get the project
	proj, err := service.Projects.Get(appengine.AppID(ctx)).Do()
	if err != nil {
		return nil, err
	}

	// Convert metadata to a nice map
	meta := make(map[string]string)
	for _, item := range proj.CommonInstanceMetadata.Items {
		if item.Value == nil {
			continue
		}
		meta[item.Key] = *item.Value
	}

	return meta, nil
}
