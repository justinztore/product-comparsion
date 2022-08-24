# Initial the project

## install the following package in local python environemnt 
```
pip install pipenv
```

## create a virtual environment insdie the project 
```
pipenv install
```

## change to the virtual environment
```
pipenv shell
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

## start mysql
```
make create-mysql-volume
make deploy-mysql
```

## create talble in database
import the sql file "productdata/db/schema.py" to database


# Execute the task

## Scrape watsons category
```
pipenv run python productdata/producer.py watsons_category 
```

## Scrape watsons category
```
pipenv run python productdata/producer.py watsons_product
```