FROM redmine:6

USER root
RUN apt-get update && apt-get install -y git build-essential --no-install-recommends     && rm -rf /var/lib/apt/lists/*

RUN git clone --depth 1 https://github.com/haru/redmine_ai_helper.git     /usr/src/redmine/plugins/redmine_ai_helper

WORKDIR /usr/src/redmine
RUN HOME=/root bundle install --without development test     && chown -R redmine:redmine /usr/local/bundle     && chown redmine:redmine Gemfile.lock
