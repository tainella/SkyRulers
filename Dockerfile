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
    pint

#веса моделей
COPY ./ML/models /models/
#код для отработки
COPY ./ML/src/pipeline.py /src/pipeline.py
COPY ./ML/src/preprocess.py /src/preprocess.py
#файл с описанием фичей для отдельных групп flight_mode+engine_family
COPY ./ML/data/feature_groups.json /data/feature_groups.json
COPY ./ML/data/needed.json /data/needed.json

#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]



