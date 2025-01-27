%bcond_with bootstrap

Name:           fusesource-pom
Version:        1.12
Release:        %autorelease
Summary:        Parent POM for FuseSource Maven projects
License:        Apache-2.0
URL:            https://fusesource.com/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://github.com/fusesource/mvnplugins/archive/refs/tags/fusesource-pom-%{version}.tar.gz

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
%endif

%description
This is a shared POM parent for FuseSource Maven projects.

%prep
%autosetup -p1 -C
mv fusesource-pom/pom.xml .

%pom_remove_plugin :maven-scm-plugin

# WebDAV wagon is not available in Fedora.
%pom_xpath_remove "pom:extension[pom:artifactId[text()='wagon-webdav-jackrabbit']]"

%build
%mvn_build -j

%install
%mvn_install

%files -f .mfiles
%license license.txt notice.txt

%changelog
%autochangelog
