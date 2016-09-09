Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/trusty64"
  # we'll forward the port 8000 from the VM to the port 8000 on the host
  config.vm.network :forwarded_port, host: 8080, guest: 80, auto_correct: true
  #config.vm.network :private_network, ip: "192.168.68.8"
  config.vm.network :public_network
  config.vm.provision "docker"
  config.vm.provision :docker_compose, yml: "/vagrant/docker-compose.yml", rebuild: true, run: "always"
  # add 2 GB of memory
  config.vm.provider :virtualbox do |vb|
    vb.customize ["modifyvm", :id, "--memory", 2048]
    vb.gui = true
  end
end