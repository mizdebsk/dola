%bcond_with bootstrap

Name:           jakarta-cdi2.0
Version:        2.0.2
Release:        %autorelease
Summary:        Jakarta Contexts and Dependency Injection
License:        Apache-2.0
URL:            https://jakarta.ee/specifications/cdi/2.0/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://github.com/jakartaee/cdi/archive/%{version}.tar.gz

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(javax.inject:javax.inject)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 2.0.2-8
# Remove in Fedora 45
Obsoletes:      cdi-api < 2.0.2-16
Provides:       cdi-api = %{version}-%{release}

%description
Jakarta Contexts Dependency Injection specifies a means for obtaining
objects in such a way as to maximize reusability, testability and
maintainability compared to traditional approaches such as
constructors, factories, and service locators (e.g., JNDI).

%prep
%autosetup -p1 -C

%pom_remove_parent
%pom_remove_parent api
%pom_xpath_set pom:project/pom:groupId javax.enterprise api
%pom_xpath_set pom:project/pom:artifactId cdi-api api
%pom_disable_module spec
%pom_remove_plugin -r :maven-javadoc-plugin

%pom_change_dep jakarta.inject:jakarta.inject-api javax.inject:javax.inject api
%pom_remove_dep :jakarta.el-api api
%pom_remove_dep :jakarta.interceptor-api api
rm -rf api/src/main/java/javax/enterprise/{context/,inject/spi/,inject/se/,inject/Model.java,inject/New.java}

%mvn_package :cdi-parent __noinstall

%build
%mvn_build -j -f

%install
%mvn_install

%files -f .mfiles
%doc README.md
%license LICENSE.txt

%changelog
%autochangelog
