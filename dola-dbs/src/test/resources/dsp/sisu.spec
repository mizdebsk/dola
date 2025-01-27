%bcond_with bootstrap

Name:           sisu
Epoch:          1
Version:        0.9.0~M3
Release:        %autorelease
Summary:        Eclipse dependency injection framework
# sisu is EPL-1.0, the bundled asm is BSD
License:        EPL-1.0 AND BSD-3-Clause
URL:            https://eclipse.org/sisu/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://github.com/eclipse-sisu/sisu-project/archive/refs/tags/milestones/0.9.0.M3.tar.gz#/sisu-%{version}.tar.gz

Patch:          0001-Add-ASM-support-for-Java-24-and-25.patch

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(com.google.inject.extensions:guice-servlet)
BuildRequires:  mvn(com.google.inject:guice)
BuildRequires:  mvn(javax.annotation:javax.annotation-api)
BuildRequires:  mvn(javax.enterprise:cdi-api)
BuildRequires:  mvn(javax.servlet:servlet-api)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)
BuildRequires:  mvn(org.apache.maven.plugins:maven-plugin-plugin)
BuildRequires:  mvn(org.apache.maven.shared:maven-common-artifact-filters)
BuildRequires:  mvn(org.apache.maven:maven-artifact)
BuildRequires:  mvn(org.apache.maven:maven-core)
BuildRequires:  mvn(org.apache.maven:maven-model)
BuildRequires:  mvn(org.apache.maven:maven-plugin-api)
BuildRequires:  mvn(org.codehaus.plexus:plexus-classworlds)
BuildRequires:  mvn(org.codehaus.plexus:plexus-component-annotations)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:  mvn(org.eclipse.sisu:sisu-maven-plugin)
BuildRequires:  mvn(org.junit.jupiter:junit-jupiter-api)
BuildRequires:  mvn(org.osgi:osgi.core)
BuildRequires:  mvn(org.slf4j:slf4j-api)
BuildRequires:  mvn(org.slf4j:slf4j-nop)
BuildRequires:  mvn(org.sonatype.plexus:plexus-build-api)
BuildRequires:  mvn(org.testng:testng)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 1:0.9.0~M3-14
Provides:       %{name}-inject = %{epoch}:%{version}-%{release}
Provides:       %{name}-plexus = %{epoch}:%{version}-%{release}
Provides:       bundled(objectweb-asm)

%description
Java dependency injection framework with backward support for plexus and bean
style dependency injection.

%package maven-plugin
Summary:        Sisu plugin for Apache Maven
# Remove in Fedora 45
Obsoletes:      sisu-mojos < 1:0.9.0~M3

%description maven-plugin
The Sisu Plugin for Maven provides mojos to generate
META-INF/sisu/javax.inject.Named index files for the Sisu container.

%prep
%autosetup -p1 -C

%pom_disable_module org.eclipse.sisu.inject.extender
%pom_disable_module org.eclipse.sisu.plexus.extender

%pom_remove_dep :junit-bom
%pom_change_dep :plexus-utils :::provided org.eclipse.sisu.plexus
%pom_change_dep :plexus-xml :::provided org.eclipse.sisu.plexus

%pom_remove_plugin -r :bnd-maven-plugin
%pom_remove_plugin -r :maven-jar-plugin
%pom_remove_plugin -r :jacoco-maven-plugin
%pom_remove_plugin -r :maven-enforcer-plugin
%pom_remove_plugin -r :maven-dependency-plugin
%pom_remove_plugin -r :maven-clean-plugin

%mvn_package :sisu-maven-plugin maven-plugin
%mvn_alias :org.eclipse.sisu.inject :::no_asm:
%mvn_alias :org.eclipse.sisu.plexus org.sonatype.sisu:sisu-inject-plexus org.codehaus.plexus:plexus-container-default

%build
%mvn_build -j -f

%install
%mvn_install

%files -f .mfiles
%doc README.md
%license LICENSE.txt

%files maven-plugin -f .mfiles-maven-plugin

%changelog
%autochangelog
