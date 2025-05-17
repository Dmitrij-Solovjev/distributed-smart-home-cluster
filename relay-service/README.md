# ReadMe.md

nats context save ^C-nats   --server=my-nats.default.svc.cluster.local:4222   --description="JetStream on k0s"

mkdir -p k0s-configs/nats-contexts
cp ~/.config/nats/context/my-nats.json k0s-configs/nats-contexts/

sudo docker run --name nats-nui \
   -p 31311:31311 \
   -v $(pwd)/k0s-configs/nats-db:/db \
   -v $(pwd)/k0s-configs/nats-contexts:/nats-cli-contexts:ro \
   --nats-cli-contexts=/nats-cli-contexts \
   ghcr.io/nats-nui/nui
