apt-get update
apt install gcc python3-dev libffi-dev libssl-dev libxml2-dev libxslt1-dev zlib1g-dev
cd ryu/
pip3 install --upgrade pip
pip3 install --upgrade .
pip3 install webob
python3 setup.py install