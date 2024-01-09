# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/engine/reference/builder/

ARG PYTHON_VERSION=3.10
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

ARG WORKDIR=/appuser

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user
ARG UID=10001
ARG GID=10001

RUN addgroup --gid ${GID} appuser

RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "${WORKDIR}" \
    --shell "/sbin/nologin" \
    #--no-create-home \
    --uid "${UID}" \
	--gid "${GID}" \
    appuser
	
RUN chown ${GID}:${UID} ${WORKDIR}

WORKDIR ${WORKDIR}

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# Switch to the non-privileged user to run the application.
USER appuser

# Copy the source code into the container. Only copy relevant files.
COPY app.py app.py

ARG GRADIO_SERVER_PORT=7860
ENV GRADIO_SERVER_PORT=${GRADIO_SERVER_PORT}

ENV HF_HOME=${WORKDIR}/huggingface

# Expose the port that the application listens on.
EXPOSE ${GRADIO_SERVER_PORT}

# Run the application.
CMD python3 app.py
