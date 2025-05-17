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

### 1. **Развертывание кластера k0s**:

   ```bash
   k0sctl apply --config k0s-configs/k0sctl.yaml
   ```

### 2. **To access your k0s cluster, use k0sctl to generate a kubeconfig for the purpose.**

   ```bash
   k0sctl kubeconfig --config k0s-configs/k0sctl.yaml > k0s-configs/kubeconfig
   ```

### 3. **Установите переменную окружения KUBECONFIG**

   ```bash
   export KUBECONFIG="$(pwd)/k0s-configs/kubeconfig"
   ```

### 4. **Настроить хранилку**
   ```bash
    kubectl apply -f https://raw.githubusercontent.com/rancher/local-path-provisioner/master/deploy/local-path-storage.yaml
   ```

### 5. **Проверка работы Provisioner**
    1. Убедитесь, что появились ресурсы в namespace:
   ```bash
   kubectl get ns/local-path-storage                  # namespace создан
   kubectl get pods -n local-path-storage             # должен быть Pod provisioner
   kubectl get sc                                     # StorageClass local-path(default=false)
   ```
   2. Сделайте его default:
   ```bash
   kubectl patch storageclass local-path \
      -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'
   ```

### 6. **Добавление репозитория Helm**

   ```bash
   helm repo add nats https://nats-io.github.io/k8s/helm/charts/    # подключаем репозиторий
   helm repo update                                               # обновляем списки чартов
   ```

### 7. **Установка NATS с JetStream**

    Далее необходимо непосредственно применить конфиг-файл и развернуть NATS

   ```bash
    helm upgrade --install my-nats nats/nats -f k0s-configs/nats-values.yaml
   ```


### 8. Проверка работы

1. Убедитесь, что Pods в статусе `Running`:

   ```bash
   kubectl get pods -l app.kubernetes.io/instance=my-nats
   ```
2. Запустите в трех разных экземплярах терминала:

   ```bash
   kubectl port-forward svc/my-nats 4222:4222
   ```
   ```bash
   nats pub test "hello" -s nats://127.0.0.1:4222
   ```
   ```bash
   nats sub test -s nats://127.0.0.1:4222 --timeout 2s
   ```

### 9. **Применение манифестов Kubernetes**:

   ```bash
   kubectl apply -f relay-service/statefullset.yaml
   kubectl apply -f relay-service/service.yaml
   ```

### 10. **Проверка статуса**:

   ```bash
   kubectl get pods,svc,statefulset -n default
   kubectl describe statefulset relay-service
   kubectl describe pod relay-service-0
   ```

### 11. **Чтобы обновить после выпуска обновления**

   ```bash
   kubectl rollout restart deployment/relay-service
   ```

