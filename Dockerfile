
FROM ubuntu:latest
RUN apt-get update \
    && apt-get install -y python3-pip \
    && pip3 install --upgrade pip

RUN pip3 install numpy pandas matplotlib seaborn plotly sklearn
COPY Final-project-data-investigation.py .
COPY Final-project-LogReg.py .





CMD ["python3","-u","Final-project-data-investigation.py"]
CMD ["python3","-u","final-project-LogReg.py"]





