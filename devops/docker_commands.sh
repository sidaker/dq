docker run hello-world
docker image ls
docker ps
docker ps -all

docker run hello-world
docker create hello-world
docker start -a <image id>
# -a option attaches the output from the container and displays it to you

docker run = docker create + docker start

docker system prune

docker logs <container id>

docker stop <container id>
#Issues SIGTERM . Graceful shutdown and clean up.

docker kill <container id>
#Immediate kill. Issues SIGKILL.

docker run redis

docker exec -it <container-id> <command to execute>

docker exec -it <container-id>  redis-cli

docker exec -it <container-id>  sh
# ensures you loginto the container.

'''
You start a redis container and then execute a command.
-it allows us to provide input to the container.
-i -t flags
-i ensures what we type get redirected to the stdin of the process.
In this case -i will ensure what we type gets redirected to stdin of redis-cli.
'''











'''
hodqadms-MacBook-Pro:.aws sbommireddy$ docker create hello-world
888ab351d1ef828a456740daf21b2d189499b8eaf49db0b7ef754a297cd28e8b

hodqadms-MacBook-Pro:.aws sbommireddy$ docker create hello-world
feaad1b6de1de484bcde73b819babf94c9386761291b4d9a29b2606dd7546c64
hodqadms-MacBook-Pro:.aws sbommireddy$ docker start -a feaad1b6de1de484bcde73b819babf94c9386761291b4d9a29b2606dd7546c64

Hello from Docker!

'''

'''
hodqadms-MacBook-Pro:.aws sbommireddy$ docker run hello-world

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/

hodqadms-MacBook-Pro:.aws sbommireddy$
'''

docker image ls

'''
hodqadms-MacBook-Pro:.aws sbommireddy$ docker image ls
REPOSITORY                                TAG                 IMAGE ID            CREATED             SIZE
fmstable                                  latest              9996854cc302        9 days ago          992MB
athenaadhoc                               latest              a867c9b48594        2 weeks ago         1.04GB
natsprocess                               latest              66f4fea8ae53        2 weeks ago         1.15GB
python                                    3.7                 fbf9f709ca9f        6 weeks ago         917MB
quay.io/ukhomeofficedigital/centos-base   v0.5.14             77294726301e        5 months ago        312MB
hello-world                               latest              fce289e99eb9        12 months ago       1.84kB
hodqadms-MacBook-Pro:.aws sbommireddy$
'''
docker ps
docker ps -all

'''
hodqadms-MacBook-Pro:.aws sbommireddy$ docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
hodqadms-MacBook-Pro:.aws sbommireddy$
hodqadms-MacBook-Pro:.aws sbommireddy$
hodqadms-MacBook-Pro:.aws sbommireddy$ docker ps -all
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS                   PORTS               NAMES
76da539df464        hello-world         "/hello"            3 hours ago         Exited (0) 3 hours ago                       busy_poincare
hodqadms-MacBook-Pro:.aws sbommireddy$
'''



'''

You can override the primary run command.

hodqadms-MacBook-Pro:.aws sbommireddy$ docker run busybox echo Hi BaLi
Unable to find image 'busybox:latest' locally
latest: Pulling from library/busybox
bdbbaa22dec6: Pull complete
Digest: sha256:6915be4043561d64e0ab0f8f098dc2ac48e077fe23f488ac24b665166898115a
Status: Downloaded newer image for busybox:latest
Hi BaLi
hodqadms-MacBook-Pro:.aws sbommireddy$
'''
