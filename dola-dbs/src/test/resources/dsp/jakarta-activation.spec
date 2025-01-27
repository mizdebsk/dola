%bcond_with bootstrap

Name:           jakarta-activation
Version:        2.1.3
Release:        %autorelease
Summary:        Jakarta Activation API
# the whole project is licensed under (EPL-2.0 or BSD)
# the source code additionally can be licensed under GPLv2 with exceptions
# we only ship built source code
License:        EPL-2.0 OR BSD-3-Clause OR GPL-2.0-only WITH Classpath-exception-2.0
URL:            https://jakarta.ee/specifications/activation/2.1/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://github.com/jakartaee/jaf-api/archive/%{version}/jaf-%{version}.tar.gz

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.codehaus.mojo:build-helper-maven-plugin)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 2.1.3-13

%description
Jakarta Activation defines a set of standard services to: determine
the MIME type of an arbitrary piece of data; encapsulate access to it;
discover the operations available on it; and instantiate the
appropriate bean to perform the operation(s).

%prep
%autosetup -p1 -C

pushd api
%pom_remove_parent

# remove custom doclet configuration
%pom_remove_plugin :maven-javadoc-plugin

%pom_remove_plugin -r :buildnumber-maven-plugin
%pom_remove_plugin -r :maven-enforcer-plugin
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
%doc README.md
%license LICENSE.md NOTICE.md

%changelog
%autochangelog
