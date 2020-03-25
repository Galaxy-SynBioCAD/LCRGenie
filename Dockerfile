FROM python:3.7

WORKDIR /home/

RUN git clone https://github.com/neilswainston/LCRGenie
RUN mv LCRGenie/lcr_genie /home/
RUN mv LCRGenie/requirements.txt /home/
RUN rm -r LCRGenie

# Install Python dependencies:
RUN pip install --upgrade pip \
  && pip install -r /home/requirements.txt
