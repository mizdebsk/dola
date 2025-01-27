%bcond_with bootstrap

Name:           slf4j
Version:        1.7.36
Release:        %autorelease
Summary:        Simple Logging Facade for Java
# the log4j-over-slf4j and jcl-over-slf4j submodules are ASL 2.0, rest is MIT
License:        MIT AND Apache-2.0
URL:            https://www.slf4j.org/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://github.com/qos-ch/slf4j/archive/v_%{version}.tar.gz
Source1:        https://www.apache.org/licenses/LICENSE-2.0.txt

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(commons-logging:commons-logging)
BuildRequires:  mvn(org.apache.maven.plugins:maven-antrun-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-source-plugin)
BuildRequires:  mvn(org.codehaus.mojo:build-helper-maven-plugin)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 1.7.36-13
Obsoletes:      %{name}-manual < 1.7.36-13

%description
The Simple Logging Facade for Java or (SLF4J) is intended to serve
as a simple facade for various logging APIs allowing to the end-user
to plug in the desired implementation at deployment time. SLF4J also
allows for a gradual migration path away from
Jakarta Commons Logging (JCL).

Logging API implementations can either choose to implement the
SLF4J interfaces directly, e.g. NLOG4J or SimpleLogger. Alternatively,
it is possible (and rather easy) to write SLF4J adapters for the given
API implementation, e.g. Log4jLoggerAdapter or JDK14LoggerAdapter..

%package jdk14
Summary:        SLF4J JDK14 Binding

%description jdk14
SLF4J JDK14 Binding.

%package jcl
Summary:        SLF4J JCL Binding

%description jcl
SLF4J JCL Binding.

%package -n jcl-over-%{name}
Summary:        JCL 1.1.1 implemented over SLF4J

%description -n jcl-over-%{name}
JCL 1.1.1 implemented over SLF4J.

%package -n jul-to-%{name}
Summary:        JUL to SLF4J bridge

%description -n jul-to-%{name}
JUL to SLF4J bridge.

%package -n log4j-over-%{name}
Summary:        Log4j implemented over SLF4J

%description -n log4j-over-%{name}
Log4j implemented over SLF4J.

%package migrator
Summary:        SLF4J Migrator

%description migrator
SLF4J Migrator.

%package sources
Summary:        SLF4J Source JARs

%description sources
SLF4J Source JARs.

%prep
%autosetup -p1 -C
find -name '*.jar' -delete
install -p -m 0644 %{SOURCE1} LICENSE-2.0.txt

%pom_disable_module integration
%pom_disable_module osgi-over-slf4j
%pom_disable_module slf4j-android
%pom_disable_module slf4j-ext
%pom_disable_module slf4j-log4j12
%pom_disable_module slf4j-reload4j

# Port to maven-antrun-plugin 3.0.0
sed -i s/tasks/target/ slf4j-api/pom.xml

# Because of a non-ASCII comment in slf4j-api/src/main/java/org/slf4j/helpers/MessageFormatter.java
%pom_xpath_inject "pom:project/pom:properties" "
    <project.build.sourceEncoding>ISO-8859-1</project.build.sourceEncoding>"

# Fix javadoc links
%pom_xpath_remove "pom:links"
%pom_xpath_inject "pom:plugin[pom:artifactId[text()='maven-javadoc-plugin']]/pom:configuration" "
    <detectJavaApiLink>false</detectJavaApiLink>
    <isOffline>false</isOffline>
    <links><link>/usr/share/javadoc/java</link></links>"

# dos2unix
find -name '*.css' -o -name '*.js' -o -name '*.txt' -exec sed -i 's/\r//' {} +

# Remove wagon-ssh build extension
%pom_xpath_remove pom:extensions

# The general pattern is that the API package exports API classes and does
# not require impl classes. slf4j was breaking that causing "A cycle was
# detected when generating the classpath slf4j.api, slf4j.nop, slf4j.api."
# The API bundle requires impl package, so to avoid cyclic dependencies
# during build time, it is necessary to mark the imported package as an
# optional one.
# Reported upstream: http://bugzilla.slf4j.org/show_bug.cgi?id=283
sed -i '/Import-Package/s/\}$/};resolution:=optional/' slf4j-api/src/main/resources/META-INF/MANIFEST.MF

# Source JARs for are required by Maven 3.4.0
%mvn_package :::sources: sources

%mvn_package :slf4j-parent __noinstall
%mvn_package :slf4j-site __noinstall
%mvn_package :slf4j-api
%mvn_package :slf4j-simple
%mvn_package :slf4j-nop

# Compat symlinks
%mvn_file ':slf4j-{*}' %{name}/slf4j-@1 %{name}/@1

%build
%mvn_build -j -f -s -- -Drequired.jdk.version=1.8

%install
%mvn_install

%files -f .mfiles
%license LICENSE.txt LICENSE-2.0.txt

%files jdk14 -f .mfiles-slf4j-jdk14

%files jcl -f .mfiles-slf4j-jcl

%files -n jcl-over-%{name} -f .mfiles-jcl-over-slf4j

%files -n jul-to-%{name} -f .mfiles-jul-to-slf4j

%files -n log4j-over-%{name} -f .mfiles-log4j-over-slf4j

%files migrator -f .mfiles-slf4j-migrator

%files sources -f .mfiles-sources
%license LICENSE.txt LICENSE-2.0.txt

%changelog
%autochangelog
