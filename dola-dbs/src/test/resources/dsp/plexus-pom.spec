%bcond_with bootstrap

Name:           plexus-pom
Version:        18
Release:        %autorelease
Summary:        Root Plexus Projects POM
License:        Apache-2.0
URL:            https://github.com/codehaus-plexus/plexus-pom
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://github.com/codehaus-plexus/plexus-pom/archive/plexus-%{version}.tar.gz
Source1:        https://www.apache.org/licenses/LICENSE-2.0.txt

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
%endif

%description
The Plexus project provides a full software stack for creating and
executing software projects. This package provides parent POM for
Plexus packages.

%prep
%autosetup -p1 -C
cp -p %{SOURCE1} LICENSE

%pom_remove_dep org.junit:junit-bom
%pom_remove_plugin :maven-site-plugin
%pom_remove_plugin :maven-enforcer-plugin
%pom_remove_plugin :taglist-maven-plugin
%pom_remove_plugin :spotless-maven-plugin

%build
%mvn_build -j

%install
%mvn_install

%files -f .mfiles
%license LICENSE

%changelog
%autochangelog
