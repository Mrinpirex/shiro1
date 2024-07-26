#!/bin/bash
apt-get update

pip install --upgrade pip && pip install --no-cache-dir -r /content/shirobot/requirements.txt && python /content/shirobot/main.py