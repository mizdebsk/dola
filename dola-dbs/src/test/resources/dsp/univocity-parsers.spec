%bcond_with bootstrap

Name:           univocity-parsers
Version:        2.9.1
Release:        %autorelease
Summary:        Collection of parsers for Java
License:        Apache-2.0
URL:            https://github.com/uniVocity/univocity-parsers
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://github.com/uniVocity/univocity-parsers/archive/v%{version}.tar.gz

Patch:          0001-Resolve-import-clash-with-OpenJDK-17.patch

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-source-plugin)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 2.9.1-31

%description
uniVocity-parsers is a suite of extremely fast and reliable parsers
for Java.  It provides a consistent interface for handling different
file formats, and a solid framework for the development of new
parsers.

%prep
%autosetup -p1 -C

%pom_remove_plugin :nexus-staging-maven-plugin
%pom_remove_plugin :maven-compiler-plugin
%pom_remove_plugin :maven-javadoc-plugin

%build
# Tests require univocity-output-tester, which is not packaged yet.
%mvn_build -j -f -- -Dmaven.compiler.source=1.8 -Dmaven.compiler.target=1.8

%install
%mvn_install

%files -f .mfiles
%doc README.md
%license LICENSE-2.0.html

%changelog
%autochangelog
