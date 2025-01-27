%bcond_with bootstrap

Name:           slf4j2
Version:        2.0.17
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
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-source-plugin)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 2.0.16-4

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

%package jdk-platform-logging
Summary:        SLF4J Platform Logging Binding

%description jdk-platform-logging
SLF4J Platform Logging Binding.

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

%prep
%autosetup -p1 -C
find -name '*.jar' -delete
install -p -m 0644 %{SOURCE1} LICENSE-2.0.txt

%pom_disable_module integration
%pom_disable_module osgi-over-slf4j
%pom_disable_module slf4j-ext
%pom_disable_module slf4j-log4j12
%pom_disable_module slf4j-reload4j

# dos2unix
find -name '*.css' -o -name '*.js' -o -name '*.txt' -exec sed -i 's/\r//' {} +

# Remove wagon-ssh build extension
%pom_xpath_remove pom:extensions parent

%mvn_package :::sources: __noinstall
%mvn_package :slf4j-bom __noinstall
%mvn_package :slf4j-parent __noinstall
%mvn_package :slf4j-site __noinstall
%mvn_package :slf4j-api
%mvn_package :slf4j-simple
%mvn_package :slf4j-nop

%mvn_compat_version : 2.0.17

%build
%mvn_build -j -f -s -j -- -Drequired.jdk.version=1.8

%install
# Compat symlinks
%mvn_file ':slf4j-{*}' %{name}/slf4j-@1 %{name}/@1

%mvn_install

%files -f .mfiles
%license LICENSE.txt LICENSE-2.0.txt

%files jdk14 -f .mfiles-slf4j-jdk14

%files jdk-platform-logging -f .mfiles-slf4j-jdk-platform-logging

%files -n jcl-over-%{name} -f .mfiles-jcl-over-slf4j

%files -n jul-to-%{name} -f .mfiles-jul-to-slf4j

%files -n log4j-over-%{name} -f .mfiles-log4j-over-slf4j

%files migrator -f .mfiles-slf4j-migrator

%changelog
%autochangelog
