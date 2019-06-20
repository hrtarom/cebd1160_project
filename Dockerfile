
FROM ubuntu:latest
RUN apt-get update \
    && apt-get install -y python3-pip \
    && pip3 install --upgrade pip

RUN pip3 install numpy pandas matplotlib seaborn plotly sklearn

COPY Final-Project-LogReg.py .






CMD ["python3","-u","Final-Project-LogReg.py"]





