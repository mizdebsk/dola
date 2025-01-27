%bcond_with bootstrap

Name:           jakarta-servlet
Version:        5.0.0
Release:        %autorelease
Summary:        Jakarta Servlet
# most of the project is EPL-2.0 or GPLv2 w/exceptions,
# but some files still have Apache-2.0 license headers:
# https://github.com/eclipse-ee4j/servlet-api/issues/347
License:        (EPL-2.0 OR GPL-2.0-only WITH Classpath-exception-2.0) AND Apache-2.0
URL:            https://jakarta.ee/specifications/servlet/5.0/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://github.com/jakartaee/servlet/archive/%{version}-RELEASE/servlet-api-%{version}.tar.gz

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.codehaus.mojo:build-helper-maven-plugin)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 5.0.0-37
Provides:       glassfish-servlet-api = %{version}-%{release}

%description
Jakarta Servlet defines a server-side API for handling HTTP requests
and responses.

%prep
%autosetup -p1 -C

# remove unnecessary dependency on parent POM
%pom_remove_parent . api

# do not build specification documentation
%pom_disable_module spec

# Copy to old package name
# TODO: Remove when all dependencies are migrated from javax.servlet to jakarta.servlet
cp -pr api/src/main/java/jakarta api/src/main/java/javax
sed -i -e 's/jakarta\./javax./g' $(find api/src/main/java/javax -name *.java)
%pom_xpath_replace pom:instructions/pom:Export-Package \
  '<Export-Package>jakarta.servlet.*,javax.servlet.*;version="4.0.0"</Export-Package>' api

# do not install useless parent POM
%mvn_package jakarta.servlet:servlet-parent __noinstall

# remove unnecessary maven plugins
%pom_remove_plugin -r :formatter-maven-plugin
%pom_remove_plugin -r :impsort-maven-plugin
%pom_remove_plugin -r :maven-enforcer-plugin
%pom_remove_plugin -r :maven-javadoc-plugin
%pom_remove_plugin -r :maven-source-plugin

# add maven artifact coordinate aliases for backwards compatibility
%mvn_alias jakarta.servlet:jakarta.servlet-api \
    javax.servlet:javax.servlet-api \
    javax.servlet:servlet-api

# add compat symlink for packages constructing the classpath manually
%mvn_file :{*} %{name}/@1 glassfish-servlet-api

%build
%mvn_build -j

%install
%mvn_install

%files -f .mfiles
%license LICENSE.md NOTICE.md
%doc README.md

%changelog
%autochangelog
