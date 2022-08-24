# 初始化 docker swarm
init-swarm:
	docker swarm init

deploy-portainer:
	docker stack deploy -c portainer.yml por

# 啟動 rabbitmq
deploy-rabbitmq:
	docker stack deploy -c rabbitmq.yml rabbitmq

# 建立 network
create-network:
	docker network create --driver=overlay my_network

# 建立 mysql volume
create-mysql-volume:
	docker volume create mysql

# 啟動 mysql
deploy-mysql:
	docker stack deploy -c mysql.yml mysql

# 安裝相對應的 package
install-package:
	pipenv sync

# 建立 dev 環境變數
gen-dev-env-variable:
	python genenv.py

# 建立 staging 環境變數
gen-staging-env-variable:
	VERSION=STAGING python genenv.py

# 建立 release 環境變數
gen-release-env-variable:
	VERSION=RELEASE python genenv.py

run-worker-watsons:
	pipenv run celery -A productdata.worker worker --loglevel=info --concurrency=1  --hostname=%h -Q watsons

run-worker-hktvmall:
	pipenv run celery -A productdata.worker worker --loglevel=info --concurrency=1  --hostname=%h -Q hktvmall