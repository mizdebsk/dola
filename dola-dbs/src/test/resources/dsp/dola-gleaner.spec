Name:           dola-gleaner
Version:        0^20250415.072425.git.ecef81e
Release:        %autorelease
Summary:        Maven 4 extension for extracting build dependencies
License:        Apache-2.0
URL:            https://github.com/mizdebsk/dola-gleaner
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source:         dola-gleaner-snapshot-20250415.072425-ecef81e.tar.zst

BuildRequires:  maven-local
BuildRequires:  mvn(io.kojan:kojan-parent:pom:)
BuildRequires:  mvn(javax.inject:javax.inject)
BuildRequires:  mvn(org.apache.maven.resolver:maven-resolver-api)
BuildRequires:  mvn(org.apache.maven:maven-api-core:4.0.0-rc-3)
BuildRequires:  mvn(org.apache.maven:maven-api-model:4.0.0-rc-3)
BuildRequires:  mvn(org.apache.maven:maven-artifact:4.0.0-rc-3)
BuildRequires:  mvn(org.apache.maven:maven-core:4.0.0-rc-3)
BuildRequires:  mvn(org.apache.maven:maven-model:4.0.0-rc-3)
BuildRequires:  mvn(org.apache.maven:maven-plugin-api:4.0.0-rc-3)
BuildRequires:  mvn(org.eclipse.sisu:org.eclipse.sisu.inject)
BuildRequires:  mvn(org.eclipse.sisu:sisu-maven-plugin)

%description
Dola Gleaner is an extension for Apache Maven 4 that extracts build
dependencies without actually executing the build.  Instead of running
plugins (MOJOs), it analyzes the project and prints the dependencies
that would be required to complete the specified build.

This tool is especially useful for tools and environments that need to
understand build requirements without performing the build itself.

%prep
%autosetup -p1 -C

%build
%mvn_build -j

%install
%mvn_install

%files -f .mfiles
%license LICENSE NOTICE
%doc README.md

%changelog
%autochangelog
