%bcond_with bootstrap

Name:           maven-jar-plugin
Version:        3.3.0
Release:        %autorelease
Summary:        Maven JAR Plugin
License:        Apache-2.0
URL:            https://maven.apache.org/plugins/maven-jar-plugin/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://repo1.maven.org/maven2/org/apache/maven/plugins/%{name}/%{version}/%{name}-%{version}-source-release.zip

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.maven.plugin-testing:maven-plugin-testing-harness)
BuildRequires:  mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)
BuildRequires:  mvn(org.apache.maven.plugins:maven-plugin-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-plugins:pom:)
BuildRequires:  mvn(org.apache.maven.shared:file-management)
BuildRequires:  mvn(org.apache.maven:maven-archiver)
BuildRequires:  mvn(org.apache.maven:maven-artifact)
BuildRequires:  mvn(org.apache.maven:maven-compat)
BuildRequires:  mvn(org.apache.maven:maven-core)
BuildRequires:  mvn(org.apache.maven:maven-model)
BuildRequires:  mvn(org.apache.maven:maven-plugin-api)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 3.3.0-17

%description
Builds a Java Archive (JAR) file from the compiled
project classes and resources.

%prep
%autosetup -p1 -C
# System version of maven-jar-plugin should be used, not reactor version
%pom_xpath_inject pom:pluginManagement/pom:plugins "<plugin><artifactId>maven-jar-plugin</artifactId><version>SYSTEM</version></plugin>"

%build
%mvn_build -j

%install
%mvn_install

%files -f .mfiles
%license LICENSE NOTICE

%changelog
%autochangelog
