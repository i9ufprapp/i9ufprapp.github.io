#!/bin/bash
pip install --no-cache-dir -r requirements.txt
gunicorn main:app --bind 0.0.0.0:$PORT
