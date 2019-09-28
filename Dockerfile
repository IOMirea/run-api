FROM python:3.7-alpine

# enables proper stdout flushing
ENV PYTHONUNBUFFERED 1

# pip optimizations
ENV PIP_NO_CACHE_DIR 1
ENV PIP_DISABLE_PIP_VERSION_CHECK 1

WORKDIR /code

# avoid cache invalidation after copying entire directory
COPY requirements.txt .

RUN apk add --no-cache --virtual build-deps \
        git \
        gcc \
        make \
        musl-dev && \
    pip install -r requirements.txt && \
    apk del build-deps

EXPOSE 8080

COPY . .

RUN addgroup -S iomirea && \
    adduser -S run-api-public -G iomirea && \
    chown -R run-api-public:iomirea /code

USER run-api-public

ENTRYPOINT ["python", "-m", "run_api"]