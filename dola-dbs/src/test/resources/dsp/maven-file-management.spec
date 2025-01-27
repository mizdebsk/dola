%bcond_with bootstrap

Name:           maven-file-management
Epoch:          1
Version:        3.1.0
Release:        %autorelease
Summary:        Maven File Management API
License:        Apache-2.0
URL:            https://maven.apache.org/shared/file-management
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://repo1.maven.org/maven2/org/apache/maven/shared/file-management/%{version}/file-management-%{version}-source-release.zip

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(commons-io:commons-io)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.maven.shared:maven-shared-components:pom:)
BuildRequires:  mvn(org.codehaus.modello:modello-maven-plugin)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:  mvn(org.slf4j:slf4j-api)
BuildRequires:  mvn(org.slf4j:slf4j-simple)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 1:3.1.0-19

%description
Provides a component for plugins to easily resolve project dependencies.

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
