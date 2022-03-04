# load_footy_import


In case vm has to be restored or is replaced by tf:

sudo apt install build-essential make unzip libssl-dev libghc-zlib-dev libcurl4-gnutls-dev libexpat1-dev gettext dh-autoreconf libz-dev

sudo apt-get install git

git clone https://github.com/footy-bookie/load_footy_import.git

sudo apt-get -y install python3-pip

pip3 install --upgrade pip

pip3 install -r requirements.txt

sudo apt-get install wget

sudo apt-get update
sudo apt-get install -y curl unzip xvfb libxi6 libgconf-2-4

sudo apt-get install default-jdk 

sudo curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
sudo echo "deb [arch=amd64]  http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
sudo apt-get -y update
sudo apt-get -y install google-chrome-stable

wget https://chromedriver.storage.googleapis.com/98.0.4758.102/chromedriver_linux64.zip
unzip chromedriver_linux64.zip

sudo mv chromedriver /usr/bin/chromedriver
sudo chown root:root /usr/bin/chromedriver
sudo chmod +x /usr/bin/chromedriver

wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb