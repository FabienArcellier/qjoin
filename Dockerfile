FROM python:3.10 as builder

RUN mkdir -p /app
WORKDIR /app
RUN pip3 install poetry

COPY . /app
RUN poetry install --without dev

FROM python:3.10-bullseye as base

COPY --from=builder /app /app

RUN groupadd --gid 1000 user && \
    useradd --create-home -u 1000 -g 1000 user && \
    chown -R user:user /app

USER user
WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH"
CMD ["python"]
