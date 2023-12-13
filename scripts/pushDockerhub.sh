docker rmi polymetrie
docker build -t polymetrie .
docker tag polymetrie leolebossducloud/polymetrie:latest
docker push leolebossducloud/polymetrie:latest