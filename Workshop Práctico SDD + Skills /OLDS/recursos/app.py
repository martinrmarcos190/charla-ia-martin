"""Solución de referencia — API local de issues de infraestructura (Bloque 3).

Correr (sin instalar nada, con uv — pinneá el Python para no agarrar uno viejo):
    uv run --python 3.12 --with flask app.py

OJO macOS: AirPlay Receiver ocupa el puerto 5000 (devuelve 403). Desactivalo en
Ajustes del Sistema → General → AirDrop y Handoff, o cambiá el puerto.

Probar:
    curl http://127.0.0.1:5000/health
    curl http://127.0.0.1:5000/issues
    curl -X POST http://127.0.0.1:5000/issues -H "Content-Type: application/json" \
      -d '{"title":"Cert TLS por vencer","service":"cert-monitor","severity":"medium"}'
    curl -X PUT http://127.0.0.1:5000/issues/1 -H "Content-Type: application/json" \
      -d '{"status":"resolved","proposed_solution":"Pool ampliado a 50."}'
    curl http://127.0.0.1:5000/issues/1

Nota: este archivo es la *referencia* del facilitador. En el Bloque 3 los
participantes lo generan vía SDD a partir de recursos/problema.md.
"""
import sqlite3
from datetime import datetime, timezone

from flask import Flask, g, jsonify, request

app = Flask(__name__)
DB = "issues.db"

SEVERITIES = {"low", "medium", "high", "critical"}
STATUSES = {"open", "investigating", "resolved"}

SEED = [
    {
        "title": "Timeouts intermitentes contra la DB",
        "service": "payments-api",
        "severity": "high",
        "description": "Conexiones a la base agotan el pool en hora pico.",
        "proposed_solution": "Revisar tamaño del pool y queries lentas.",
    },
    {
        "title": "502 intermitentes en /checkout",
        "service": "api-gateway",
        "severity": "high",
        "description": "El gateway devuelve 502 esporádicos hacia checkout-service.",
        "proposed_solution": "Chequear health del upstream y reintentos.",
    },
]


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = sqlite3.connect(DB)
    db.execute(
        """CREATE TABLE IF NOT EXISTS issues (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               title TEXT NOT NULL,
               service TEXT NOT NULL,
               severity TEXT NOT NULL,
               status TEXT NOT NULL DEFAULT 'open',
               description TEXT,
               proposed_solution TEXT,
               created_at TEXT,
               updated_at TEXT
           )"""
    )
    if db.execute("SELECT COUNT(*) FROM issues").fetchone()[0] == 0:
        for it in SEED:
            db.execute(
                """INSERT INTO issues
                   (title, service, severity, status, description, proposed_solution, created_at)
                   VALUES (?, ?, ?, 'open', ?, ?, ?)""",
                (it["title"], it["service"], it["severity"],
                 it["description"], it["proposed_solution"], now_iso()),
            )
    db.commit()
    db.close()


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/issues")
def list_issues():
    rows = get_db().execute("SELECT * FROM issues ORDER BY id").fetchall()
    return jsonify([dict(r) for r in rows])


@app.get("/issues/<int:issue_id>")
def get_issue(issue_id):
    row = get_db().execute("SELECT * FROM issues WHERE id = ?", (issue_id,)).fetchone()
    if row is None:
        return jsonify({"error": f"issue {issue_id} no existe"}), 404
    return jsonify(dict(row))


@app.post("/issues")
def add_issue():
    data = request.get_json(silent=True) or {}
    missing = [f for f in ("title", "service", "severity") if not data.get(f)]
    if missing:
        return jsonify({"error": f"campos obligatorios: {', '.join(missing)}"}), 400
    if data["severity"] not in SEVERITIES:
        return jsonify({"error": f"severity inválida; valores: {sorted(SEVERITIES)}"}), 400
    status = data.get("status", "open")
    if status not in STATUSES:
        return jsonify({"error": f"status inválido; valores: {sorted(STATUSES)}"}), 400
    db = get_db()
    cur = db.execute(
        """INSERT INTO issues
           (title, service, severity, status, description, proposed_solution, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (data["title"], data["service"], data["severity"], status,
         data.get("description"), data.get("proposed_solution"), now_iso()),
    )
    db.commit()
    return jsonify({"id": cur.lastrowid}), 201


@app.put("/issues/<int:issue_id>")
def update_issue(issue_id):
    db = get_db()
    row = db.execute("SELECT * FROM issues WHERE id = ?", (issue_id,)).fetchone()
    if row is None:
        return jsonify({"error": f"issue {issue_id} no existe"}), 404
    data = request.get_json(silent=True) or {}
    if "severity" in data and data["severity"] not in SEVERITIES:
        return jsonify({"error": f"severity inválida; valores: {sorted(SEVERITIES)}"}), 400
    if "status" in data and data["status"] not in STATUSES:
        return jsonify({"error": f"status inválido; valores: {sorted(STATUSES)}"}), 400
    fields = {k: data[k] for k in ("status", "severity", "description", "proposed_solution") if k in data}
    if not fields:
        return jsonify({"error": "nada para actualizar"}), 400
    fields["updated_at"] = now_iso()
    sets = ", ".join(f"{k} = ?" for k in fields)
    db.execute(f"UPDATE issues SET {sets} WHERE id = ?", (*fields.values(), issue_id))
    db.commit()
    row = db.execute("SELECT * FROM issues WHERE id = ?", (issue_id,)).fetchone()
    return jsonify(dict(row))


if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5000, debug=True)
