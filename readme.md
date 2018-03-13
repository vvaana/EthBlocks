# EthBlocks

## 1. Dev with Vagrant
### Go to:

    
## 2. Using venv
## Create folder /dev
    mkdir ./dev
## Clone repository
      git clone https://github.com/vvaana/EthBlocks.git  
      
## Create and activate new environment
      sudo apt-get install -y python3-pip
	  sudo pip3 install --upgrade pip
	  sudo apt-get install -y python3-venv
	  python3 -m venv my_env
	  source my_env/bin/activate
## Install packages
	  cd ./EthBlocks
      sudo pip3 install -r ./requirements.txt
## And run
	  python manage.py migrate
	  python manage.py makemigrations
	  python manage.py runserver 0:8000
## Go to:
      localhost:8000
