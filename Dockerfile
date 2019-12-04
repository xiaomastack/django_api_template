FROM centos:centos7.4.1708

ENV MICRO_APP_NAME={{cookiecutter.project_name}} MICRO_APP_PORT=8080

ADD . /data/${MICRO_APP_NAME}

WORKDIR /data/${MICRO_APP_NAME}

RUN rm -f /etc/yum.repos.d/* \
  && curl -o /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo \
  && sed -i 's#http://mirrors.aliyuncs.com#http://mirrors.aliyun.com#g' /etc/yum.repos.d/CentOS-Base.repo \
  && sed -i 's#http://mirrors.cloud.aliyuncs.com#http://mirrors.aliyun.com#g' /etc/yum.repos.d/CentOS-Base.repo \
  && curl -o /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-7.repo \
  && sed -i 's#http://mirrors.aliyuncs.com#http://mirrors.aliyun.com#g' /etc/yum.repos.d/epel.repo \
  && sed -i 's#http://mirrors.cloud.aliyuncs.com#http://mirrors.aliyun.com#g' /etc/yum.repos.d/epel.repo \
  && rpm  --import  /etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-7 \
  && yum clean all \
  && yum makecache \
  && yum -y install python-pip \
  && pip install --upgrade pip \
  && rm -f /etc/localtime \
  && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
  && mv /data/${MICRO_APP_NAME}/uwsgi.ini /etc/uwsgi.ini \
  && yum -y install mariadb-devel \
  && yum -y install gcc \
  && yum -y install python-devel \
  && pip install -r /data/${MICRO_APP_NAME}/requirements.txt \
  && pip install uWSGI==2.0.18 \
  && yum history list gcc|grep 'install'|awk '{print $1}'|xargs yum history undo -y \
  && yum history list python-devel|grep 'install'|awk '{print $1}'|xargs yum history undo -y \
  && rm -rf /root/.cache/pip \
  && yum clean all \
  && rm -rf /var/cache/yum \
  && python manage.py collectstatic --noinput

EXPOSE ${MICRO_APP_PORT}

ENTRYPOINT [ "/usr/bin/uwsgi", "--ini", "/etc/uwsgi.ini"]
