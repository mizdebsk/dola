%bcond_with bootstrap

Name:           maven-plugin-testing
Version:        3.3.0
Release:        %autorelease
Summary:        Maven Plugin Testing
License:        Apache-2.0
URL:            https://maven.apache.org/plugin-testing/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://repo1.maven.org/maven2/org/apache/maven/plugin-testing/%{name}/%{version}/%{name}-%{version}-source-release.zip

Patch:          0001-Port-to-plexus-utils-3.0.21.patch
Patch:          0002-Port-to-current-maven-artifact.patch
Patch:          0003-Port-to-maven-3.8.1.patch
# From upstream commit 43b8eaaf
Patch:          0004-Stabilize-project.patch

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(commons-io:commons-io)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.maven:maven-aether-provider)
BuildRequires:  mvn(org.apache.maven:maven-compat)
BuildRequires:  mvn(org.apache.maven:maven-core)
BuildRequires:  mvn(org.apache.maven:maven-model)
BuildRequires:  mvn(org.apache.maven:maven-parent:pom:)
BuildRequires:  mvn(org.apache.maven:maven-plugin-api)
BuildRequires:  mvn(org.codehaus.plexus:plexus-archiver)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 3.3.0-55

%description
The Maven Plugin Testing contains the necessary modules
to be able to test Maven Plugins.

%package harness
Summary:        Maven Plugin Testing Mechanism

%description harness
The Maven Plugin Testing Harness provides mechanisms to manage tests on Mojo.

%prep
%autosetup -p1 -C


%pom_remove_plugin :maven-enforcer-plugin
%pom_remove_plugin :maven-site-plugin
%pom_remove_plugin :maven-source-plugin maven-plugin-testing-harness

%pom_disable_module maven-plugin-testing-tools
%pom_disable_module maven-test-tools

%mvn_alias : org.apache.maven.shared:

%build
%mvn_build -j -s -- -Dmaven.compiler.target=8

%install
%mvn_install

%files -f .mfiles-%{name}
%license LICENSE NOTICE

%files harness -f .mfiles-%{name}-harness

%changelog
%autochangelog
