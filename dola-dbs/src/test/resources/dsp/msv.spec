Name:           msv
Version:        2022.7
Release:        %autorelease
Summary:        Multi-Schema Validator Toolkit
# License breakdown
# Apache-1.1
# * xsdlib/src/main/java/com/sun/msv/datatype/regexp - All files except for InternalImpl.java
# BSD-3-Clause-Sun
# * pom.xml
# * xsdlib/src/main/java/com/sun/msv/datatype/regexp/InternalImpl.java
# BSD-3-Clause-Sun implied by docs/xsdlib/license.txt of the original tarball
# * xsdlib/src/main/java/com/sun/msv/datatype/xsd/CommandLineTester.java
# * xsdlib/src/main/resources/com/sun/msv/datatype/xsd/Messages.properties
# * xsdlib/src/main/resources/com/sun/msv/datatype/xsd/Messages_ja.properties
# BSD-3-Clause - All other .java files
License:        Apache-1.1 AND BSD-3-Clause AND BSD-3-Clause-Sun
URL:            https://xmlark.github.io/msv/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

# ./generate-tarball.sh
Source0:        %{name}-%{version}.tar.gz
Source1:        generate-tarball.sh

Patch:          0001-Disable-Apache-XercesImpl.patch

BuildRequires:  maven-local
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-assembly-plugin)
BuildRequires:  mvn(org.jdom:jdom2)
BuildRequires:  mvn(relaxngDatatype:relaxngDatatype)
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 2022.7-15

%description
The Multi Schema Validation toolkit is a Java based toolkit consisting of 8
different submodules. The core module is the Multi-Schema XML Validator (MSV)
for the validation of XML documents against several kinds of XML schemata The
core supports RELAX NG, RELAX Namespace, RELAX Core, TREX, XML DTDs, and a
subset of XML Schema Part 1.

%package xsdlib
Summary:        Java implementation of W3C’s XML Schema Part 2

%description xsdlib
MSV XML Datatypes Library, Java implementation of W3C’s XML Schema Part 2, is
intended for use with applications that incorporate XML Schema Part 2.

%prep
%autosetup -p1 -C

# Disable runtime dependency on Apache Xerces
rm xsdlib/src/main/java/com/sun/msv/datatype/xsd/regex/XercesImpl.java

%pom_xpath_remove 'pom:project/pom:modules'
%pom_xpath_inject 'pom:project' '<modules><module>xsdlib</module></modules>'

%pom_xpath_remove 'pom:build/pom:extensions'

%pom_remove_dep org.apache.maven.scm:maven-scm-provider-gitexe
%pom_remove_dep xerces:xercesImpl xsdlib

%pom_remove_plugin org.codehaus.mojo:flatten-maven-plugin
%pom_remove_plugin -r :maven-javadoc-plugin

# We only build xsdlib
%mvn_package net.java.dev.msv:msv __noinstall

%build
%mvn_build -j -s

%install
%mvn_install

%files xsdlib -f .mfiles-xsdlib
%doc README.md README-xsdlib.md
%license Apache-LICENSE-1.1.txt license.txt

%changelog
%autochangelog
