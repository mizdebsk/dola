%bcond_with bootstrap

Name:           maven-antrun-plugin
Version:        3.1.0
Release:        %autorelease
Summary:        Maven AntRun Plugin
License:        Apache-2.0
URL:            https://maven.apache.org/plugins/maven-antrun-plugin/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://repo1.maven.org/maven2/org/apache/maven/plugins/%{name}/%{version}/%{name}-%{version}-source-release.zip

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(org.apache.ant:ant)
BuildRequires:  mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)
BuildRequires:  mvn(org.apache.maven.plugins:maven-plugin-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-plugins:pom:)
BuildRequires:  mvn(org.apache.maven:maven-artifact)
BuildRequires:  mvn(org.apache.maven:maven-core)
BuildRequires:  mvn(org.apache.maven:maven-plugin-api)
BuildRequires:  mvn(org.codehaus.modello:modello-maven-plugin)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:  mvn(org.junit.jupiter:junit-jupiter-engine)
BuildRequires:  mvn(org.xmlunit:xmlunit-core)
BuildRequires:  mvn(org.xmlunit:xmlunit-matchers)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 3.1.0-23

%description
This plugin provides the ability to run Ant tasks from within Maven.
It is even possible to embed Ant scripts in the POM.

%prep
%autosetup -p1 -C

%build
%mvn_build -j

%install
%mvn_install

%files -f .mfiles
%license LICENSE NOTICE

%changelog
%autochangelog
