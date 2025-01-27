%bcond_with bootstrap

Name:           plexus-sec-dispatcher4
Version:        4.1.0
Release:        %autorelease
Summary:        Plexus Security Dispatcher Component
License:        Apache-2.0
URL:            https://github.com/codehaus-plexus/plexus-sec-dispatcher
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        %{url}/archive/plexus-sec-dispatcher-%{version}/plexus-sec-dispatcher-%{version}.tar.gz
Source1:        https://www.apache.org/licenses/LICENSE-2.0.txt

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(javax.inject:javax.inject)
BuildRequires:  mvn(org.codehaus.modello:modello-maven-plugin)
BuildRequires:  mvn(org.codehaus.plexus:plexus:pom:)
BuildRequires:  mvn(org.eclipse.sisu:org.eclipse.sisu.inject)
BuildRequires:  mvn(org.eclipse.sisu:sisu-maven-plugin)
BuildRequires:  mvn(org.junit.jupiter:junit-jupiter)
BuildRequires:  mvn(org.slf4j:slf4j-api:2.0.17)
BuildRequires:  mvn(org.slf4j:slf4j-simple:2.0.17)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 4.0.3-3

%description
Plexus Security Dispatcher Component

%prep
%autosetup -p1 -C
cp %{SOURCE1} .
%mvn_compat_version : 4.1.0

%build
%mvn_build -j -- -Dversion.slf4j=2.0.17

%install
%mvn_install

%files -f .mfiles
%license LICENSE-2.0.txt

%changelog
%autochangelog
