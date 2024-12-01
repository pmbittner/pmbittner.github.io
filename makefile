# Run this and will launch a local server that hosts the website.
# We will connect with firefox to it.
run:
	(sleep 4s ; firefox "localhost:4000") &
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
