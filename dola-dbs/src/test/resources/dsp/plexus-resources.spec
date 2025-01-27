%bcond_with bootstrap

Name:           plexus-resources
Version:        1.3.0
Release:        %autorelease
Summary:        Plexus Resource Manager
License:        Apache-2.0 AND MIT
URL:            https://github.com/codehaus-plexus/plexus-resources
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://github.com/codehaus-plexus/plexus-resources/archive/plexus-resources-%{version}.tar.gz

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(javax.inject:javax.inject)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:  mvn(org.codehaus.plexus:plexus-xml)
BuildRequires:  mvn(org.codehaus.plexus:plexus:pom:)
BuildRequires:  mvn(org.eclipse.sisu:sisu-maven-plugin)
BuildRequires:  mvn(org.slf4j:slf4j-api)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 1.3.0-13

%description
The Plexus project seeks to create end-to-end developer tools for
writing applications. At the core is the container, which can be
embedded or for a full scale application server. There are many
reusable components for hibernate, form processing, jndi, i18n,
velocity, etc. Plexus also includes an application server which
is like a J2EE application server, without all the baggage.

%prep
%autosetup -p1 -C

%build
%mvn_file  : plexus/resources
%mvn_build -j -f

%install
%mvn_install

%files -f .mfiles

%changelog
%autochangelog
