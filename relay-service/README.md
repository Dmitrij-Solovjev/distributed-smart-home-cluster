# ReadMe.md

### 1. Создаем контекст который после будем использовать для подключения к удаленному сервису NATS

```bash
nats context save my-nats --server=my-nats.default.svc.cluster.local:4222 --description="JetStream on k0s"
```

### 2. Формируем папки и переносим контекст

```bash
mkdir -p k0s-configs/nats
mkdir -p k0s-configs/nats/contexts
mkdir -p k0s-configs/nats/db
cp ~/.config/nats/context/my-nats.json k0s-configs/nats/contexts/
```
### 3. Запускаем Docker-образ NATS GUI (NUI) который будет доступен по [ссылке](http://127.0.0.1:31311)

```bash
sudo docker run --name nats-nui \
  -p 31311:31311 \
  -p 4222:4222 \
  -v "$(pwd)/k0s-configs/nats/db:/db" \
  -v "$(pwd)/k0s-configs/nats/contexts:/nats-cli-contexts:ro" \
  ghcr.io/nats-nui/nui:latest
```

