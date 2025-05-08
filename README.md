# distributed-smart-home-cluster

Distributed smart home cluster — это распределённая система ретрансляции сообщений для устройств умного дома, работающая без централизованного облака. Проект использует кластер Kubernetes на базе k0s с сетевым провайдером Kube-Router и лёгковесный брокер сообщений (NATS). Каждый узел кластера выступает ретранслятором, обмениваясь сообщениями по топику `retr_msg`, что обеспечивает устойчивую и масштабируемую связь между устройствами в локальной сети. Благодаря контейнеризации на Python-сервисах и автоматическому деплою через GitHub Actions (CI/CD), HomeRelayCluster легко разворачивается, настраивается и расширяется под любые сценарии «умного дома» без зависимости от внешних облачных сервисов.


### Структура проекта

```bash
distributed-smart-home-cluster/
├── nats-broker/                # Kubernetes манифесты для NATS
│   ├── deployment.yaml         # Deployment для NATS
│   └── service.yaml            # Service для NATS
├── relay-service/              # Python сервис для ретрансляции сообщений
│   ├── Dockerfile              # Dockerfile для Python сервиса
│   ├── app.py                  # Основной Python скрипт
│   └── requirements.txt        # Зависимости Python
└── k0s-configs/                # Конфигурация k0s
    └── k0sctl.yaml             # k0sctl конфигурация
```

