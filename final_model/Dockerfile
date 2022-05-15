# Use pytorch GPU base image
# FROM gcr.io/cloud-aiplatform/training/pytorch-gpu.1-7
FROM us-docker.pkg.dev/vertex-ai/training/tf-gpu.2-8

# set working directory
WORKDIR /app

# Install required packages
RUN pip install google-cloud-storage cloudml-hypertune

# Copies the trainer code to the docker image.
COPY ./__init__.py /app/trainer/__init__.py
COPY ./utils.py /app/trainer/utils.py
COPY ./metadata.py /app/trainer/metadata.py
COPY ./model.py /app/trainer/model.py
COPY ./task.py /app/trainer/task.py

# Set up the entry point to invoke the trainer.
ENTRYPOINT ["python", "-m", "trainer.task"]