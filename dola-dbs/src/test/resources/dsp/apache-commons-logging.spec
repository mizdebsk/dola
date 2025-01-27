%bcond_with bootstrap

Name:           apache-commons-logging
Version:        1.3.4
Release:        %autorelease
Summary:        Apache Commons Logging
License:        Apache-2.0
URL:            https://commons.apache.org/proper/commons-logging/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://www.apache.org/dist/commons/logging/source/commons-logging-%{version}-src.tar.gz

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(javax.servlet:javax.servlet-api)
BuildRequires:  mvn(org.apache.commons:commons-parent:pom:)
BuildRequires:  mvn(org.apache.logging.log4j:log4j-1.2-api)
BuildRequires:  mvn(org.apache.logging.log4j:log4j-api)
BuildRequires:  mvn(org.apache.maven.plugins:maven-antrun-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-dependency-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-enforcer-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-failsafe-plugin)
BuildRequires:  mvn(org.moditect:moditect-maven-plugin)
BuildRequires:  mvn(org.slf4j:slf4j-api)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 1.3.4-8

%description
The commons-logging package provides a simple, component oriented
interface (org.apache.commons.logging.Log) together with wrappers for
logging systems. The user can choose at runtime which system they want
to use. In addition, a small number of basic implementations are
provided to allow users to use the package standalone.
commons-logging was heavily influenced by Avalon's Logkit and Log4J. The
commons-logging abstraction is meant to minimize the differences between
the two, and to allow a developer to not tie himself to a particular
logging implementation.

%prep
%autosetup -p1 -C

%pom_remove_dep :avalon-framework
%pom_remove_dep :logkit
rm src/main/java/org/apache/commons/logging/impl/AvalonLogger.java
rm src/main/java/org/apache/commons/logging/impl/LogKitLogger.java
rm -r src/test/java/org/apache/commons/logging/{avalon,logkit}
rm src/test/java/org/apache/commons/logging/pathable/{Parent,Child}FirstTestCase.java

# Avoid hard-coded versions in OSGi metadata
%pom_xpath_set "pom:properties/pom:commons.osgi.import" '*;resolution:=optional'

%pom_remove_plugin :cobertura-maven-plugin
%pom_remove_plugin :maven-scm-publish-plugin

sed -i 's/\r//' RELEASE-NOTES.txt LICENSE.txt NOTICE.txt

# for compatibility reasons
%mvn_file ":commons-logging{*}" "commons-logging@1" "%{name}@1"
%mvn_alias ":commons-logging{*}" "org.apache.commons:commons-logging@1" "apache:commons-logging@1"

%mvn_package ":::{*}:"

# Remove log4j12 tests
rm -rf src/test/java/org/apache/commons/logging/log4j/log4j12

%build
# missing test dependencies
%mvn_build -j -f

%install
%mvn_install

%files -f .mfiles
%license LICENSE.txt NOTICE.txt
%doc PROPOSAL.html RELEASE-NOTES.txt

%changelog
%autochangelog
