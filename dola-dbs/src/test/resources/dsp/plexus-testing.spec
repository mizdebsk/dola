%bcond_with bootstrap

Name:           plexus-testing
Version:        1.3.0
Release:        %autorelease
Summary:        Plexus Testing
License:        Apache-2.0
URL:            https://github.com/codehaus-plexus/plexus-testing
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://github.com/codehaus-plexus/%{name}/archive/%{name}-%{version}.tar.gz

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(com.google.inject:guice)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:  mvn(org.codehaus.plexus:plexus-xml)
BuildRequires:  mvn(org.codehaus.plexus:plexus:pom:)
BuildRequires:  mvn(org.eclipse.sisu:org.eclipse.sisu.inject)
BuildRequires:  mvn(org.eclipse.sisu:org.eclipse.sisu.plexus)
BuildRequires:  mvn(org.junit.jupiter:junit-jupiter-api)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 1.3.0-12

%description
The Plexus Testing contains the necessary classes to be able to test
Plexus components.

%prep
%autosetup -p1 -C
%pom_add_dep org.codehaus.plexus:plexus-utils
%pom_add_dep org.codehaus.plexus:plexus-xml

# Some tests rely on Jakarta Injection API, which is not packaged
rm src/test/java/org/codehaus/plexus/testing/TestJakartaComponent.java
rm src/test/java/org/codehaus/plexus/testing/PlexusTestJakartaTest.java

%build
%mvn_build -j

%install
%mvn_install

%files -f .mfiles
%doc README.md
%license LICENSE

%changelog
%autochangelog
