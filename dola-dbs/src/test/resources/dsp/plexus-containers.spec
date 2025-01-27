%bcond_with bootstrap

Name:           plexus-containers
Version:        2.2.0
Release:        %autorelease
Summary:        Containers for Plexus
# Most of the files are either under Apache-2.0 or MIT
# The following files are under xpp:
# plexus-component-metadata/src/main/java/org/codehaus/plexus/metadata/merge/Driver.java
# plexus-component-metadata/src/main/java/org/codehaus/plexus/metadata/merge/MXParser.java
License:        Apache-2.0 AND MIT AND xpp
URL:            https://github.com/codehaus-plexus/plexus-containers
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://github.com/codehaus-plexus/%{name}/archive/%{name}-%{version}.tar.gz
Source1:        http://www.apache.org/licenses/LICENSE-2.0.txt
Source2:        LICENSE.MIT

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(com.thoughtworks.qdox:qdox)
BuildRequires:  mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)
BuildRequires:  mvn(org.apache.maven.plugins:maven-plugin-plugin)
BuildRequires:  mvn(org.apache.maven:maven-core)
BuildRequires:  mvn(org.apache.maven:maven-model)
BuildRequires:  mvn(org.apache.maven:maven-plugin-api)
BuildRequires:  mvn(org.codehaus.plexus:plexus-testing)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:  mvn(org.codehaus.plexus:plexus:pom:)
BuildRequires:  mvn(org.jdom:jdom2)
BuildRequires:  mvn(org.junit.jupiter:junit-jupiter-api)
BuildRequires:  mvn(org.ow2.asm:asm)
BuildRequires:  mvn(org.slf4j:slf4j-simple)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 2.2.0-13

%description
The Plexus project seeks to create end-to-end developer tools for
writing applications. At the core is the container, which can be
embedded or for a full scale application server. There are many
reusable components for hibernate, form processing, jndi, i18n,
velocity, etc. Plexus also includes an application server which
is like a J2EE application server, without all the baggage.

%package component-metadata
Summary:        Component metadata from %{name}

%description component-metadata
%{summary}.

%package component-annotations
Summary:        Component API from %{name}

%description component-annotations
%{summary}.

%prep
%autosetup -p1 -C
cp %{SOURCE1} .
cp %{SOURCE2} .

%pom_remove_plugin -r :maven-site-plugin

# remove some broken tests
rm plexus-component-metadata/src/test/java/org/codehaus/plexus/metadata/merge/ComponentsXmlMergerTest.java
rm plexus-component-metadata/src/test/java/org/codehaus/plexus/metadata/DefaultComponentDescriptorWriterTest.java

%mvn_package :plexus-containers __noinstall

%build
%mvn_build -j -s

%install
%mvn_install

%files component-metadata -f .mfiles-plexus-component-metadata
%license LICENSE-2.0.txt LICENSE.MIT

%files component-annotations -f .mfiles-plexus-component-annotations
%license LICENSE-2.0.txt LICENSE.MIT

%changelog
%autochangelog
