docker rmi polymetrie
docker rmi leolebossducloud/polymetrie
docker build -t polymetrie .
docker tag polymetrie leolebossducloud/polymetrie:latest
docker push leolebossducloud/polymetrie:latest