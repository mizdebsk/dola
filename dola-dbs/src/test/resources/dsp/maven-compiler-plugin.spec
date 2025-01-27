%bcond_with bootstrap

Name:           maven-compiler-plugin
Version:        3.12.1
Release:        %autorelease
Summary:        Maven Compiler Plugin
License:        Apache-2.0
URL:            https://maven.apache.org/plugins/maven-compiler-plugin
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://archive.apache.org/dist/maven/plugins/%{name}-%{version}-source-release.zip

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.maven.plugin-testing:maven-plugin-testing-harness)
BuildRequires:  mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)
BuildRequires:  mvn(org.apache.maven.plugins:maven-plugin-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-plugins:pom:)
BuildRequires:  mvn(org.apache.maven.shared:maven-shared-incremental)
BuildRequires:  mvn(org.apache.maven.shared:maven-shared-utils)
BuildRequires:  mvn(org.apache.maven:maven-artifact)
BuildRequires:  mvn(org.apache.maven:maven-compat)
BuildRequires:  mvn(org.apache.maven:maven-core)
BuildRequires:  mvn(org.apache.maven:maven-plugin-api)
BuildRequires:  mvn(org.codehaus.plexus:plexus-compiler-api)
BuildRequires:  mvn(org.codehaus.plexus:plexus-compiler-javac)
BuildRequires:  mvn(org.codehaus.plexus:plexus-compiler-manager)
BuildRequires:  mvn(org.codehaus.plexus:plexus-java)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:  mvn(org.codehaus.plexus:plexus-xml)
BuildRequires:  mvn(org.eclipse.sisu:sisu-maven-plugin)
BuildRequires:  mvn(org.mockito:mockito-core)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 3.12.1-13

%description
The Compiler Plugin is used to compile the sources of your project.

%prep
%autosetup -p1 -C

# Replace path to junit in a test case with the system wide .jar
sed -i 's|localRepository,\ "junit/junit/3.8.1/junit-3.8.1.jar"|"%(find-jar junit || find-jar javapackages-bootstrap/junit)"|' src/test/java/org/apache/maven/plugin/compiler/CompilerMojoTestCase.java

%build
# JAVA_HOME must be exported because unit tests make use of it for locating javac executable
export JAVA_HOME=%{java_home}
%mvn_build -j

%install
%mvn_install

%files -f .mfiles
%license LICENSE NOTICE

%changelog
%autochangelog
