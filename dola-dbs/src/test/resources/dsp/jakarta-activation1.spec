%bcond_with bootstrap

Name:           jakarta-activation1
Version:        1.2.2
Release:        %autorelease
Summary:        Jakarta Activation API 1.2
License:        BSD-3-Clause
URL:            https://jakarta.ee/specifications/activation/1.2/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://github.com/jakartaee/jaf-api/archive/%{version}/jaf-%{version}.tar.gz

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-dependency-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-source-plugin)
BuildRequires:  mvn(org.codehaus.mojo:build-helper-maven-plugin)
%endif

%description
Jakarta Activation defines a set of standard services to: determine
the MIME type of an arbitrary piece of data; encapsulate access to it;
discover the operations available on it; and instantiate the
appropriate bean to perform the operation(s).

%prep
%autosetup -p1 -C

%pom_remove_parent
%pom_disable_module demo

%pom_remove_plugin -r :maven-enforcer-plugin

%pom_remove_plugin :directory-maven-plugin
sed -i 's/${main.basedir}/${basedir}/' pom.xml

# Remove custom doclet configuration
%pom_remove_plugin :maven-javadoc-plugin activation

# Set bundle version manually instead of with osgiversion-maven-plugin
# (the plugin is only used to strip off -SNAPSHOT or -Mx qualifiers)
%pom_remove_plugin :osgiversion-maven-plugin
sed -i "s/\${activation.osgiversion}/%{version}/g" activation/pom.xml

%mvn_compat_version jakarta*: 1 %{version} 1.2.1 1.2.0 1.1.1

# TODO delete
%mvn_file com.sun.activation:jakarta.activation %{name}/jakarta.activation javax.activation

%build
# Javadoc fails:
# /builddir/build/BUILD/jaf-api-1.2.2/activation/src/main/java/module-info.java:11: error: duplicate module: jakarta.activation
%mvn_build -j

%install
%mvn_install

%files -f .mfiles
%doc README.md
%license LICENSE.md NOTICE.md

%changelog
%autochangelog
