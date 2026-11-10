FROM python@sha256:935c3c5b12357a7e10caa9c1e6ca5692344d97cf229832ef584be2cec9fc03df
ENV PYTHONDONTWRITEBYTECODE=1 PIP_NO_CACHE_DIR=1
COPY requirements.lock /opt/experiment/requirements.lock
# Named build context contains only the reviewed wheels, never model assets.
RUN --mount=type=bind,from=wheels,target=/wheels,ro \
    python -m pip install --no-index --find-links=/wheels --only-binary=:all: \
      --require-hashes -r /opt/experiment/requirements.lock && python -m pip check
COPY run.py runtime_checks.py verify_artifacts.py model-manifest.json /opt/experiment/
USER 1000:1000
WORKDIR /results
CMD ["python", "/opt/experiment/run.py"]
