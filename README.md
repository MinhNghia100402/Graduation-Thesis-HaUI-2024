## <p align="center">HAUI CHAT</p> <br>
### This is the research topic of the graduation project in 2024.
### Application of RAG and LLM techniques in information retrieval systems.

## How to use

> [!IMPORTANT]
> <br/>
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
> <br/>
>***Set up file `.env` when run :***<br>

``` bash 
git clone https://github.com/MinhNghia100402/Graduation-Thesis-HaUI-2024.git
cd Graduation-Thesis-HaUI-2024/backend/
cp .env_example .env
```

> ### To get data please execute the following command
``` bash 
cd Graduation-Thesis-HaUI-2024/backend/
bash scripts/vector_store.sh
```

> #### Correctly edit the parameter paths in the `/backend/.env` file to be able to use the program.


> [!TIP] 
> <br/>
>***To launch the program run the following command:***<br>
```bash 
docker-compose up -d --build
```


