%bcond_with bootstrap

Name:           modello
Version:        2.1.2
Release:        %autorelease
Summary:        Modello Data Model toolkit
# The majority of files are under MIT license, but some of them are ASL 2.0.
# Some parts of the project are derived from the Exolab project,
# and are licensed under a 5-clause BSD license (Plexus in SPDX).
License:        MIT AND Apache-2.0 AND Plexus
URL:            https://codehaus-plexus.github.io/modello
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://repo1.maven.org/maven2/org/codehaus/%{name}/%{name}/%{version}/%{name}-%{version}-source-release.zip
Source1:        https://www.apache.org/licenses/LICENSE-2.0.txt

Patch:          0001-Revert-Switch-to-codehaus-plexus-build-api-1.2.0-345.patch

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(com.google.inject:guice)
BuildRequires:  mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)
BuildRequires:  mvn(org.apache.maven.plugins:maven-dependency-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-enforcer-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-plugin-plugin)
BuildRequires:  mvn(org.apache.maven:maven-core)
BuildRequires:  mvn(org.apache.maven:maven-model)
BuildRequires:  mvn(org.apache.maven:maven-plugin-api)
BuildRequires:  mvn(org.apache.velocity:velocity-engine-core)
BuildRequires:  mvn(org.codehaus.plexus:plexus-component-annotations)
BuildRequires:  mvn(org.codehaus.plexus:plexus-component-metadata)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:  mvn(org.codehaus.plexus:plexus:pom:)
BuildRequires:  mvn(org.eclipse.sisu:org.eclipse.sisu.plexus)
BuildRequires:  mvn(org.jsoup:jsoup)
BuildRequires:  mvn(org.sonatype.plexus:plexus-build-api)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 2.1.2-23

%description
Modello is a Data Model toolkit in use by the Apache Maven Project.

Modello is a framework for code generation from a simple model.
Modello generates code from a simple model format based on a plugin
architecture, various types of code and descriptors can be generated
from the single model, including Java POJOs, XML
marshallers/unmarshallers, XSD and documentation.

%prep
%autosetup -p1 -C
cp -p %{SOURCE1} LICENSE
# We don't generate site; don't pull extra dependencies.
%pom_remove_plugin :maven-site-plugin

%pom_remove_dep :plexus-xml modello-core
%pom_remove_dep :sisu-guice modello-core
%pom_add_dep com.google.inject:guice modello-core

%pom_remove_dep :jackson-bom
%pom_disable_module modello-plugin-jackson modello-plugins
%pom_disable_module modello-plugin-jsonschema modello-plugins
%pom_remove_dep :modello-plugin-jackson modello-maven-plugin
%pom_remove_dep :modello-plugin-jsonschema modello-maven-plugin

%pom_disable_module modello-plugin-snakeyaml modello-plugins
%pom_remove_dep :modello-plugin-snakeyaml modello-maven-plugin

%pom_disable_module modello-test

%build
# skip tests because we have too old xmlunit in Fedora now (1.0.8)
%mvn_build -j -f

%install
%mvn_install

%jpackage_script org.codehaus.modello.ModelloCli "" "" modello:sisu/org.eclipse.sisu.plexus:sisu/org.eclipse.sisu.inject:google-guice:aopalliance:atinject:plexus-containers/plexus-component-annotations:plexus/classworlds:plexus/utils:plexus/plexus-build-api0:guava:velocity/velocity-engine-core %{name} true

%files -f .mfiles
%license LICENSE
%{_bindir}/modello

%changelog
%autochangelog
