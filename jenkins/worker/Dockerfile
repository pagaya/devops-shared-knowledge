FROM ubuntu:18.04

ENV TERRAFORM_VERSION=1.0.2


RUN apt update && apt install -y curl unzip software-properties-common jq git make wget

# Install yq
RUN add-apt-repository ppa:rmescandon/yq -y && apt install yq

# Install Docker
RUN curl https://get.docker.com | bash

# Install kubectl
RUN curl -LO https://dl.k8s.io/release/v1.21.0/bin/linux/amd64/kubectl \
&& chmod +x kubectl && mv kubectl /usr/local/bin/kubectl

# Install helm
RUN curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash

# Install awscli
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
&& unzip awscliv2.zip && ./aws/install && rm -rf awscliv2.zip ./aws

# Install python3
RUN add-apt-repository ppa:deadsnakes/ppa && apt-get update \
&& apt-get install -y python3.8 && apt install -y python3.8-distutils

# Install terraform
RUN curl -fsSL https://apt.releases.hashicorp.com/gpg | apt-key add - \
&& apt-add-repository "deb [arch=$(dpkg --print-architecture)] https://apt.releases.hashicorp.com $(lsb_release -cs) main" \
&& apt install -y terraform=${TERRAFORM_VERSION}

# Install Nodejs
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash - \
  && apt install -y nodejs

# Install aws-iam-authenticator
RUN curl -o /usr/local/bin/aws-iam-authenticator https://amazon-eks.s3-us-west-2.amazonaws.com/1.21.2/2021-07-05/bin/linux/amd64/aws-iam-authenticator \
&& chmod +x /usr/local/bin/aws-iam-authenticator

ENTRYPOINT ["bash"]