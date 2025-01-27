%bcond_with bootstrap

Name:           apache-resource-bundles
Epoch:          1
Version:        1.5
Release:        %autorelease
Summary:        Apache Resource Bundles
License:        Apache-2.0
URL:            https://maven.apache.org/apache-resource-bundles/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://repo1.maven.org/maven2/org/apache/apache/resources/apache-resource-bundles/%{version}/apache-resource-bundles-%{version}-source-release.zip

Patch:          0001-Port-ITs-to-Maven-Verifier-2.0.0-M1.patch
# From upstream commit 5eab384b
Patch:          0002-MASFRES-68-Upgrade-parent-pom-to-42.patch

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.maven.plugins:maven-remote-resources-plugin)
BuildRequires:  mvn(org.apache.maven.shared:maven-verifier)
BuildRequires:  mvn(org.apache.maven:maven-parent:pom:)
BuildRequires:  mvn(org.codehaus.plexus:plexus-archiver)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)
%endif

%description
An archive which contains templates for generating the necessary license files
and notices for all Apache releases.

%prep
%autosetup -p1 -C
%pom_disable_module resources-bundles-sample
%mvn_alias :apache-jar-resource-bundle org.apache:

%build
# Use system version of apache-resource-bundles instead of reactor version
%mvn_build -j -- -Dversion.apache-resource-bundles=SYSTEM

%install
%mvn_install

%files -f .mfiles
%license LICENSE NOTICE

%changelog
%autochangelog
