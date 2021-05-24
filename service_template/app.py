import os

from flask import Flask
from sqlalchemy import create_engine

from service_template.api.health_view import HealthView
from service_template.common import PrefixMiddleware, get, map_url_rules
from service_template.models import Base
from service_template.service.health_service import HealthService

app = Flask(__name__)

PREFIX_PATH = os.environ.get("PREFIX_PATH", "")
DB_HOST = os.environ.get("DB_HOST", "db:5432")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "password")

print(DB_HOST, DB_PASSWORD)

app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix=PREFIX_PATH)

db_engine = create_engine(f"postgresql://postgres:{DB_PASSWORD}@{DB_HOST}/postgres")
Base.metadata.bind = db_engine

health_service = HealthService(db_engine)
health_view = HealthView(health_service)

map_url_rules(
    app,
    {
        "/health": [get(health_view.get_health)],
    },
)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
