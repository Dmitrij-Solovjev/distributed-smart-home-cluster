# distributed-smart-home-cluster

Distributed smart home cluster — это распределённая система ретрансляции сообщений для устройств умного дома, работающая без централизованного облака. Проект использует кластер Kubernetes на базе k0s с сетевым провайдером Kube-Router и лёгковесный брокер сообщений (NATS). Каждый узел кластера выступает ретранслятором, обмениваясь сообщениями по топику `retr_msg`, что обеспечивает устойчивую и масштабируемую связь между устройствами в локальной сети. Благодаря контейнеризации на Python-сервисах и автоматическому деплою через GitHub Actions (CI/CD), HomeRelayCluster легко разворачивается, настраивается и расширяется под любые сценарии «умного дома» без зависимости от внешних облачных сервисов.


### Структура проекта

```bash
distributed-smart-home-cluster/
├── nats-broker/
│   ├── Dockerfile
│   ├── nats-config.conf
│   └── docker-compose.yml
├── relay-service/
│   ├── Dockerfile
│   ├── app/
│   │   ├── main.py
│   │   └── requirements.txt
│   └── docker-compose.yml
└── k0sctl.yaml
```
