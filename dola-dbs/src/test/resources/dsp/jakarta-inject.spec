%bcond_with bootstrap

Name:           jakarta-inject
Version:        2.0.1
Release:        %autorelease
Summary:        Jakarta Dependency Injection
License:        Apache-2.0
URL:            https://jakarta.ee/specifications/dependency-injection/2.0/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://github.com/jakartaee/inject/archive/%{version}.tar.gz

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 2.0.1-6

%description
Jakarta Dependency Injection specifies a means for obtaining objects
in such a way as to maximize reusability, testability and
maintainability compared to traditional approaches such as
constructors, factories, and service locators (e.g., JNDI).
This process, known as dependency injection, is beneficial
to most nontrivial applications.

%prep
%autosetup -p1 -C

%pom_remove_parent
%pom_remove_plugin :maven-javadoc-plugin

%build
%mvn_build -j

%install
%mvn_install

%files -f .mfiles
%license LICENSE.txt NOTICE.md

%changelog
%autochangelog
