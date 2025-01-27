Name:           jaxb-api
Version:        4.0.2
Release:        %autorelease
Summary:        Jakarta XML Binding API
License:        BSD-3-Clause
URL:            https://github.com/eclipse-ee4j/jaxb-api
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  maven-local
BuildRequires:  mvn(jakarta.activation:jakarta.activation-api)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.codehaus.mojo:build-helper-maven-plugin)
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 4.0.2-13

%description
The Jakarta XML Binding provides an API and tools that automate the mapping
between XML documents and Java objects.

%prep
%autosetup -p1 -C

# Remove unnecessary dependency on parent POM
%pom_remove_parent

%pom_remove_plugin -r :buildnumber-maven-plugin
%pom_remove_plugin -r :glassfish-copyright-maven-plugin
%pom_remove_plugin -r :maven-enforcer-plugin

%build
%mvn_build -j

%install
%mvn_install

%files -f .mfiles
%license LICENSE.md NOTICE.md

%changelog
%autochangelog
