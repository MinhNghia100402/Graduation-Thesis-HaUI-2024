## <p align="center">NX-TRANS DEVELOPMENT BY SDCAI</p> <br>
## How to use<br>


> [!IMPORTANT]
>***Install Docker Engine (on Ubuntu):***<br>
<!-- > Run the following command to uninstall all conflicting packages:
```bash 
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done
``` -->
### Install using the apt repository<br>
1. Set up Docker's apt repository.<br>
``` bash 
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```
2. Install the Docker packages.
To install the latest version, run:
``` bash
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin 
```

<br/>

> [!TIP] 
>***Set up when there is a new model:***<br>
<!-- ### Set up when there is a new model:<br> -->
#### Create a .env file with content similar to the following<br>
``` bash 
api_key=API_KEY
model_name=/hf_models/ntq-trans-m2m-ja-vi-it-20062024
cpu_model_name=/hf_models/ntq-trans-m2m-ja-vi
ko_model_name=/hf_models/ntq-train-ko-vi-08072024
ja_en_model_name=/hf_models/m2m100_418M
log_file=logs/translation.log
REDIS_HOST='HOST'
REDIS_PORT='0000'
REDIS_PASSWORD='PASSWORD'
```

In `Docker-compose.yaml` change the `/hdd-6tb/vuhuy/JaViTranslate/model` path to the `New_path` to use the new translation model (`New_path` is the folder containing the translation model) <br>
```bash
    volumes:
      - ./:/app/
      - {New_path}:/hf_models/
```

### Running the translation project: 
```bash 
docker-compose up --build 
```