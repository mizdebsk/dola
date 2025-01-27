%bcond_with bootstrap

Name:           maven-resolver
Epoch:          1
Version:        1.9.22
Release:        %autorelease
Summary:        Apache Maven Artifact Resolver library
License:        Apache-2.0
URL:            https://maven.apache.org/resolver/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://archive.apache.org/dist/maven/resolver/maven-resolver-%{version}-source-release.zip

Patch:          0001-Remove-use-of-deprecated-SHA-1-and-MD5-algorithms.patch

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(com.google.inject:guice)
BuildRequires:  mvn(commons-codec:commons-codec)
BuildRequires:  mvn(javax.inject:javax.inject)
BuildRequires:  mvn(javax.servlet:javax.servlet-api)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.httpcomponents:httpclient)
BuildRequires:  mvn(org.apache.httpcomponents:httpcore)
BuildRequires:  mvn(org.apache.maven.wagon:wagon-provider-api)
BuildRequires:  mvn(org.apache.maven:maven-model-builder)
BuildRequires:  mvn(org.apache.maven:maven-parent:pom:)
BuildRequires:  mvn(org.apache.maven:maven-resolver-provider)
BuildRequires:  mvn(org.codehaus.plexus:plexus-classworlds)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:  mvn(org.codehaus.plexus:plexus-xml)
BuildRequires:  mvn(org.eclipse.sisu:org.eclipse.sisu.inject)
BuildRequires:  mvn(org.eclipse.sisu:org.eclipse.sisu.plexus)
BuildRequires:  mvn(org.eclipse.sisu:sisu-maven-plugin)
BuildRequires:  mvn(org.hamcrest:hamcrest)
BuildRequires:  mvn(org.hamcrest:hamcrest-core)
BuildRequires:  mvn(org.mockito:mockito-core)
BuildRequires:  mvn(org.slf4j:jcl-over-slf4j)
BuildRequires:  mvn(org.slf4j:slf4j-api)
BuildRequires:  mvn(org.slf4j:slf4j-simple)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 1:1.9.22-10
Provides:       maven-resolver-api = %{epoch}:%{version}-%{release}
Provides:       maven-resolver-connector-basic = %{epoch}:%{version}-%{release}
Provides:       maven-resolver-impl = %{epoch}:%{version}-%{release}
Provides:       maven-resolver-spi = %{epoch}:%{version}-%{release}
Provides:       maven-resolver-transport-classpath = %{epoch}:%{version}-%{release}
Provides:       maven-resolver-transport-file = %{epoch}:%{version}-%{release}
Provides:       maven-resolver-transport-http = %{epoch}:%{version}-%{release}
Provides:       maven-resolver-transport-wagon = %{epoch}:%{version}-%{release}
Provides:       maven-resolver-util = %{epoch}:%{version}-%{release}

%description
Apache Maven Artifact Resolver is a library for working with artifact
repositories and dependency resolution. Maven Artifact Resolver deals with the
specification of local repository, remote repository, developer workspaces,
artifact transports and artifact resolution.

%prep
%autosetup -p1 -C

# Skip tests that equire internet connection
rm maven-resolver-supplier/src/test/java/org/eclipse/aether/supplier/RepositorySystemSupplierTest.java
rm maven-resolver-transport-http/src/test/java/org/eclipse/aether/transport/http/{HttpServer,HttpTransporterTest}.java
%pom_remove_dep org.eclipse.jetty: maven-resolver-transport-http

%pom_remove_plugin -r :bnd-maven-plugin
%pom_remove_plugin -r org.codehaus.mojo:animal-sniffer-maven-plugin
%pom_remove_plugin -r :japicmp-maven-plugin

%pom_disable_module maven-resolver-demos
%pom_disable_module maven-resolver-named-locks-hazelcast
%pom_disable_module maven-resolver-named-locks-redisson
%pom_disable_module maven-resolver-transport-classpath
%mvn_package :maven-resolver-test-util __noinstall

# generate OSGi manifests
for pom in $(find -mindepth 2 -name pom.xml) ; do
  %pom_add_plugin "org.apache.felix:maven-bundle-plugin" $pom \
  "<configuration>
    <instructions>
      <Bundle-SymbolicName>\${project.groupId}$(sed 's:./maven-resolver::;s:/pom.xml::;s:-:.:g' <<< $pom)</Bundle-SymbolicName>
      <Export-Package>!org.eclipse.aether.internal*,org.eclipse.aether*</Export-Package>
      <_nouses>true</_nouses>
    </instructions>
  </configuration>
  <executions>
    <execution>
      <id>create-manifest</id>
      <phase>process-classes</phase>
      <goals><goal>manifest</goal></goals>
    </execution>
  </executions>"
done
%pom_add_plugin "org.apache.maven.plugins:maven-jar-plugin" pom.xml \
"<configuration>
  <archive>
    <manifestFile>\${project.build.outputDirectory}/META-INF/MANIFEST.MF</manifestFile>
  </archive>
</configuration>"

%mvn_alias 'org.apache.maven.resolver:maven-resolver{*}' 'org.eclipse.aether:aether@1'
%mvn_alias 'org.apache.maven.resolver:maven-resolver-transport-wagon' 'org.eclipse.aether:aether-connector-wagon'
%mvn_file ':maven-resolver{*}' %{name}/maven-resolver@1 aether/aether@1

%build
%mvn_build -j

%install
%mvn_install

%files -f .mfiles
%license LICENSE NOTICE

%changelog
%autochangelog
