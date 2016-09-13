# vagrant-docker-django-nginx
A sample django project which uses redis and postgresql, which is deployed using docker and vagrant.

This is a Django/nginx/postgres/redis app which is deployed using Vagrant and Docker. 
The stack includes a separate container for each service: 

1 web/Django container
1 nginx container
1 Postgres container
1 Redis container
1 data container

Architecture :

1. First, the django_image service is built via the instructions in the Dockerfile within the “django_image” directory – where the Python environment is setup, 
requirements are installed, and the Django application is fired up on port 8080. That port is then forwarded to port 80 on the host environment – e.g., the Docker Machine. 
This service also adds environment variables to the container that are defined in the .env file.
2. The nginx service is used for reverse proxy to forward requests either to Django or the static file directory.
3. Next, the postgres service is built from the the official PostgreSQL image from Docker Hub, which installs Postgres and runs the server on the default port 5432. 
4. The data container? This helps ensure that the data persists even if the Postgres container is deleted.
5. Likewise, the redis service uses the official Redis image to install, well, Redis and then the service is ran on port 6379.

SETUP
----------------------------------
For deployment, do the next steps:

( This will only need to be done once per machine.)

1. Virtual Box >= 5 MUST be installed, else you'll end up having problems with npm packages inside client container

2. Vagrant
    https://www.vagrantup.com/downloads.html

3. Vagrant plugins

   vagrant plugin install vagrant-docker-compose    
   vagrant plugin install vagrant-gatling-rsync
   vagrant plugin install vagrant-vbguest


RUN
-----------------------------------

Using your fav terminal from the project root, run:
    vagrant up

This will provision an Ubuntu VM (your docker host), forward ports down to the host OS, install docker, docker-compose
and docker-cloud, setup rsync for synced folders and start watching for changes, build and run your application.

This should launch the django server at http://localhost:8080/.

To create the database migrations, run : 
docker-compose run --rm django_image python manage.py migrate

The project root should be synced to the /vagrant directory in the VM and the rsync should be active.

If you run docker-compose ps to see all the active containers, you should see something like this : 

vagrant@vagrant-ubuntu-trusty-64:/vagrant$ docker-compose ps
         Name                       Command                 State              Ports
---------------------------------------------------------------------------------------------
vagrant_data_1           /docker-entrypoint.sh true       Restarting   5432/tcp
vagrant_db_1             /docker-entrypoint.sh postgres   Up           0.0.0.0:5432->5432/tcp
vagrant_django_image_1   /bin/bash -c python manage ...   Up           8000/tcp
vagrant_nginx_1          /usr/sbin/nginx                  Up           0.0.0.0:80->80/tcp
vagrant_redis_1          docker-entrypoint.sh redis ...   Up           0.0.0.0:6379->6379/tcp


-----------------------------------
DEBUG
-----------------------------------

From project root in your fav terminal:

VM/Vagrant
----------

To launch the VM 
    vagrant up

To check the status of the VM
    vagrant status

To shutdown the VM (free up RAM and paged disk)
    vagrant halt

To suspend the VM (free up RAM)
    vagrant suspend

To destoy the VM completely (free up all teh things)
    vagrant destroy

To reload the VM (after vagrantfile changes, to relaunch etc.)
    vagrant reload

To SSH into the VM
    vagrant ssh

To manually start watching files to sync (if the VM failed to properly init/reload)
    vagrant gatling-rsync-auto

To reprovision the VM (re-run all VM provisioners on a running box e.g. docker and docker-compose)
    vagrant provision

Container/Docker
----------------

Once SSHed into the VM you can run any docker commands as you would normally..

Then:

To build the application
    docker-compose build

To (re)launch the application
    docker-compose up

To check the status of the application
    docker-compose ps

To teardown the application (stop and remove containers)
    docker-compose down

To start/stop/restart a specific service
    docker-compose start/stop/restart <service-name>

To view logs (optionally filtered by service name)
    docker-compose logs <service-name>

To bash into a running container (used to debug/run tests etc.)
    docker exec -it <container-name> bash



