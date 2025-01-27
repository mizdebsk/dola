%bcond_with bootstrap

Name:           mockito
Version:        5.8.0
Release:        %autorelease
Summary:        Tasty mocking framework for unit tests in Java
License:        MIT
URL:            https://site.mockito.org/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

# ./generate-tarball.sh
Source0:        %{name}-%{version}.tar.gz
Source1:        generate-tarball.sh
# A custom build script to allow building with maven instead of gradle
Source2:        aggregator.pom
# Maven central POMs for subprojects
Source3:        https://repo1.maven.org/maven2/org/mockito/mockito-core/%{version}/mockito-core-%{version}.pom
Source4:        https://repo1.maven.org/maven2/org/mockito/mockito-junit-jupiter/%{version}/mockito-junit-jupiter-%{version}.pom

# Mockito expects byte-buddy to have a shaded/bundled version of ASM, but
# we don't bundle in Fedora, so this patch makes mockito use ASM explicitly
Patch:          use-unbundled-asm.patch

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(net.bytebuddy:byte-buddy)
BuildRequires:  mvn(net.bytebuddy:byte-buddy-agent)
BuildRequires:  mvn(net.bytebuddy:byte-buddy-dep)
BuildRequires:  mvn(org.apache.maven.plugins:maven-antrun-plugin)
BuildRequires:  mvn(org.junit.jupiter:junit-jupiter-api)
BuildRequires:  mvn(org.objenesis:objenesis)
BuildRequires:  mvn(org.opentest4j:opentest4j)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 5.8.0-16

%description
Mockito is a mocking framework that tastes really good. It lets you write
beautiful tests with clean & simple API. Mockito doesn't give you hangover
because the tests are very readable and they produce clean verification
errors.

%package junit-jupiter
Summary:        Mockito JUnit 5 support
Requires:       %{name} = %{version}-%{release}

%description junit-jupiter
Mockito JUnit 5 support.

%prep
%autosetup -p1 -C

cp %{SOURCE2} aggregator.pom
cp %{SOURCE3} pom.xml
cp %{SOURCE4} subprojects/junit-jupiter/pom.xml

# Disable failing test
# TODO check status: https://github.com/mockito/mockito/issues/2162
sed -i '/add_listeners_concurrently_sanity_check/i @org.junit.Ignore' src/test/java/org/mockitousage/debugging/StubbingLookupListenerCallbackTest.java

# Workaround easymock incompatibility with Java 17 that should be fixed
# in easymock 4.4: https://github.com/easymock/easymock/issues/274
%pom_add_plugin :maven-surefire-plugin . "<configuration>
    <argLine>--add-opens=java.base/sun.reflect.generics.reflectiveObjects=ALL-UNNAMED</argLine></configuration>"

# Compatibility alias
%mvn_alias org.%{name}:%{name}-core org.%{name}:%{name}-all

%pom_add_dep junit:junit
%pom_add_dep net.bytebuddy:byte-buddy-dep
%pom_remove_dep org.objenesis:objenesis
%pom_add_dep org.objenesis:objenesis
%pom_add_dep org.opentest4j:opentest4j

%pom_remove_dep org.junit.jupiter:junit-jupiter-api subprojects/junit-jupiter
%pom_add_dep org.junit.jupiter:junit-jupiter-api subprojects/junit-jupiter

mkdir -p src/main/resources/mockito-extensions
echo 'member-accessor-module' > src/main/resources/mockito-extensions/org.mockito.plugins.MemberAccessor
echo 'mock-maker-subclass' > src/main/resources/mockito-extensions/org.mockito.plugins.MockMaker

# see gradle/mockito-core/inline-mock.gradle
%pom_xpath_inject 'pom:project/pom:build/pom:plugins' '
<plugin>
  <groupId>org.apache.maven.plugins</groupId>
  <artifactId>maven-antrun-plugin</artifactId>
  <version>any</version>
  <executions>
    <execution>
      <phase>process-classes</phase>
      <configuration>
        <target>
          <copy file="${project.build.outputDirectory}/org/mockito/internal/creation/bytebuddy/inject/MockMethodDispatcher.class"
            tofile="${project.build.outputDirectory}/org/mockito/internal/creation/bytebuddy/inject/MockMethodDispatcher.raw"/>
        </target>
      </configuration>
      <goals>
        <goal>run</goal>
      </goals>
    </execution>
  </executions>
</plugin>
<plugin>
  <groupId>org.apache.maven.plugins</groupId>
  <artifactId>maven-jar-plugin</artifactId>
  <version>any</version>
  <configuration>
    <excludes>
      <exclude>org/mockito/internal/creation/bytebuddy/inject/*.class</exclude>
    </excludes>
  </configuration>
</plugin>
'

%mvn_package :aggregator __noinstall

%build
%mvn_build -j -f -- -Dmaven.compiler.release=11 -Dproject.build.sourceEncoding=UTF-8 -f aggregator.pom

%mvn_package org.mockito:mockito-junit-jupiter junit-jupiter

%install
%mvn_install

%files -f .mfiles
%license LICENSE
%doc README.md doc/design-docs/custom-argument-matching.md

%files junit-jupiter -f .mfiles-junit-jupiter

%changelog
%autochangelog
