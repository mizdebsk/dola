%bcond_with bootstrap

Name:           jakarta-mail
Version:        2.1.3
Release:        %autorelease
Summary:        Jakarta Mail API
License:        EPL-2.0 OR GPL-2.0-only WITH Classpath-exception-2.0
URL:            https://jakarta.ee/specifications/mail/2.1/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://github.com/jakartaee/mail-api/archive/%{version}/mail-%{version}.tar.gz

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(jakarta.activation:jakarta.activation-api)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.codehaus.mojo:build-helper-maven-plugin)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 2.1.3-11

%description
Jakarta Mail defines a platform-independent and protocol-independent
framework to build mail and messaging applications.

%prep
%autosetup -p1 -C

pushd api
# Remove unnecessary dependency on parent POM
%pom_remove_parent

%pom_remove_plugin :buildnumber-maven-plugin

# Missing dependency
%pom_remove_dep :angus-activation
rm src/test/java/jakarta/mail/internet/NonAsciiFileNamesTest.java
popd

%build
pushd api
%mvn_build -j
popd

%install
pushd api
%mvn_install
popd

%files -f api/.mfiles
%license LICENSE.md NOTICE.md
%doc README.md

%changelog
%autochangelog
