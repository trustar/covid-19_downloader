python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
mkdir config_file/private
cp config_file/example/trustar.conf.spec config_file/private/