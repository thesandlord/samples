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
docker rmi -f api-world/frontend:2.0
docker rmi -f gcr.io/smart-spark-93622/frontend:2.0
clear

printf "\n IMPORTANT: Part 1 Must be run first! \n"

printf "\n\n Build Containers \n"

cat << EOM
docker build -t api-world/frontend:2.0 ./frontend-container/
EOM

docker build -t api-world/frontend:2.0 ./frontend-container/

cat << EOM
docker build -t api-world/backend:1.0 ./backend-container/
EOM

docker build -t api-world/backend:1.0 ./backend-container/

printf "\n\n Publish Containers \n"

cat << EOM
docker tag api-world/frontend:2.0 gcr.io/smart-spark-93622/frontend:2.0
gcloud docker push gcr.io/smart-spark-93622/frontend:2.0
EOM

docker tag api-world/frontend:2.0 gcr.io/smart-spark-93622/frontend:2.0
gcloud docker push gcr.io/smart-spark-93622/frontend:2.0

cat << EOM
docker tag api-world/backend:1.0 gcr.io/smart-spark-93622/backend:1.0
gcloud docker push gcr.io/smart-spark-93622/backend:1.0
EOM

docker tag api-world/backend:1.0 gcr.io/smart-spark-93622/backend:1.0
gcloud docker push gcr.io/smart-spark-93622/backend:1.0

printf "\n\n Create Backend Controller \n"

cat << EOM

kubectl create -f backend-controller.yaml
EOM

kubectl create -f backend-controller.yaml

printf "\n\n Create Backend Service \n"

cat << EOM

kubectl create -f backend-service.yaml
EOM

kubectl create -f backend-service.yaml

printf "\n\n Update Frontend \n"

cat << EOM
kubectl rolling-update frontend --image=gcr.io/smart-spark-93622/frontend:2.0 --update-period="1s"

EOM

kubectl rolling-update frontend --image=gcr.io/smart-spark-93622/frontend:2.0 --update-period="1s"