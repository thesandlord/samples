#	Copyright 2015, Google, Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#!/bin/bash

clear

printf "\n Creating Cluster \n"

cat << EOM
gcloud beta container --project "smart-spark-93622"
    clusters create "api-world-cluster"
    --zone "us-central1-f"
    --machine-type "n1-standard-1"
    --num-nodes "5"
    --scope "https://www.googleapis.com/auth/compute","https://www.googleapis.com/auth/devstorage.read_only","https://www.googleapis.com/auth/logging.write","https://www.googleapis.com/auth/monitoring"
EOM

gcloud beta container --project "smart-spark-93622" \
    clusters create "api-world-cluster" \
    --zone "us-central1-f" \
    --machine-type "n1-standard-1" \
    --num-nodes "5" \
    --scope "https://www.googleapis.com/auth/compute","https://www.googleapis.com/auth/devstorage.read_only","https://www.googleapis.com/auth/logging.write","https://www.googleapis.com/auth/monitoring"

printf "\n\n Logging into Cluster \n"

cat << EOM
gcloud beta container clusters get-credentials
    --project "smart-spark-93622"
    --cluster "api-world-cluster"
    --zone "us-central1-f"
EOM

gcloud beta container clusters get-credentials \
    --project "smart-spark-93622" \
    --cluster "api-world-cluster" \
    --zone "us-central1-f"

printf "\n\n Build Container \n"

cat << EOM
docker build -t api-world/frontend:1.0 ./frontend-container/
EOM

docker build -t api-world/frontend:1.0 ./frontend-container/

printf "\n\n Publish Container \n"

cat << EOM
docker tag api-world/frontend:1.0 gcr.io/smart-spark-93622/frontend:1.0
gcloud docker push gcr.io/smart-spark-93622/frontend:1.0
EOM

docker tag api-world/frontend:1.0 gcr.io/smart-spark-93622/frontend:1.0
gcloud docker push gcr.io/smart-spark-93622/frontend:1.0

printf "\n\n Create Controller \n"

cat << EOM

kubectl create -f frontend-controller.yaml
EOM

kubectl create -f frontend-controller.yaml

printf "\n\n Create Service \n"

cat << EOM

kubectl create -f frontend-service.yaml
EOM

kubectl create -f frontend-service.yaml

printf "\n\n Get IP Address \n"

cat << EOM
kubectl get services

EOM

sleep 30
kubectl get services