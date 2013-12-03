Name:          restlet-jse
Version:       2.1.4
Release:       1%{?dist}
Summary:       Open Source Lightweight REST framework
License:       ASL 2.0 and CDDL and EPL and LGPLv2+ and LGPLv3+
URL:           http://restlet.org/
# sh restlet-jse-create-tarball.sh < VERSION >
Source0:       %{name}-%{version}-clean.tar.xz
Source1:       %{name}-create-tarball.sh
Source2:       http://maven.restlet.org/org/restlet/jee/org.restlet.parent/%{version}/org.restlet.parent-%{version}.pom

BuildRequires: java-devel
BuildRequires: mvn(cglib:cglib)
BuildRequires: mvn(com.sun.xml.bind:jaxb-impl)
BuildRequires: mvn(com.thoughtworks.xstream:xstream)
BuildRequires: mvn(commons-dbcp:commons-dbcp)
BuildRequires: mvn(commons-fileupload:commons-fileupload)
BuildRequires: mvn(commons-pool:commons-pool)
BuildRequires: mvn(commons-lang:commons-lang)
BuildRequires: mvn(commons-logging:commons-logging)
BuildRequires: mvn(javax.mail:mail)
BuildRequires: mvn(javax.servlet:servlet-api)
BuildRequires: mvn(javax.xml.bind:jaxb-api)
BuildRequires: mvn(javax.xml.stream:stax-api)
BuildRequires: mvn(junit:junit)
BuildRequires: mvn(net.jcip:jcip-annotations)
BuildRequires: mvn(org.apache.httpcomponents:httpclient)
BuildRequires: mvn(org.apache.httpcomponents:httpcore)
BuildRequires: mvn(org.apache.httpcomponents:httpmime)
BuildRequires: mvn(org.apache.james:apache-mime4j-core)
BuildRequires: mvn(org.apache.james:james-project)
BuildRequires: mvn(org.apache.velocity:velocity)
BuildRequires: mvn(org.codehaus.jackson:jackson-core-asl)
BuildRequires: mvn(org.codehaus.jackson:jackson-mapper-asl)
BuildRequires: mvn(org.codehaus.jettison:jettison)
BuildRequires: mvn(org.freemarker:freemarker)
BuildRequires: mvn(org.jdom:jdom)
BuildRequires: mvn(org.jibx:jibx-run)
BuildRequires: mvn(org.jsslutils:jsslutils)
BuildRequires: mvn(org.slf4j:slf4j-api)
BuildRequires: mvn(org.springframework:spring-beans)
BuildRequires: mvn(org.springframework:spring-context)
BuildRequires: mvn(org.springframework:spring-core)
BuildRequires: mvn(org.springframework:spring-expression)
BuildRequires: mvn(org.springframework:spring-web)
BuildRequires: mvn(org.springframework:spring-webmvc)
BuildRequires: mvn(rome:rome)

BuildRequires: maven-local

BuildArch:     noarch
# JSON, A GWT port of the client-side
#library is also available.
%description
Restlet is a lightweight, comprehensive, REST framework for the
Java platform. Restlet is suitable for both server and client
Web applications. It supports major Internet transport, data
format, and service description standards like HTTP and HTTPS,
SMTP, XML, Atom, and WADL. 

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q
cp -p %{SOURCE2} pom.xml
# Require org.restlet.lib.com.db4o*
%pom_disable_module org.restlet.example
# Require org.json:json:2.0
%pom_disable_module org.restlet.ext.json
%pom_disable_module org.restlet.ext.jaxrs
%pom_disable_module org.restlet.ext.openid
%pom_disable_module org.restlet.ext.oauth
# Require com.google.gwt:gwt-servlet:2.3.0
%pom_disable_module org.restlet.ext.gwt
# Require lucene-core 2.9.2 org.apache.solr:solr-core,solr-solrj 1.4.0 org.apache.tika:tika-core,tika-parsers 0.6
%pom_disable_module org.restlet.ext.lucene
# Require org.eclipse.emf
%pom_disable_module org.restlet.ext.emf
%pom_disable_module org.restlet.ext.sdc
%pom_disable_module org.restlet.test

# Adapt for newer mime4j
%pom_remove_dep org.apache.james:apache-mime4j org.restlet.ext.httpclient
%pom_add_dep org.apache.james:apache-mime4j-core:0.7.2 org.restlet.ext.httpclient
# Use system jvm apis
%pom_remove_dep javax.activation:activation org.restlet.ext.javamail
# Remove unavailable dep
%pom_remove_dep :spring-asm org.restlet.ext.spring
# Fix cglib aId
%pom_xpath_set "pom:project/pom:dependencies/pom:dependency[pom:groupId = 'cglib' ]/pom:artifactId" cglib org.restlet.ext.spring

sed -i 's/\r//' changes.txt readme.txt



%build

%mvn_build

%install
%mvn_install

# TODO ./bin/linux/restlet.sh

%files -f .mfiles
%dir %{_javadir}/%{name}
%doc changes.txt copyright.txt license.txt readme.txt trademarks.txt

%files javadoc -f .mfiles-javadoc
%doc copyright.txt license.txt trademarks.txt

%changelog
* Sun Oct 27 2013 gil cattaneo <puntogil@libero.it> 2.1.4-1
- update to 2.1.4

* Wed Aug 28 2013 gil cattaneo <puntogil@libero.it> 2.1.3-1
- initial rpm