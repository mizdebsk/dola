Name:           jaxb-fi
Version:        2.1.1
Release:        %autorelease
Summary:        Implementation of the Fast Infoset Standard for Binary XML
# jaxb-fi is licensed Apache-2.0 and EDL-1.0 (BSD-3-Clause)
# bundled org.apache.xerces.util.XMLChar.java is licensed ASL 1.1
License:        Apache-2.0 AND BSD-3-Clause AND Apache-1.1
URL:            https://github.com/eclipse-ee4j/jaxb-fi
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  maven-local
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-assembly-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-dependency-plugin)
BuildRequires:  mvn(org.codehaus.mojo:build-helper-maven-plugin)
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 2.1.1-17

%description
Fast Infoset Project, an Open Source implementation of the Fast Infoset
Standard for Binary XML.

The Fast Infoset specification (ITU-T Rec. X.891 | ISO/IEC 24824-1)
describes an open, standards-based "binary XML" format that is based on
the XML Information Set.

%package tests
Summary:        FastInfoset Roundtrip Tests
License:        Apache-2.0 AND BSD-3-Clause

%description tests
%{summary}.

%prep
%autosetup -p1 -C

%pom_remove_parent

%pom_disable_module samples
%pom_disable_module utilities

%pom_remove_plugin :buildnumber-maven-plugin
%pom_remove_plugin :glassfish-copyright-maven-plugin
%pom_remove_plugin :maven-enforcer-plugin

%mvn_package :FastInfosetRoundTripTests tests

%build
%mvn_build -j

%install
%mvn_install

%files -f .mfiles
%license LICENSE NOTICE.md
%doc README.md

%files tests -f .mfiles-tests
%license LICENSE NOTICE.md

%changelog
%autochangelog
