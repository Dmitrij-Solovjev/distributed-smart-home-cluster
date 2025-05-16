# distributed-smart-home-cluster

Distributed smart home cluster — это распределённая система ретрансляции сообщений для устройств умного дома, работающая без централизованного облака. Проект использует кластер Kubernetes на базе k0s с сетевым провайдером Kube-Router и лёгковесный брокер сообщений (NATS). Каждый узел кластера выступает ретранслятором, обмениваясь сообщениями по топику `retr_msg`, что обеспечивает устойчивую и масштабируемую связь между устройствами в локальной сети. Благодаря контейнеризации на Python-сервисах и автоматическому деплою через GitHub Actions (CI/CD), HomeRelayCluster легко разворачивается, настраивается и расширяется под любые сценарии «умного дома» без зависимости от внешних облачных сервисов.

---

### 🌳 Структура проекта (устарела, обновить)

```bash
distributed-smart-home-cluster/
├── local_dev_scripts           # Скриптики Python для NATS локального тестирования
├── relay-service/              # Python сервис для ретрансляции сообщений
│   ├── Dockerfile              # Dockerfile для Python сервиса
│   ├── # и мгого-много еще чего
│   ├── app.py                  # Основной Python скрипт
│   └── requirements.txt        # Зависимости Python
└── k0s-configs/                # Конфигурация k0s
    ├── storageclass.yaml       # Хранилка
    └── k0sctl.yaml             # k0sctl конфигурация
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

