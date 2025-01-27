%bcond_with bootstrap

Name:           apache-commons-cli
Version:        1.9.0
Release:        %autorelease
Summary:        Command Line Interface Library for Java
License:        Apache-2.0
URL:            https://commons.apache.org/proper/commons-cli/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://www.apache.org/dist/commons/cli/source/commons-cli-%{version}-src.tar.gz

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(commons-io:commons-io)
BuildRequires:  mvn(org.apache.commons:commons-parent:pom:)
BuildRequires:  mvn(org.apache.maven.plugins:maven-antrun-plugin)
BuildRequires:  mvn(org.junit.jupiter:junit-jupiter-api)
BuildRequires:  mvn(org.junit.jupiter:junit-jupiter-engine)
BuildRequires:  mvn(org.junit.jupiter:junit-jupiter-params)
BuildRequires:  mvn(org.mockito:mockito-core)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 1.9.0-7

%description
The CLI library provides a simple and easy to use API for working with the
command line arguments and options.

%prep
%autosetup -p1 -C

# Compatibility links
%mvn_alias : org.apache.commons:commons-cli
%mvn_file : commons-cli %{name}

%build
%mvn_build -j

%install
%mvn_install

%files -f .mfiles
%license LICENSE.txt NOTICE.txt
%doc README.md RELEASE-NOTES.txt

%changelog
%autochangelog
