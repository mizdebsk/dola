Name:           jaxb-stax-ex
Version:        2.1.0
Release:        %autorelease
Summary:        Extended StAX API
License:        BSD-3-Clause
URL:            https://github.com/eclipse-ee4j/jaxb-stax-ex
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  maven-local
BuildRequires:  mvn(jakarta.activation:jakarta.activation-api)
BuildRequires:  mvn(jakarta.xml.bind:jakarta.xml.bind-api)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.codehaus.mojo:build-helper-maven-plugin)
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 2.1.0-22

%description
This project contains a few extensions to complement JSR-173 StAX API in
the following areas:

- Enable parser instance reuse (which is important in the
  high-performance environment like Eclipse Implementation of JAXB and
  Eclipse Metro)
- Improve the support for reading from non-text XML infoset, such as
  FastInfoset.
- Improve the namespace support.

%prep
%autosetup -p1 -C

%pom_remove_parent

%pom_remove_plugin :buildnumber-maven-plugin
%pom_remove_plugin :glassfish-copyright-maven-plugin
%pom_remove_plugin :maven-enforcer-plugin

%build
%mvn_build -j

%install
%mvn_install

%files -f .mfiles
%license LICENSE.md NOTICE.md
%doc README.md

%changelog
%autochangelog
