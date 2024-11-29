run:
	bundle exec jekyll serve

# alternative setup with docker
docker-prepare:
	sudo docker compose pull
docker-run:
	sudo docker compose up
start-docker-daemon:
	sudo systemctl start docker
stop-docker-daemon:
	sudo systemctl stop docker
