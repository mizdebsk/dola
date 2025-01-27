%bcond_with bootstrap

Name:           plexus-interactivity
Version:        1.3
Release:        %autorelease
Summary:        Plexus Interactivity Handler Component
License:        MIT
URL:            https://github.com/codehaus-plexus/plexus-interactivity
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        %{url}/archive/%{name}-%{version}.tar.gz
Source1:        LICENSE.MIT

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(com.google.inject:guice)
BuildRequires:  mvn(javax.inject:javax.inject)
BuildRequires:  mvn(org.codehaus.plexus:plexus:pom:)
BuildRequires:  mvn(org.eclipse.sisu:org.eclipse.sisu.inject)
BuildRequires:  mvn(org.eclipse.sisu:sisu-maven-plugin)
BuildRequires:  mvn(org.jline:jline-reader)
BuildRequires:  mvn(org.junit.jupiter:junit-jupiter-api)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 1.3-5

%description
Plexus component that handles interactive user input from different
sources.

%prep
%autosetup -p1 -C
cp %{SOURCE1} .

%build
%mvn_build -j

%install
%mvn_install

%files -f .mfiles
%license LICENSE.MIT

%changelog
%autochangelog
