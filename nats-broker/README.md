## 🎯 Быстрый старт

1. Применить все манифесты:

   ```bash
   kubectl apply -f nats-broker/configmap.yaml      # конфигурация сервера NATS
   kubectl apply -f nats-broker/pv-pvc.yaml         # PersistentVolumeClaim для хранения JetStream
   kubectl apply -f nats-broker/deployment.yaml     # Deployment с включенным JetStream
   kubectl apply -f nats-broker/service.yaml        # Service для доступа к NATS
   kubectl apply -f nats-broker/storageclass.yaml
   kubectl apply -f nats-broker/persistentvolumeclaim.yaml
   kubectl apply -f nats-broker/configmap.yaml
   kubectl apply -f nats-broker/statefulset.yaml
   kubectl apply -f nats-broker/service.yaml

   ```

2. Проверить статус:

   ```bash
   kubectl get pods,svc,pvc -l app=nats-broker
   ```

---

## 📁 Описание файлов

| Файл                | За что отвечает                                                                                                                                                                                   |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **configmap.yaml**  | Настройки NATS Server:<br>– включает JetStream (`jetstream { … }`),<br>– задаёт `store_dir` для хранения данных,<br>– открывает HTTP‑мониторинг на 8222 порту. |
| **pv-pvc.yaml**     | Запрос на PersistentVolumeClaim для `store_dir` JetStream:<br>– запрашивает 5 Gi хранилища, чит‑запись (RWO),<br>– связывается с динамически созданным PV через StorageClass.   |
| **deployment.yaml** | Деплой NATS:<br>– монтирует `configmap` как `/etc/nats`,<br>– монтирует `pvc` как `/data/jetstream`,<br>– запускает `nats-server` с `-c /etc/nats/nats-server.conf` для включения JetStream.      |
| **service.yaml**    | Kubernetes Service:<br>– порт 4222 для клиентов NATS, <br>– порт 8222 для мониторинга/HTTP.                                                                                                       |

---

## ℹ️ Замечания

* **ConfigMap** позволяет отделить конфигурацию от образа контейнера и хранить её отдельно.
* **PersistentVolumeClaim (PVC)** запрашивает постоянное хранилище для потоков JetStream, обеспечивая сохранность данных даже после перезапуска пода.
* После успешного `kubectl apply -f` NATS поднимется автоматически и начнёт слушать клиентов на `nats-broker:4222`, а мониторинг будет доступен по `nats-broker:8222`.

