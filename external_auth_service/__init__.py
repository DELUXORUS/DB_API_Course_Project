from flask import Flask
import json

service = Flask(__name__)

with open('../data/cache_config.json') as f:
    service.config['external_auth_service_config'] = json.load(f)

from external_auth_service import api      # только после создания Flask!

if __name__ == '__main__':
    service.run(host='127.0.0.1', port=5000)
