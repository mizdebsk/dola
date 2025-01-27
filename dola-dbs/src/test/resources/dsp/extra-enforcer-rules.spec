%bcond_with bootstrap

Name:           extra-enforcer-rules
Version:        1.8.0
Release:        %autorelease
Summary:        Extra rules for maven-enforcer-plugin
License:        Apache-2.0
URL:            https://github.com/mojohaus/extra-enforcer-rules
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://repo1.maven.org/maven2/org/codehaus/mojo/extra-enforcer-rules/%{version}/extra-enforcer-rules-%{version}-source-release.zip

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(commons-codec:commons-codec)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.maven.enforcer:enforcer-api)
BuildRequires:  mvn(org.apache.maven.shared:maven-common-artifact-filters)
BuildRequires:  mvn(org.apache.maven.shared:maven-dependency-tree)
BuildRequires:  mvn(org.apache.maven:maven-core)
BuildRequires:  mvn(org.codehaus.mojo:mojo-parent:pom:)
BuildRequires:  mvn(org.eclipse.sisu:sisu-maven-plugin)
BuildRequires:  mvn(org.mockito:mockito-core)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 1.8.0-11

%description
Apache's Maven Enforcer Plugin is used to apply and enforce rules on Maven
projects. The Enforcer plugin ships with a set of standard rules. This project
provides extra rules which are not part of the standard rule set.

%prep
%autosetup -p1 -C

# Integration tests fetch upstream poms
%pom_remove_plugin :maven-invoker-plugin

%build
%mvn_build -j

%install
%mvn_install

%files -f .mfiles
%license LICENSE.txt
%doc README.md

%changelog
%autochangelog
