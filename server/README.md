# projectbd

## Server
```
git clone https://github.com/fyfyfyfik/projectbd
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