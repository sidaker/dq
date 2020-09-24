import docker
client = docker.from_env()
print(client)
for container in client.containers.list():
  print(container.id)
