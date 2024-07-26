#!/bin/bash
exec_path="/usr/bin/geckodriver"
if [[ -d $exec_path ]]; then
    echo "geckodriver exists"
else
    #firefox
    sudo install -d -m 0755 /etc/apt/keyrings
    echo 'Package: *Pin: origin packages.mozilla.org Pin-Priority: 1000' | sudo tee /etc/apt/preferences.d/mozilla
    wget -q https://packages.mozilla.org/apt/repo-signing-key.gpg -O- | sudo tee /etc/apt/keyrings/packages.mozilla.org.asc > /dev/null
    echo "deb [signed-by=/etc/apt/keyrings/packages.mozilla.org.asc] https://packages.mozilla.org/apt mozilla main" | sudo tee -a /etc/apt/sources.list.d/mozilla.list > /dev/null
    sudo apt update && sudo apt install firefox -y

    #geckodriver
    wget https://github.com/mozilla/geckodriver/releases/download/v0.34.0/geckodriver-v0.34.0-linux64.tar.gz
    sudo sh -c 'tar -x geckodriver -zf geckodriver-v0.34.0-linux64.tar.gz -O > /usr/bin/geckodriver'
    sudo chown root:root /usr/bin/geckodriver
    sudo chmod +x /usr/bin/geckodriver
    export PATH=$PATH:/usr/bin/geckodriver
    rm geckodriver-v0.34.0-linux64.tar.gz
fi