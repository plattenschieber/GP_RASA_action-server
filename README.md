# Action Server for the Chatbot
Custom Action server build with rasa.ai, used to execute custom actions for the chatbot.

##Structure

* *actions.py* this file contains all custom action for the chatbot and will start a http server to communicate with.
* *docker* contains the docker-compose file.

## Deploy and run the project

### locally
First you need to install the requirements by using the provided 'requirements.txt'. To achieve this you can run the following command:
```bash
pip install -r requirements.txt
```
In order to run the action server, you have to execute the next command in a terminal window:
```bash
python -m rasa_core_sdk.endpoint --actions actions
```

### Build
To deploy and run this project docker is mandatory, you would need to install docker as well as docker stack or docker compose. 
You can run the build by the following command. We will tag the image with our docker registry url and the projects name.
```bash
docker build -t docker.nexus.gpchatbot.archi-lab.io/chatbot/action-server .
```

### Run
To run the project simply type the following command:
```bash
docker-compose -f docker/docker-compose.yaml up -d
```
