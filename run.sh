#!/bin/bash
docker run -d -p 6379:6379 --name redis-db redis:latest
python app/app.py
