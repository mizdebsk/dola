%bcond_with bootstrap

Name:           jakarta-annotations
Version:        1.3.5
Release:        %autorelease
Summary:        Jakarta Annotations
License:        EPL-2.0 OR GPL-2.0-only WITH Classpath-exception-2.0
URL:            https://jakarta.ee/specifications/annotations/1.3/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://github.com/jakartaee/common-annotations-api/archive/%{version}/common-annotations-api-%{version}.tar.gz

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.codehaus.mojo:build-helper-maven-plugin)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 1.3.5-41
Provides:       glassfish-annotation-api = %{version}-%{release}

%description
Jakarta Annotations defines a collection of annotations representing
common semantic concepts that enable a declarative style of
programming that applies across a variety of Java technologies.

%prep
%autosetup -p1 -C

# remove unnecessary dependency on parent POM
# org.eclipse.ee4j:project is not packaged and isn't needed
%pom_remove_parent

# disable spec submodule: it's not needed, and
# it has missing dependencies (jruby, asciidoctor-maven-plugin, ...)
%pom_disable_module spec

# remove plugins not needed for RPM builds
%pom_remove_plugin :maven-javadoc-plugin api
%pom_remove_plugin :maven-source-plugin api
%pom_remove_plugin :findbugs-maven-plugin api

# Remove use of spec-version-maven-plugin
%pom_remove_plugin :spec-version-maven-plugin api
%pom_xpath_set pom:Bundle-Version '${project.version}' api
%pom_xpath_set pom:Bundle-SymbolicName '${project.artifactId}' api
%pom_xpath_set pom:Extension-Name '${extension.name}' api
%pom_xpath_set pom:Implementation-Version '${project.version}' api
%pom_xpath_set pom:Specification-Version '${spec.version}' api

# provide aliases for the old artifact coordinates
%mvn_alias jakarta.annotation:jakarta.annotation-api \
  javax.annotation:javax.annotation-api \
  javax.annotation:jsr250-api

%build
%mvn_build -j

%install
%mvn_install

%files -f .mfiles
%license LICENSE.md NOTICE.md
%doc README.md

%changelog
%autochangelog
