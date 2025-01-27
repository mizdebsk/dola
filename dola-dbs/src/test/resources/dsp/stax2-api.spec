%bcond_with bootstrap

Name:           stax2-api
Version:        4.2.2
Release:        %autorelease
Summary:        Streaming API for XML
License:        BSD-2-Clause
URL:            https://github.com/FasterXML/stax2-api
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        %{url}/archive/%{name}-%{version}.tar.gz

# From upstream commit 67d5988
Patch:          0001-Add-BSD-2-license-file.patch

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 4.2.2-6

%description
Stax2 API is an extension to standard Java Streaming API for XML
(StAX) added in JDK 6.

%prep
%autosetup -p1 -C
%pom_remove_parent
%pom_xpath_remove pom:Import-Package
%pom_remove_plugin :maven-javadoc-plugin
%pom_remove_plugin :moditect-maven-plugin

%build
%mvn_build -j -- -Djavac.src.version=8 -Djavac.target.version=8

%install
%mvn_install

%files -f .mfiles
%doc README.md
%license LICENSE

%changelog
%autochangelog
