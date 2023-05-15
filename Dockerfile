FROM mambaorg/micromamba:1.4.2

# maintainer details
MAINTAINER Patrick Sadil "psadil1@jh.edu"

COPY --chown=$MAMBA_USER:$MAMBA_USER env.yml /tmp/env.yml

RUN micromamba install -y -n base -f /tmp/env.yml && \
    micromamba clean --all --yes

# make the python script executable
COPY --chown=$MAMBA_USER:$MAMBA_USER embed_html_images.py /usr/local/bin/embed_html_images.py
RUN ["chmod", "+x", "/usr/local/bin/embed_html_images.py"]

ENTRYPOINT ["/usr/local/bin/_entrypoint.sh", "python", "/usr/local/bin/embed_html_images.py"]

