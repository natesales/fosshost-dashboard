FROM tiangolo/uvicorn-gunicorn:python3.7

# Set up working directory
RUN mkdir -p /usr/share/fosshost-dashboard
WORKDIR /usr/share/fosshost-dashboard

# Copy source
COPY . /usr/share/fosshost-dashboard

# Install deps
RUN pip install -r requirements.txt
