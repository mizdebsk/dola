%bcond_with bootstrap
%global upstream_version %(echo '%{version}' | tr '~' '-')

Name:           maven-surefire
Version:        3.2.2
Release:        %autorelease
Summary:        Test framework project
License:        Apache-2.0 AND CPL-1.0
URL:            https://maven.apache.org/surefire/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

# ./generate-tarball.sh
Source0:        %{name}-%{version}.tar.gz
# Remove bundled binaries which cannot be easily verified for licensing
Source1:        generate-tarball.sh
Source2:        https://junit.sourceforge.net/cpl-v10.html

Patch:          0001-Port-to-TestNG-7.4.0.patch
Patch:          0002-Disable-JUnit-4.8-test-grouping.patch

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(com.google.code.findbugs:jsr305)
BuildRequires:  mvn(commons-io:commons-io)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.commons:commons-compress)
BuildRequires:  mvn(org.apache.commons:commons-lang3)
BuildRequires:  mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)
BuildRequires:  mvn(org.apache.maven.plugins:maven-dependency-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-plugin-plugin) >= 3.6.4
BuildRequires:  mvn(org.apache.maven.shared:maven-common-artifact-filters)
BuildRequires:  mvn(org.apache.maven.shared:maven-shared-utils)
BuildRequires:  mvn(org.apache.maven:maven-core)
BuildRequires:  mvn(org.apache.maven:maven-parent:pom:)
BuildRequires:  mvn(org.apache.maven:maven-plugin-api)
BuildRequires:  mvn(org.codehaus.plexus:plexus-component-metadata)
BuildRequires:  mvn(org.codehaus.plexus:plexus-java)
BuildRequires:  mvn(org.eclipse.aether:aether-util)
BuildRequires:  mvn(org.eclipse.sisu:sisu-maven-plugin)
BuildRequires:  mvn(org.fusesource.jansi:jansi)
BuildRequires:  mvn(org.junit.platform:junit-platform-launcher)
BuildRequires:  mvn(org.testng:testng)
BuildRequires:  mvn(org.testng:testng::jdk15:)
%endif
# PpidChecker relies on /usr/bin/ps to check process uptime
Requires:       procps-ng
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 3.2.2-19

%description
Surefire is a test framework project.

%package plugin
Summary:        Surefire plugin for maven
Requires:       (%{name}-provider-junit = %{version}-%{release} if junit)
Requires:       (%{name}-provider-junit5 = %{version}-%{release} if junit5)
Requires:       (%{name}-provider-testng = %{version}-%{release} if testng)

%description plugin
Maven surefire plugin for running tests via the surefire framework.

%package provider-junit
Summary:        JUnit provider for Maven Surefire

%description provider-junit
JUnit provider for Maven Surefire.

%package provider-junit5
Summary:        JUnit 5 provider for Maven Surefire

%description provider-junit5
JUnit 5 provider for Maven Surefire.

%package provider-testng
Summary:        TestNG provider for Maven Surefire

%description provider-testng
TestNG provider for Maven Surefire.

%package -n maven-failsafe-plugin
Summary:        Maven plugin for running integration tests

%description -n maven-failsafe-plugin
The Failsafe Plugin is designed to run integration tests while the
Surefire Plugins is designed to run unit. The name (failsafe) was
chosen both because it is a synonym of surefire and because it implies
that when it fails, it does so in a safe way.

If you use the Surefire Plugin for running tests, then when you have a
test failure, the build will stop at the integration-test phase and
your integration test environment will not have been torn down
correctly.

The Failsafe Plugin is used during the integration-test and verify
phases of the build lifecycle to execute the integration tests of an
application. The Failsafe Plugin will not fail the build during the
integration-test phase thus enabling the post-integration-test phase
to execute.

%prep
%autosetup -p1 -C
cp -p %{SOURCE2} .


# Disable strict doclint
sed -i /-Xdoclint:all/d pom.xml

%pom_disable_module maven-surefire-report-plugin
%pom_disable_module surefire-report-parser
%pom_disable_module surefire-shadefire

%pom_disable_module surefire-grouper
%pom_remove_dep org.junit:junit-bom
%pom_remove_dep :surefire-grouper surefire-providers/common-junit48
%pom_remove_dep :surefire-grouper surefire-providers/surefire-testng-utils
rm surefire-providers/common-junit48/src/main/java/org/apache/maven/surefire/common/junit48/{FilterFactory,GroupMatcherCategoryFilter}.java
rm surefire-providers/surefire-testng-utils/src/main/java/org/apache/maven/surefire/testng/utils/GroupMatcherMethodSelector.java

%pom_remove_dep -r org.apache.maven.surefire:surefire-shadefire

# Help plugin is needed only to evaluate effective Maven settings.
# For building RPM package default settings will suffice.
%pom_remove_plugin :maven-help-plugin surefire-its

# QA plugin useful only for upstream
%pom_remove_plugin -r :jacoco-maven-plugin
# Not wanted
%pom_remove_plugin -r :maven-shade-plugin

find -name *.java -exec sed -i -e s/org.apache.maven.surefire.shared.utils/org.apache.maven.shared.utils/ -e s/org.apache.maven.surefire.shared.io/org.apache.commons.io/ -e s/org.apache.maven.surefire.shared.lang3/org.apache.commons.lang3/ -e s/org.apache.maven.surefire.shared.compress/org.apache.commons.compress/ {} \;

# Not in Fedora
%pom_remove_plugin -r :animal-sniffer-maven-plugin
# Complains
%pom_remove_plugin -r :apache-rat-plugin
# We don't need site-source
%pom_remove_plugin :maven-assembly-plugin maven-surefire-plugin
%pom_remove_dep -r ::::site-source

%build
%mvn_package ":*{surefire-plugin}*" @1
%mvn_package ":*junit-platform*" junit5
%mvn_package ":*{junit,testng,failsafe-plugin}*"  @1
%mvn_package ":*tests*" __noinstall
# tests turned off because they need jmock
%mvn_build -j -f

%install
%mvn_install

%files -f .mfiles
%doc README.md
%license LICENSE NOTICE cpl-v10.html

%files plugin -f .mfiles-surefire-plugin

%files provider-junit -f .mfiles-junit

%files provider-junit5 -f .mfiles-junit5

%files provider-testng -f .mfiles-testng

%files -n maven-failsafe-plugin -f .mfiles-failsafe-plugin

%changelog
%autochangelog
