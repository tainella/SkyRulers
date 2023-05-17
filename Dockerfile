FROM nvidia/cuda:11.5.1-base-ubuntu20.04

RUN apt-get update && \
    apt-get install -q -y \ 
    python3 \
    python3-pip \
    python-is-python3

RUN mkdir /data /model /src

RUN pip install --no-cache-dir --upgrade shiny \
    seaborn \
    lightgbm \
    pandas \
    numpy \
    shap \
    pint \
    shinyswatch \
    loguru

#веса моделей
COPY ./ML/models /models/
#код для отработки
COPY ./ML/src/pipeline.py /src/pipeline.py
COPY ./ML/src/preprocess.py /src/preprocess.py

COPY ./front/ /src
COPY ./data /data

CMD ["python", "-m", "shiny", "run", "--host", "0.0.0.0", "--port", "49903", "--reload", "/src/app.py"]



