%bcond_with bootstrap

Name:           maven-plugin-tools
Version:        3.9.0
Release:        %autorelease
Summary:        Maven Plugin Tools
License:        Apache-2.0
URL:            https://maven.apache.org/plugin-tools/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://repo1.maven.org/maven2/org/apache/maven/plugin-tools/%{name}/%{version}/%{name}-%{version}-source-release.zip

Patch:          0001-Disable-help-MOJO-generation.patch
Patch:          0002-Remove-dependency-on-jtidy.patch
Patch:          0003-Disable-reporting.patch

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(com.thoughtworks.qdox:qdox)
BuildRequires:  mvn(org.apache.maven.plugins:maven-enforcer-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-plugin-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-source-plugin)
BuildRequires:  mvn(org.apache.maven:maven-artifact)
BuildRequires:  mvn(org.apache.maven:maven-core)
BuildRequires:  mvn(org.apache.maven:maven-model)
BuildRequires:  mvn(org.apache.maven:maven-parent:pom:)
BuildRequires:  mvn(org.apache.maven:maven-plugin-api)
BuildRequires:  mvn(org.apache.maven:maven-repository-metadata)
BuildRequires:  mvn(org.apache.maven:maven-settings)
BuildRequires:  mvn(org.codehaus.modello:modello-maven-plugin)
BuildRequires:  mvn(org.codehaus.plexus:plexus-archiver)
BuildRequires:  mvn(org.codehaus.plexus:plexus-component-annotations)
BuildRequires:  mvn(org.codehaus.plexus:plexus-component-metadata)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:  mvn(org.eclipse.sisu:org.eclipse.sisu.plexus)
BuildRequires:  mvn(org.eclipse.sisu:sisu-maven-plugin)
BuildRequires:  mvn(org.jsoup:jsoup)
BuildRequires:  mvn(org.ow2.asm:asm)
BuildRequires:  mvn(org.ow2.asm:asm-commons)
BuildRequires:  mvn(org.sonatype.plexus:plexus-build-api)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 3.9.0-22

%description
The Maven Plugin Tools contains the necessary tools to be able to produce Maven
Plugins in a variety of languages.

%package -n maven-plugin-annotations
Summary:        Maven Plugin Java 5 Annotations

%description -n maven-plugin-annotations
This package contains Java 5 annotations to use in Mojos.

%package -n maven-plugin-plugin
Summary:        Maven Plugin Plugin

%description -n maven-plugin-plugin
The Plugin Plugin is used to create a Maven plugin descriptor for any Mojo's
found in the source tree, to include in the JAR. It is also used to generate
Xdoc files for the Mojos as well as for updating the plugin registry, the
artifact metadata and a generic help goal.

%package annotations
Summary:        Maven Plugin Tool for Annotations

%description annotations
This package provides Java 5 annotation tools for use with Apache Maven.

%package api
Summary:        Maven Plugin Tools APIs
Provides:       maven-shared-plugin-tools-api = 0:%{version}-%{release}

%description api
The Maven Plugin Tools API provides an API to extract information from
and generate documentation for Maven Plugins.

%package generators
Summary:        Maven Plugin Tools Generators

%description generators
The Maven Plugin Tools Generators provides content generation
(documentation, help) from plugin descriptor.

%package java
Summary:        Maven Plugin Tool for Java
Provides:       maven-shared-plugin-tools-java = 0:%{version}-%{release}

%description java
Descriptor extractor for plugins written in Java.

%prep
%autosetup -p1 -C
find -name '*.java' -exec sed -i 's/\r//' {} +

rm -r maven-plugin-tools-api/src/test/resources/javadoc

%pom_xpath_inject "pom:project/pom:properties" "
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>"

%pom_xpath_remove "pom:execution[pom:id='generated-helpmojo']" maven-plugin-plugin

%pom_disable_module maven-script
%pom_disable_module maven-plugin-report-plugin

%pom_remove_dep -r :maven-reporting-impl
%pom_remove_dep -r :maven-reporting-api
%pom_remove_dep -r :plexus-velocity
%pom_remove_dep -r :velocity
%pom_remove_dep -r :jtidy
%pom_remove_plugin -r :spotless-maven-plugin

%pom_remove_dep org.junit:junit-bom
%pom_remove_dep :maven-plugin-tools-ant maven-plugin-plugin
%pom_remove_dep :maven-plugin-tools-beanshell maven-plugin-plugin

rm maven-plugin-tools-generators/src/main/java/org/apache/maven/tools/plugin/generator/PluginXdocGenerator.java

%build
%mvn_build -j -s -f

%install
%mvn_install

%files -f .mfiles-maven-plugin-tools
%license LICENSE NOTICE

%files -n maven-plugin-annotations -f .mfiles-maven-plugin-annotations
%license LICENSE NOTICE

%files -n maven-plugin-plugin -f .mfiles-maven-plugin-plugin

%files annotations -f .mfiles-maven-plugin-tools-annotations
%license LICENSE NOTICE

%files api -f .mfiles-maven-plugin-tools-api
%license LICENSE NOTICE

%files generators -f .mfiles-maven-plugin-tools-generators

%files java -f .mfiles-maven-plugin-tools-java

%changelog
%autochangelog
