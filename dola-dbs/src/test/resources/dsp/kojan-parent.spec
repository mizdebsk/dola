%bcond_with bootstrap

Name:           kojan-parent
Version:        6
Release:        %autorelease
Summary:        Maven parent POM for io.kojan
License:        Apache-2.0
URL:            https://github.com/mizdebsk/kojan-parent
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://github.com/mizdebsk/kojan-parent/archive/refs/tags/6.tar.gz#/%{name}-%{version}.tar.gz

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
%endif

%description
Parent Maven POM file for io.kojan organization.

%prep
%autosetup -p1 -C
%pom_remove_plugin :spotless-maven-plugin

%build
%mvn_build -j

%install
%mvn_install

%files -f .mfiles
%license LICENSE

%changelog
%autochangelog
