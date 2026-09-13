# homelab-docker

Docker Compose stack and configuration for my homelab running on a Proxmox VM (`docker-vm`, 100.99.62.65).

## Stack overview

| Service | Port | Description |
|---------|------|-------------|
| Homarr | 7575 | Dashboard with Catppuccin Mocha glassmorphism theme |
| Grafana | 3000 | Metrics dashboards (Node Exporter, Proxmox, GPU, cAdvisor, smartctl) |
| Prometheus | 9090 | Metrics scraping — nodes, Proxmox, GPU, Docker, smart |
| Alertmanager | 9093 | Alert routing to ntfy push notifications |
| Frigate | 5000 | NVR with TensorRT object detection (RTX 3060) |
| Jellyfin | 8096 | Media server with NVENC hardware transcoding |
| Nextcloud | — | File sync and sharing |
| Ollama | 11434 | LLM inference on RTX 3060 |
| Open WebUI | 3002 | Web interface for Ollama |
| ComfyUI | 8188 | Stable Diffusion image generation |
| Radarr | 7878 | Movie management |
| Sonarr | 8989 | TV series management |
| Prowlarr | 9696 | Indexer manager |
| Fathom | 8091 | Self-hosted log aggregator |
| ntfy | 8090 | Push notification server |
| AdGuard Home | 3001 | DNS ad blocker |
| Redmine | 8080/8081 | Project management (production + dev) |
| Watchtower | — | Automatic container image updates (3 AM nightly) |
| cAdvisor | 8070 | Container resource metrics |
| Blackbox Exporter | 9115 | Service uptime probing |
| PVE Exporter | 9221 | Proxmox metrics for Prometheus |
| Whisper | — | ASR for Frigate audio events |

## Structure

```
docker-compose.yml          # Main stack definition
.env                        # Credentials (not committed — see .env.example)
prometheus/                 # prometheus.yml scrape config
prometheus-rules/           # Alert rules
alertmanager/               # alertmanager.yml routing config
caddy/                      # Caddyfile reverse proxy (Frigate TLS)
pve-exporter/               # pve.yml Proxmox exporter config
ntfy/                       # server.yml ntfy config
homarr/                     # Custom CSS theme + layout snapshot
grafana-*.css               # Catppuccin theme for Grafana
adguard-catppuccin.css      # Catppuccin theme for AdGuard
arr-catppuccin.css          # Catppuccin theme for *arr apps
redmine-custom/             # Custom Redmine Dockerfile with plugins
redmine-ai/                 # Redmine AI helper config
```

## Setup

1. Copy `.env.example` to `.env` and fill in all values.
2. `docker compose up -d`

Credentials are passed via environment variables — no secrets are committed to this repository.

## Themes

All services use [Catppuccin Mocha](https://github.com/catppuccin/catppuccin) with glassmorphism effects where supported (Homarr, Grafana, AdGuard, Open WebUI, *arr apps).

Homarr wallpaper: Milky Way nebula — `https://images.unsplash.com/photo-1419242902214-272b3f66ee7a`
