# projectbd

## Server
```
git clone https://github.com/fyfyfyfik/projectbd
sudo apt-get install libqt5x11extras5
cd projectbd/server
cp config.py.bak config.py
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Add new keys
edit add_keys.json
```
python3 model.py
```