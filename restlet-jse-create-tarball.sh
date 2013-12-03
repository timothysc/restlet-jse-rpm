#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: ./create-sources VERSION"
    exit 1
fi

VERSION=${1}
NAME="restlet-jse"
MAJOR_VERSION=$(echo ${VERSION} | cut -d. -f 1-2)

wget http://restlet.org/download/${MAJOR_VERSION}/${NAME}-${VERSION}.zip
unzip -qq ${NAME}-${VERSION}.zip
rm ${NAME}-${VERSION}.zip
# Remove unused files
rm -Rf ./${NAME}-${VERSION}/bin/conf
rm -Rf ./${NAME}-${VERSION}/bin/linux/wrapper
rm -Rf ./${NAME}-${VERSION}/bin/win
rm -Rf ./${NAME}-${VERSION}/docs/*
rm -Rf ./${NAME}-${VERSION}/lib
find ./${NAME}-${VERSION} -name "*.jar" -delete
find ./${NAME}-${VERSION} -name "*.class" -delete
cd ./${NAME}-${VERSION}

#wget http://maven.restlet.org/org/restlet/jee/org.restlet.parent/${VERSION}/org.restlet.parent-${VERSION}.pom
#mv org.restlet.parent-${VERSION}.pom pom.xml

mv src/* .

for m in org.restlet \
 org.restlet.example \
 org.restlet.ext.atom \
 org.restlet.ext.crypto \
 org.restlet.ext.dataservices \
 org.restlet.ext.emf \
 org.restlet.ext.fileupload \
 org.restlet.ext.freemarker \
 org.restlet.ext.gson \
 org.restlet.ext.gwt \
 org.restlet.ext.html \
 org.restlet.ext.httpclient \
 org.restlet.ext.jaas \
 org.restlet.ext.jackson \
 org.restlet.ext.javamail \
 org.restlet.ext.jaxb \
 org.restlet.ext.jaxrs \
 org.restlet.ext.jdbc \
 org.restlet.ext.jibx \
 org.restlet.ext.json \
 org.restlet.ext.lucene \
 org.restlet.ext.net \
 org.restlet.ext.netty \
 org.restlet.ext.oauth \
 org.restlet.ext.odata \
 org.restlet.ext.openid \
 org.restlet.ext.rdf \
 org.restlet.ext.rome \
 org.restlet.ext.sdc \
 org.restlet.ext.sip \
 org.restlet.ext.slf4j \
 org.restlet.ext.spring \
 org.restlet.ext.ssl \
 org.restlet.ext.velocity \
 org.restlet.ext.wadl \
 org.restlet.ext.xml \
 org.restlet.ext.xstream \
 org.restlet.test; do
(
cd ${m}

mkdir -p src
mv org src

[ -d META-INF/services]; mv META-INF src/
wget -O pom.xml http://maven.restlet.org/org/restlet/jee/${m}/${VERSION}/${m}-${VERSION}.pom

)

done

mkdir -p org.restlet.ext.servlet

(
cd org.restlet.ext.servlet
wget -O pom.xml http://maven.restlet.org/org/restlet/jee/org.restlet.ext.servlet/${VERSION}/org.restlet.ext.servlet-${VERSION}.pom
wget http://maven.restlet.org/org/restlet/jee/org.restlet.ext.servlet/${VERSION}/org.restlet.ext.servlet-${VERSION}-sources.jar
jar -xf org.restlet.ext.servlet-${VERSION}-sources.jar
rm -R org.restlet.ext.servlet-${VERSION}-sources.jar META-INF
mkdir -p src
mv org src
)

mkdir -p org.restlet.ext.xdb

(
cd org.restlet.ext.xdb
wget -O pom.xml http://maven.restlet.org/org/restlet/jee/org.restlet.ext.xdb/${VERSION}/org.restlet.ext.xdb-${VERSION}.pom
wget http://maven.restlet.org/org/restlet/jee/org.restlet.ext.xdb/${VERSION}/org.restlet.ext.xdb-${VERSION}-sources.jar
jar -xf org.restlet.ext.xdb-${VERSION}-sources.jar
rm -R org.restlet.ext.xdb-${VERSION}-sources.jar META-INF
mkdir -p src
mv org src
mv resources src/
)

rm -Rf org.restlet.ext.jetty
rm -Rf org.restlet.ext.simple
# require jetty 7.0.0.v20091005
#(
#cd org.restlet.ext.jetty
#JETTY_VERSION=2.0-M6
#wget -O pom.xml http://maven.restlet.org/org/restlet/jee/org.restlet.ext.jetty/${JETTY_VERSION}/org.restlet.ext.jetty-${JETTY_VERSION}.pom
#sed -i "s|2.0-M6|${VERSION}|" pom.xml
#mkdir -p src
#mv org src
#)
# disable for now
#(
#cd org.restlet.ext.simple
#SIMPLE_VERSION=2.0-M6
#wget -O pom.xml http://maven.restlet.org/org/restlet/jee/org.restlet.ext.simple/${SIMPLE_VERSION}/org.restlet.ext.simple-${SIMPLE_VERSION}.pom
#sed -i "s|2.0-M6|${VERSION}|" pom.xml
#mkdir -p src
#mv org src
#)

cd ..
find ./${NAME}-${VERSION} -name "*.jar" -delete
find ./${NAME}-${VERSION} -name "MANIFEST.MF" -delete

tar cJf ${NAME}-${VERSION}-clean.tar.xz ./${NAME}-${VERSION}