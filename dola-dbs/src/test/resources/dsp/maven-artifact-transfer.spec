%bcond_with bootstrap

Name:           maven-artifact-transfer
Epoch:          1
Version:        0.13.1
Release:        %autorelease
Summary:        Apache Maven Artifact Transfer
License:        Apache-2.0
URL:            https://maven.apache.org/shared/maven-artifact-transfer
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://repo1.maven.org/maven2/org/apache/maven/shared/%{name}/%{version}/%{name}-%{version}-source-release.zip

Patch:          0001-Compatibility-with-Maven-3.0.3-and-later.patch
Patch:          0002-Remove-support-for-maven-3.0.X.patch
Patch:          0003-Port-to-maven-3.8.1.patch
# From upstream commit 75a99b21
Patch:          0004-Bump-maven-shared-components-from-34-to-37.patch

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(commons-codec:commons-codec)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.maven.shared:maven-common-artifact-filters)
BuildRequires:  mvn(org.apache.maven.shared:maven-shared-components:pom:)
BuildRequires:  mvn(org.apache.maven:maven-artifact)
BuildRequires:  mvn(org.apache.maven:maven-core)
BuildRequires:  mvn(org.codehaus.plexus:plexus-component-annotations)
BuildRequires:  mvn(org.codehaus.plexus:plexus-component-metadata)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:  mvn(org.eclipse.aether:aether-api)
BuildRequires:  mvn(org.eclipse.aether:aether-impl)
BuildRequires:  mvn(org.eclipse.aether:aether-util)
BuildRequires:  mvn(org.mockito:mockito-core)
BuildRequires:  mvn(org.slf4j:slf4j-api)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 1:0.13.1-34

%description
An API to either install or deploy artifacts with Maven 3.

%prep
%autosetup -p1 -C
find -name '*.java' -exec sed -i 's/\r//' {} +

%pom_remove_plugin :apache-rat-plugin
%pom_remove_plugin :maven-shade-plugin
%pom_remove_plugin :animal-sniffer-maven-plugin

# We don't want to support legacy Maven versions (older than 3.1)
%pom_remove_dep org.sonatype.aether:
find -name Maven30\*.java -delete

%build
%mvn_build -j -- -DjavaVersion=8

%install
%mvn_install

%files -f .mfiles
%license LICENSE NOTICE

%changelog
%autochangelog
