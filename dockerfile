FROM jenkins/jenkins:lts-jdk11

ENV JENKINS_OPTS --httpPort=-1 --httpsPort=8090 --prefix=umlJenkins --httpsKeyStore=/var/lib/jenkins/certificate.pfx --httpsKeyStorePassword=Password12
EXPOSE 8090


