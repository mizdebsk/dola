%bcond_with bootstrap

Name:           plexus-build-api0
Version:        0.0.7
Release:        %autorelease
Summary:        Plexus Build API
License:        Apache-2.0
URL:            https://github.com/codehaus-plexus/plexus-build-api
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://github.com/codehaus-plexus/plexus-build-api/archive/refs/tags/plexus-build-api-0.0.7.tar.gz
Source1:        http://www.apache.org/licenses/LICENSE-2.0.txt

# Forwarded upstream: https://github.com/sonatype/sisu-build-api/pull/2
Patch:          %{name}-migration-to-component-metadata.patch
Patch:          0000-Port-to-plexus-utils-3.3.0.patch

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(org.codehaus.plexus:plexus-component-metadata)
BuildRequires:  mvn(org.codehaus.plexus:plexus-container-default)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 0.0.7-52

%description
Plexus Build API

%prep
%autosetup -p1 -C
cp -p %{SOURCE1} .


%pom_remove_parent
# From upstream commit: https://github.com/codehaus-plexus/plexus-build-api/commit/6566292a7d85e275b824857bdf92d6504bc4824e
%pom_xpath_set "pom:plugin[pom:artifactId='maven-compiler-plugin']/pom:configuration/*" 1.8

%mvn_file : plexus/%{name}

# Install plexus-build-api-tests as well
%mvn_package :

%build
%mvn_build -j

%install
%mvn_install

%files -f .mfiles
%license LICENSE-2.0.txt

%changelog
%autochangelog
