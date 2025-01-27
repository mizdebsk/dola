%bcond_with bootstrap

Name:           maven-assembly-plugin
Version:        3.7.1
Release:        %autorelease
Summary:        Maven Assembly Plugin
License:        Apache-2.0
URL:            https://maven.apache.org/plugins/maven-assembly-plugin/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://repo1.maven.org/maven2/org/apache/maven/plugins/%{name}/%{version}/%{name}-%{version}-source-release.zip

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(com.google.code.findbugs:jsr305)
BuildRequires:  mvn(commons-codec:commons-codec)
BuildRequires:  mvn(commons-io:commons-io)
BuildRequires:  mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)
BuildRequires:  mvn(org.apache.maven.plugins:maven-assembly-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-plugins:pom:)
BuildRequires:  mvn(org.apache.maven.shared:file-management)
BuildRequires:  mvn(org.apache.maven.shared:maven-artifact-transfer)
BuildRequires:  mvn(org.apache.maven.shared:maven-common-artifact-filters)
BuildRequires:  mvn(org.apache.maven.shared:maven-filtering)
BuildRequires:  mvn(org.apache.maven.shared:maven-shared-io)
BuildRequires:  mvn(org.apache.maven:maven-archiver)
BuildRequires:  mvn(org.apache.maven:maven-artifact)
BuildRequires:  mvn(org.apache.maven:maven-core)
BuildRequires:  mvn(org.apache.maven:maven-model)
BuildRequires:  mvn(org.apache.maven:maven-plugin-api)
BuildRequires:  mvn(org.codehaus.modello:modello-maven-plugin)
BuildRequires:  mvn(org.codehaus.plexus:plexus-archiver)
BuildRequires:  mvn(org.codehaus.plexus:plexus-component-annotations)
BuildRequires:  mvn(org.codehaus.plexus:plexus-component-metadata)
BuildRequires:  mvn(org.codehaus.plexus:plexus-interpolation)
BuildRequires:  mvn(org.codehaus.plexus:plexus-io)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:  mvn(org.eclipse.sisu:sisu-maven-plugin)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 3.7.1-12

%description
A Maven plugin to create archives of your project's sources, classes,
dependencies etc. from flexible assembly descriptors.

%prep
%autosetup -p1 -C

%pom_remove_dep jaxen:jaxen

%build
%mvn_build -j -f

%install
%mvn_install

%files -f .mfiles
%license LICENSE NOTICE

%changelog
%autochangelog
