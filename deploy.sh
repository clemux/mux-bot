#!/bin/bash
podman save mux-bot:latest | ssh clemux@charlotte.local "docker load"
