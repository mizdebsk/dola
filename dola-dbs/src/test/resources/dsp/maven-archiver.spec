%bcond_with bootstrap

Name:           maven-archiver
Version:        3.6.2
Release:        %autorelease
Summary:        Maven Archiver
License:        Apache-2.0
URL:            https://maven.apache.org/shared/maven-archiver/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://repo1.maven.org/maven2/org/apache/maven/%{name}/%{version}/%{name}-%{version}-source-release.zip

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(org.apache.maven.shared:maven-shared-components:pom:)
BuildRequires:  mvn(org.apache.maven:maven-core)
BuildRequires:  mvn(org.assertj:assertj-core)
BuildRequires:  mvn(org.codehaus.plexus:plexus-archiver)
BuildRequires:  mvn(org.codehaus.plexus:plexus-interpolation)
BuildRequires:  mvn(org.junit.jupiter:junit-jupiter-api)
BuildRequires:  mvn(org.junit.jupiter:junit-jupiter-params)
BuildRequires:  mvn(org.mockito:mockito-core)
BuildRequires:  mvn(org.slf4j:slf4j-simple)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 3.6.2-7

%description
The Maven Archiver is used by other Maven plugins
to handle packaging

%prep
%autosetup -p1 -C
%pom_remove_dep :junit-bom

%build
%mvn_build -j

%install
%mvn_install

%files -f .mfiles
%doc README.md
%license LICENSE NOTICE

%changelog
%autochangelog
