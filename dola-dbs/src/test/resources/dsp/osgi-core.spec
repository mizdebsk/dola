%bcond_with bootstrap

Name:           osgi-core
Version:        8.0.0
Release:        %autorelease
Summary:        OSGi Core API
License:        Apache-2.0
URL:            https://www.osgi.org
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://docs.osgi.org/download/r8/osgi.core-%{version}.jar

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.osgi:osgi.annotation)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 8.0.0-34

%description
OSGi Core, Interfaces and Classes for use in compiling bundles.

%prep
%autosetup -p1 -C

# Delete pre-built binaries
rm -r org
find -name '*.class' -delete

mkdir -p src/main/{java,resources}
mv OSGI-OPT/src/org src/main/java/

mv META-INF/maven/org.osgi/osgi.core/pom.xml .

%pom_xpath_inject pom:project '
<packaging>bundle</packaging>
<properties>
  <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
</properties>
<build>
  <plugins>
    <plugin>
      <groupId>org.apache.felix</groupId>
      <artifactId>maven-bundle-plugin</artifactId>
      <extensions>true</extensions>
      <configuration>
        <instructions>
          <Bundle-Name>${project.artifactId}</Bundle-Name>
          <Bundle-SymbolicName>${project.artifactId}</Bundle-SymbolicName>
        </instructions>
      </configuration>
    </plugin>
  </plugins>
</build>'

%mvn_alias : org.osgi:org.osgi.core

%build
%mvn_build -j -- -Dmaven.compiler.source=1.8 -Dmaven.compiler.target=1.8

%install
%mvn_install

%files -f .mfiles
%license LICENSE
%doc about.html

%changelog
%autochangelog
