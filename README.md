# ships
#for activate without docker
git clone https://github.com/hens2013/ships.git

cd ships

python3 -m venv env

source env/bin/activate

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver

navigate to the given url in the log


#for activate with docker -> https://blog.logrocket.com/dockerizing-django-app/
git clone https://github.com/hens2013/ships.git

cd ships

sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io

docker build . -t docker-django-v0.0

docker ps

docker run docker-django-v0.0




