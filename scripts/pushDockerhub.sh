printf "\n\033[1;31m## Deleting old Polymetrie Docker image\033[0m\n"
docker rmi polymetrie
docker rmi leolebossducloud/polymetrie

printf "\n\033[1;36m## Build new Polymetrie Docker image\033[0m\n"
docker build -t polymetrie .

printf "\n\033[1;36m## Tag new image leolebossducloud/polymetrie:latest\033[0m\n"
docker tag polymetrie leolebossducloud/polymetrie:latest

printf "\n\033[1;36m## Push taged image on DockerHub\033[0m\n"
docker push leolebossducloud/polymetrie:latest