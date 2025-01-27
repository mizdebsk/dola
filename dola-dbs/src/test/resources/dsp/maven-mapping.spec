%bcond_with bootstrap

Name:           maven-mapping
Version:        3.0.0
Release:        %autorelease
Summary:        Apache Maven Mapping
License:        Apache-2.0
URL:            https://maven.apache.org/shared/maven-mapping/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://repo.maven.apache.org/maven2/org/apache/maven/shared/%{name}/%{version}/%{name}-%{version}-source-release.zip

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.maven.plugin-testing:maven-plugin-testing-harness)
BuildRequires:  mvn(org.apache.maven.shared:maven-shared-components:pom:)
BuildRequires:  mvn(org.apache.maven:maven-core)
BuildRequires:  mvn(org.codehaus.plexus:plexus-interpolation)
%endif

%description
Maven shared component that implements file name mapping.

%package javadoc
Summary:        API documentation for %{name}

%description javadoc
API documentation for %{name}.

%prep
%autosetup -p1 -C
%pom_xpath_set "pom:project/pom:properties/pom:maven.compiler.target" "8" pom.xml
%pom_xpath_set "pom:project/pom:properties/pom:maven.compiler.source" "8" pom.xml

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%license LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%license LICENSE NOTICE

%changelog
%autochangelog
