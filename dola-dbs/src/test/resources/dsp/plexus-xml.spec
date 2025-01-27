%bcond_with bootstrap

Name:           plexus-xml
Version:        4.0.4
Release:        %autorelease
Summary:        Plexus XML Utilities
# Licensing breakdown:
# Apache-1.1: src/main/java/org/codehaus/plexus/util/xml/StringUtils.java
# xpp: src/main/java/org/codehaus/plexus/util/xml/pull/MXParser.java
# Everything else is Apache-2.0
License:        Apache-1.1 AND Apache-2.0 AND xpp
URL:            https://codehaus-plexus.github.io/plexus-xml/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://github.com/codehaus-plexus/%{name}/archive/%{name}-%{version}.tar.gz

# Baseid on upstream commit 1f1ff6f
Patch:          0001-Upgrade-to-Maven-4.0.0-rc-3.patch

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(org.apache.maven:maven-xml:4.0.0-rc-3)
BuildRequires:  mvn(org.codehaus.plexus:plexus:pom:)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 4.0.4-5

%description
A collection of various utility classes to ease working with XML.

%prep
%autosetup -p1 -C

%build
# Test dependencies are not packaged
%mvn_build -j -f

%install
%mvn_install

%files -f .mfiles
%doc README.md
%license NOTICE.txt LICENSE.txt

%changelog
%autochangelog
