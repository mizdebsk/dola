%bcond_with bootstrap

Name:           apache-commons-jxpath
Version:        1.3
Release:        %autorelease
Summary:        Simple XPath interpreter
License:        Apache-2.0
URL:            https://commons.apache.org/proper/commons-jxpath/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        http://www.apache.org/dist/commons/jxpath/source/commons-jxpath-%{version}-src.tar.gz

Patch:          commons-jxpath-mockrunner.patch

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(commons-beanutils:commons-beanutils)
BuildRequires:  mvn(jdom:jdom)
BuildRequires:  mvn(org.apache.commons:commons-parent:pom:)
BuildRequires:  mvn(org.apache.maven.plugins:maven-assembly-plugin)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 1.3-77

%description
Defines a simple interpreter of an expression language called XPath.
JXPath applies XPath expressions to graphs of objects of all kinds:
JavaBeans, Maps, Servlet contexts, DOM etc, including mixtures thereof.

%prep
%autosetup -p1 -C

%pom_remove_dep xerces:
%pom_remove_dep xml-apis:

# Remove dependency on glassfish
%pom_remove_dep :servlet-api
%pom_remove_dep :jsp-api
rm src/java/org/apache/commons/jxpath/servlet/*Context*.java
rm src/java/org/apache/commons/jxpath/servlet/*Handler.java
rm src/test/org/apache/commons/jxpath/servlet/JXPathServletContextTest.java

%mvn_file ":{*}" %{name} @1
%mvn_alias : org.apache.commons:

%pom_xpath_inject 'pom:properties' \
  '<commons.osgi.import>org.apache.commons.beanutils;resolution:="optional",org.jdom*;resolution:="optional",org.w3c.dom;resolution:="optional",javax.servlet*;resolution:="optional",*</commons.osgi.import>'

%build
# we are skipping tests because we don't have com.mockrunner in repos yet
%mvn_build -j -f -- -Dcommons.packageId=jxpath

%install
%mvn_install

%files -f .mfiles
%license LICENSE.txt NOTICE.txt

%changelog
%autochangelog
