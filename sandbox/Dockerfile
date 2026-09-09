FROM python:3.12-slim

RUN pip install --no-cache-dir pytest==8.3.4

RUN useradd --create-home --uid 1002 sandbox
USER sandbox

WORKDIR /rad

CMD ["pytest", "-v", "--tb=short"]