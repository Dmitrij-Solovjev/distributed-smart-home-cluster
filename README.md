# distributed-smart-home-cluster

Distributed smart home cluster — это распределённая система ретрансляции сообщений для устройств умного дома, работающая без централизованного облака. Проект использует кластер Kubernetes на базе k0s с сетевым провайдером Kube-Router и лёгковесный брокер сообщений (NATS). Каждый узел кластера выступает ретранслятором, обмениваясь сообщениями по топику `retr_msg`, что обеспечивает устойчивую и масштабируемую связь между устройствами в локальной сети. Благодаря контейнеризации на Python-сервисах и автоматическому деплою через GitHub Actions (CI/CD), HomeRelayCluster легко разворачивается, настраивается и расширяется под любые сценарии «умного дома» без зависимости от внешних облачных сервисов.

---

### 🌳 Структура проекта (устарела, обновить)

```bash
distributed-smart-home-cluster
-----------------------------------------------------------------------------------------------------------------------
├── k0s-configs/                    # Конфигурация для k0s-кластера
│   ├── k0sctl.yaml                 # Конфигурация k0sctl (включает NATS, Prometheus Stack, Traefik Ingress Controller)
│   └── storageclass.yaml           # Конфигурация StorageClass для хранения данных NATS
│
├── local_dev_scripts/              # Скрипты для локального тестирования взаимодействия с NATS
│   ├── pub.py                      # Публикация сообщений в NATS
│   └── sub.py                      # Подписка на сообщения из NATS
│
├── pytest.ini                      # Конфигурация Pytest
│
├── README.md                       # Описание проекта (этот файл)
│
└── relay-service/                  # Сервис ретрансляции сообщений
    ├── app.py                      # Основной код приложения
    ├── Dockerfile                  # Docker-образ для развертывания сервиса
    ├── requirements.txt            # Зависимости Python-проекта
    ├── service.yaml                # Описание Kubernetes-сервиса
    ├── statefulset.yaml            # Описание StatefulSet для Kubernetes
    └── tests/
        └── test_app.py             # Тесты для приложения (Pytest)
```

---

## 🚀 Деплой

1. **Развертывание кластера k0s**:

   ```bash
   k0sctl apply --config k0s-configs/k0sctl.yaml
   ```

2. **To access your k0s cluster, use k0sctl to generate a kubeconfig for the purpose.**

   ```bash
   k0sctl kubeconfig --config k0s-configs/k0sctl.yaml > k0s-configs/kubeconfig
   ```

3. **Установите переменную окружения KUBECONFIG**

   ```bash
   export KUBECONFIG="$(pwd)/k0s-configs/kubeconfig"
   ```

4. **Настроить хранилку**
   ```bash
    k0sctl apply --config k0s-configs/storageclass.yaml
   ```

4. **(Должно работать) Заново обновить конфиг (с уже подгруженным StorageClass**
   ```bash
   k0sctl apply --config k0s-configs/k0sctl.yaml
   ```

5. **Применение манифестов Kubernetes**:

   ```bash
   kubectl apply -f relay-service/statefullset.yaml
   kubectl apply -f relay-service/service.yaml
   ```

6. **Проверка статуса**:

   ```bash
   kubectl get pods,svc,statefulset -n default
   kubectl describe statefulset relay-service
   kubectl describe pod relay-service-0
   ```

7. **Чтобы обновить после выпуска обновления**

   ```bash
   kubectl rollout restart deployment/relay-service
   ```

