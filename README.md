# gpb-chatbot-action-server
Rasa Action Server with costum actions for rasa core

## Install Steps
```bash
pip install -r requirements.txt
```
## How to run
```bash
python -m rasa_core_sdk.endpoint --actions actions
```

## Docker
Diesem Projekt liegt eine Dockerfile und ein Docker-Compose bei, diese stellen das Projekt als Docker-Container zu Verfügung.
Um das Image zu bauen und zu starten müssen die folgenden Befehle ausgeführt werden.

```bash
docker build -t chatbot-action-server .
docker-compose -p gpb -f docker/docker-compose.yaml up
```