FROM python:3.8

WORKDIR /

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        xvfb \
        xauth \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . ./

ENTRYPOINT [ "xvfb-run", "python /timelapse.py" ]
