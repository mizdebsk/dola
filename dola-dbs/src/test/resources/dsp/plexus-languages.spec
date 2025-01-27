%bcond_with bootstrap

Name:           plexus-languages
Version:        1.2.0
Release:        %autorelease
Summary:        Plexus Languages
License:        Apache-2.0
URL:            https://github.com/codehaus-plexus/plexus-languages
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

# ./generate-tarball.sh
Source0:        %{name}-%{version}.tar.gz
Source1:        https://www.apache.org/licenses/LICENSE-2.0.txt
# Sources contain bundled jars that we cannot verify for licensing
Source2:        generate-tarball.sh

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(com.thoughtworks.qdox:qdox)
BuildRequires:  mvn(javax.inject:javax.inject)
BuildRequires:  mvn(org.apache.maven.plugins:maven-failsafe-plugin)
BuildRequires:  mvn(org.codehaus.plexus:plexus:pom:)
BuildRequires:  mvn(org.eclipse.sisu:sisu-maven-plugin)
BuildRequires:  mvn(org.ow2.asm:asm)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 1.2.0-15

%description
Plexus Languages is a set of Plexus components that maintain shared
language features.

%prep
%autosetup -p1 -C

cp %{SOURCE1} .

%pom_remove_plugin :maven-enforcer-plugin

%build
# many tests rely on bundled test jars/classes
%mvn_build -j -f

%install
%mvn_install

%files -f .mfiles
%license LICENSE-2.0.txt

%changelog
%autochangelog
