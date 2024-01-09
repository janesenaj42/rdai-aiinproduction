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
	
WORKDIR ${WORKDIR}

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
# Frontend
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt
	
# Set hugginface default directory
ENV HF_HOME=${WORKDIR}/huggingface
	
# Manually download the model as a docker layer for caching because it is taking too long via the AutoModelForCausalLM.from_pretrained() method
RUN python -m pip install huggingface-hub
RUN --mount=type=cache,target=/root/.cache/pip huggingface-cli download TheBloke/Llama-2-7b-Chat-GGUF llama-2-7b-chat.Q2_K.gguf

# Copy the source code into the container. Only copy relevant files.
COPY main.py main.py

# Change permissions of working directory to appuser
RUN chown ${GID}:${UID} -R ${WORKDIR}

# Expose the port that the application listens on.
EXPOSE 8000

# Switch to the non-privileged user to run the application.
USER appuser

# Run the application.
CMD ["bash", "-c", "python3 main.py"]
