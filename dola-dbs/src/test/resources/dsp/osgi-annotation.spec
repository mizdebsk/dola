%bcond_with bootstrap

Name:           osgi-annotation
Version:        8.1.0
Release:        %autorelease
Summary:        Annotations for use in compiling OSGi bundles
License:        Apache-2.0
URL:            https://www.osgi.org
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

# Upstream project is behind an account registration system with no anonymous
# read access, so we download the source from maven central instead
Source0:        https://repo1.maven.org/maven2/org/osgi/osgi.annotation/%{version}/osgi.annotation-%{version}.jar
Source1:        https://repo1.maven.org/maven2/org/osgi/osgi.annotation/%{version}/osgi.annotation-%{version}.pom

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 8.1.0-18

%description
Annotations for use in compiling OSGi bundles. This package is not normally
needed at run-time.

%prep
%autosetup -p1 -C

mkdir -p src/main/java && mv OSGI-OPT/src/org src/main/java

rm -r org OSGI-OPT

cp -p %{SOURCE1} pom.xml

# Ensure OSGi metadata is generated
%pom_xpath_inject pom:project "
  <packaging>bundle</packaging>
  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.felix</groupId>
        <artifactId>maven-bundle-plugin</artifactId>
        <extensions>true</extensions>
        <configuration>
          <instructions>
            <Bundle-Name>\${project.artifactId}</Bundle-Name>
            <Bundle-SymbolicName>\${project.artifactId}</Bundle-SymbolicName>
          </instructions>
        </configuration>
      </plugin>
    </plugins>
  </build>"

# Known by two names in maven central, so add an alias for the older name
%mvn_alias org.osgi:osgi.annotation org.osgi:org.osgi.annotation

%build
%mvn_build -j -- -Dmaven.compiler.source=1.8 -Dmaven.compiler.target=1.8

%install
%mvn_install

%files -f .mfiles
%license META-INF/LICENSE META-INF/NOTICE

%changelog
%autochangelog
