%bcond_with bootstrap

Name:           maven-enforcer
Version:        3.5.0
Release:        %autorelease
Summary:        Maven Enforcer
License:        Apache-2.0
URL:            https://maven.apache.org/enforcer
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://repo1.maven.org/maven2/org/apache/maven/enforcer/enforcer/%{version}/enforcer-%{version}-source-release.zip

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(com.google.code.findbugs:jsr305)
BuildRequires:  mvn(commons-codec:commons-codec)
BuildRequires:  mvn(commons-io:commons-io)
BuildRequires:  mvn(javax.annotation:javax.annotation-api)
BuildRequires:  mvn(javax.inject:javax.inject)
BuildRequires:  mvn(org.apache.commons:commons-lang3)
BuildRequires:  mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)
BuildRequires:  mvn(org.apache.maven.plugins:maven-plugin-plugin)
BuildRequires:  mvn(org.apache.maven.resolver:maven-resolver-api)
BuildRequires:  mvn(org.apache.maven.resolver:maven-resolver-util)
BuildRequires:  mvn(org.apache.maven:maven-artifact)
BuildRequires:  mvn(org.apache.maven:maven-core)
BuildRequires:  mvn(org.apache.maven:maven-model)
BuildRequires:  mvn(org.apache.maven:maven-model-builder)
BuildRequires:  mvn(org.apache.maven:maven-parent:pom:)
BuildRequires:  mvn(org.apache.maven:maven-plugin-api)
BuildRequires:  mvn(org.apache.maven:maven-settings)
BuildRequires:  mvn(org.codehaus.plexus:plexus-classworlds)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:  mvn(org.codehaus.plexus:plexus-xml)
BuildRequires:  mvn(org.eclipse.sisu:org.eclipse.sisu.plexus)
BuildRequires:  mvn(org.eclipse.sisu:sisu-maven-plugin)
BuildRequires:  mvn(org.slf4j:slf4j-api)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 3.5.0-9

%description
Enforcer is a build rule execution framework.

%package api
Summary:        Enforcer API

%description api
This component provides the generic interfaces needed to
implement custom rules for the maven-enforcer-plugin.

%package rules
Summary:        Enforcer Rules

%description rules
This component contains the standard Enforcer Rules.

%package plugin
Summary:        Enforcer Plugin

%description plugin
The Enforcer plugin provides goals to control certain environmental
constraints such as Maven version, JDK version and OS family along
with many more built-in rules and user created rules.

%package extension
Summary:        Maven Enforcer Extension

%description extension
The Enforcer Extension provides a way to globally define rules without
making use of pom inheritence. This way you don't have to adjust the
pom.xml, but you can enforce a set of rules.

%prep
%autosetup -p1 -C
find -name '*.java' -exec sed -i 's/\r//' {} +

find -name EvaluateBeanshell.java -delete

%pom_remove_dep :bsh enforcer-rules

%build
# Use system version of maven-enforcer-plugin instead of reactor version
%mvn_build -j -s -f -- -Dversion.maven-enforcer-plugin=SYSTEM

%install
%mvn_install

%files -f .mfiles-enforcer
%license LICENSE NOTICE

%files api -f .mfiles-enforcer-api
%license LICENSE NOTICE

%files rules -f .mfiles-enforcer-rules

%files plugin -f .mfiles-maven-enforcer-plugin

%files extension -f .mfiles-maven-enforcer-extension

%changelog
%autochangelog
