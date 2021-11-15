# pull base docker image
FROM python:3.8.1-slim-buster

# maintainer details
MAINTAINER Shweta Gopal "sgopal@tacc.utexas.edu"

# copy source files
COPY . /opt/app

# set working directory
WORKDIR /opt/app

# install dependencies
RUN pip3 install -r requirements.txt

# copy the python script into root directory
COPY embed_html_images.py /usr/local/bin

# make the python script executable
RUN ["chmod", "+x", "/usr/local/bin/embed_html_images.py"]

# set environment variable path to detect python executable script
ENV PATH="/usr/local/bin:${PATH}"

# set the command to display a help message on how to use this image
CMD echo "To use this image: docker run -v /hostdirectory_with_html_file:/data reshg/process-html-images:1.0 embed_html_images.py -i /data/sample.html -o /data/out.html"

