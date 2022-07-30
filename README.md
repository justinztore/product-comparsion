# Initial the project

## create a virtual environment insdie the project 
```
python -m venv .venv
```

## change to the virtual environment
```
source /Users/justinkwok/Documents/GitHub/product-comparsion/.venv/bin/activate
```

## install the package
```
pip install -r requirement.txt
```

# Start the project 
you need to install docker first : https://www.docker.com/get-started/

## initial docker swarm
```
make init-swarm
```

## start portainer
```
make deploy-portainer
```

## start RabbitMQ
```
make deploy-rabbitmq
```

## start network
```
make create-network
```

## srat mysql
```
make create-mysql-volume
make deploy-mysql
```