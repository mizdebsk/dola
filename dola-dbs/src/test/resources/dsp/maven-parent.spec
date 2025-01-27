%bcond_with bootstrap

Name:           maven-parent
Version:        43
Release:        %autorelease
Summary:        Apache Maven parent POM
License:        Apache-2.0
URL:            https://maven.apache.org
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://repo1.maven.org/maven2/org/apache/maven/%{name}/%{version}/%{name}-%{version}-source-release.zip

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)
BuildRequires:  mvn(org.apache.maven.plugins:maven-enforcer-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-plugin-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-remote-resources-plugin)
BuildRequires:  mvn(org.apache:apache:pom:)
BuildRequires:  mvn(org.codehaus.plexus:plexus-component-metadata)
%endif

%description
Apache Maven parent POM file used by other Maven projects.

%prep
%autosetup -p1 -C
%pom_remove_plugin :maven-enforcer-plugin
%pom_remove_plugin :maven-checkstyle-plugin
%pom_remove_plugin :apache-rat-plugin
%pom_remove_plugin :spotless-maven-plugin
%pom_remove_plugin -r :maven-site-plugin
%pom_remove_plugin -r :maven-scm-publish-plugin
%pom_remove_dep :junit-bom

%pom_xpath_remove "pom:execution[pom:id='generate-helpmojo']" maven-plugins

%build
%mvn_build -j

%install
%mvn_install

%files -f .mfiles
%doc LICENSE NOTICE

%changelog
%autochangelog
