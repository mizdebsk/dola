%bcond_with bootstrap

Name:           apache-parent
Version:        33
Release:        %autorelease
Summary:        Parent POM file for Apache projects
License:        Apache-2.0
URL:            https://apache.org/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://repo1.maven.org/maven2/org/apache/apache/%{version}/apache-%{version}-source-release.zip

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(org.apache.maven.plugins:maven-enforcer-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-remote-resources-plugin)
%endif
%if %{without bootstrap}
# Not generated automatically
BuildRequires:  mvn(org.apache.apache.resources:apache-jar-resource-bundle)
%endif
Requires:       mvn(org.apache.apache.resources:apache-jar-resource-bundle)

%description
This package contains the parent pom file for apache projects.

%prep
%autosetup -p1 -C

%pom_remove_plugin :maven-site-plugin
%pom_remove_plugin :maven-site-plugin docs
%pom_remove_plugin :maven-scm-publish-plugin docs

%build
%mvn_build -j

%install
%mvn_install

%files -f .mfiles
%license LICENSE NOTICE

%changelog
%autochangelog
