%bcond_with bootstrap

Name:           plexus-io
Version:        3.5.0
Release:        %autorelease
Summary:        Plexus IO Components
License:        Apache-2.0
URL:            https://github.com/codehaus-plexus/plexus-io
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://github.com/codehaus-plexus/plexus-io/archive/plexus-io-%{version}.tar.gz
Source1:        http://www.apache.org/licenses/LICENSE-2.0.txt

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(com.google.code.findbugs:jsr305)
BuildRequires:  mvn(com.google.inject:guice)
BuildRequires:  mvn(commons-io:commons-io)
BuildRequires:  mvn(javax.inject:javax.inject)
BuildRequires:  mvn(org.codehaus.plexus:plexus-testing)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:  mvn(org.codehaus.plexus:plexus-xml)
BuildRequires:  mvn(org.codehaus.plexus:plexus:pom:)
BuildRequires:  mvn(org.eclipse.sisu:org.eclipse.sisu.inject)
BuildRequires:  mvn(org.eclipse.sisu:sisu-maven-plugin)
BuildRequires:  mvn(org.junit.jupiter:junit-jupiter-api)
BuildRequires:  mvn(org.slf4j:slf4j-simple)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 3.5.0-7

%description
Plexus IO is a set of plexus components, which are designed for use
in I/O operations.

%prep
%autosetup -p1 -C
cp %{SOURCE1} .

# Test fails in mock
sed -i /class/i@org.junit.jupiter.api.Disabled src/test/java/org/codehaus/plexus/components/io/attributes/SymlinkUtilsTest.java

%mvn_file : plexus/io

%build
%mvn_build -j

%install
%mvn_install

%files -f .mfiles
%license NOTICE.txt LICENSE-2.0.txt

%changelog
%autochangelog
