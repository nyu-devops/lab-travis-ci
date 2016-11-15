# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure(2) do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://atlas.hashicorp.com/search.
  config.vm.box = "ubuntu/trusty64"

  # config.vm.network "forwarded_port", guest: 80, host: 8080
  config.vm.network "forwarded_port", guest: 5000, host: 5000

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  config.vm.network "private_network", ip: "192.168.33.10"
  # config.vm.network "public_network"
  # config.vm.synced_folder "../data", "/vagrant_data"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  config.vm.provider "virtualbox" do |vb|
    # Display the VirtualBox GUI when booting the machine
    #vb.gui = true

    # Customize the amount of memory on the VM:
    vb.memory = "1024"
    vb.cpus = 1
  end

  # Copy your .gitconfig file so that your credentials are correct
  config.vm.provision "file", source: "~/.gitconfig", destination: "~/.gitconfig"

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  config.vm.provision "shell", inline: <<-SHELL
    sudo apt-get update
    sudo apt-get install -y git python-pip python-dev build-essential zip
    sudo apt-get -y autoremove
    # Make vi look nice
    echo "colorscheme desert" > ~/.vimrc
    # Install Foreman for Profile support
    sudo gem install foreman --no-rdoc --no-ri
    # Install the Cloud Foundry CLI
    wget -O cf-cli-installer_6.22.1_x86-64.deb 'https://cli.run.pivotal.io/stable?release=debian64&version=6.22.1&source=github-rel'
    sudo dpkg -i cf-cli-installer_6.22.1_x86-64.deb
    rm cf-cli-installer_6.22.1_x86-64.deb
    # # Install the Bluemix CLI
    # wget http://public.dhe.ibm.com/cloud/bluemix/cli/bluemix-cli/Bluemix_CLI_0.4.2_amd64.tar.gz
    # tar -xvf Bluemix_CLI_0.4.2_amd64.tar.gz
    # cd Bluemix_CLI/
    # sudo ./install_bluemix_cli
    # cd ..
    # rm -fr Bluemix_CLI/
    # rm Bluemix_CLI_0.4.2_amd64.tar.gz
    # Install app dependencies
    cd /vagrant
    sudo pip install -r requirements.txt
    # Prepare Redis data share
    sudo mkdir -p /var/lib/redis/data
    sudo chown vagrant:vagrant /var/lib/redis/data
  SHELL

  # Add Redis docker container
  config.vm.provision "docker" do |d|
    d.pull_images "alpine:latest"
    d.pull_images "redis:alpine"
    d.run "redis:alpine",
      args: "--restart=always -d --name redis -h redis -p 6379:6379 -v /var/lib/redis/data:/data"
  end

  # Install Docker Compose after Docker Engine
  config.vm.provision "shell", inline: <<-SHELL
    sudo pip install docker-compose
    # Install the IBM Container plugin
    cf plugins
    echo Y | cf install-plugin https://static-ice.ng.bluemix.net/ibm-containers-linux_x64
    cf plugins
  SHELL

end
