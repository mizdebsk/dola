%bcond_with bootstrap

Name:           felix-parent
Version:        9
Release:        %autorelease
Summary:        Parent POM file for Apache Felix Specs
License:        Apache-2.0
URL:            https://felix.apache.org/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://repo1.maven.org/maven2/org/apache/felix/felix-parent/%{version}/%{name}-%{version}-source-release.tar.gz

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(org.apache:apache:pom:)
%endif

%description
Parent POM file for Apache Felix Specs.

%prep
%autosetup -p1 -C
%mvn_alias : :felix
%pom_remove_plugin :maven-enforcer-plugin
%pom_remove_plugin :maven-javadoc-plugin
%pom_remove_plugin :maven-site-plugin
%pom_remove_plugin :maven-release-plugin
%pom_remove_plugin :apache-rat-plugin
%pom_remove_plugin :animal-sniffer-maven-plugin
%pom_remove_plugin org.apache.geronimo.genesis.plugins:tools-maven-plugin

# wagon ssh dependency unneeded
%pom_xpath_remove pom:extensions

%build
%mvn_build -j

%install
%mvn_install

%files -f .mfiles
%doc LICENSE NOTICE

%changelog
%autochangelog
