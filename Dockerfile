# ── DVWA Brute Force Lab ──────────────────────────────────────────────────────
# Intentionally vulnerable Flask app for cybersecurity education.
# DO NOT deploy on a public-facing server.
# ─────────────────────────────────────────────────────────────────────────────

FROM python:3.12-slim

LABEL maintainer="cybersec-instructor"
LABEL description="DVWA-style Brute Force Lab — educational use only"

# ── System deps ──
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ── App directory ──
WORKDIR /app

# ── Install Python dependencies ──
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Copy application code ──
COPY app.py .
COPY templates/ templates/
COPY static/ static/

# ── Expose port — Railway overrides this with $PORT at runtime ──
EXPOSE ${PORT:-5000}

# ── Health check — must use $PORT so it matches whatever Railway assigns ──
HEALTHCHECK --interval=15s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:${PORT:-5000}/ || exit 1

# ── Run with Gunicorn bound to $PORT ──
# gunicorn is already in requirements.txt
CMD gunicorn --bind 0.0.0.0:${PORT:-5000} --workers 1 app:app
