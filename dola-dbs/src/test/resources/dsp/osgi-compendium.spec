%bcond_with bootstrap

Name:           osgi-compendium
Version:        7.0.0
Release:        %autorelease
Summary:        Interfaces and Classes for use in compiling OSGi bundles
License:        Apache-2.0
URL:            https://www.osgi.org
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://osgi.org/download/r7/osgi.cmpn-%{version}.jar

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.osgi:osgi.annotation)
BuildRequires:  mvn(org.osgi:osgi.core)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 7.0.0-38

%description
OSGi Compendium, Interfaces and Classes for use in compiling bundles.

%prep
%autosetup -p1 -C

# Delete pre-built binaries
rm -r org
find -name '*.class' -delete

mkdir -p src/main/{java,resources}
mv OSGI-OPT/src/org src/main/java/
mv xmlns src/main/resources

# J2ME stuff
rm -r src/main/java/org/osgi/service/io

mv META-INF/maven/org.osgi/osgi.cmpn/pom.xml .

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

%pom_add_dep org.osgi:osgi.annotation::provided
%pom_add_dep org.osgi:osgi.core::provided
# Don't compile in Servlet, Jax RS and JPA support
rm -r src/main/java/org/osgi/service/http
rm -r src/main/java/org/osgi/service/jaxrs
rm -r src/main/java/org/osgi/service/jpa
rm -r src/main/java/org/osgi/service/transaction/control/jpa

%build
%mvn_build -j -- -Dmaven.compiler.source=1.8 -Dmaven.compiler.target=1.8

%install
%mvn_install

%files -f .mfiles
%license LICENSE
%doc about.html

%changelog
%autochangelog
