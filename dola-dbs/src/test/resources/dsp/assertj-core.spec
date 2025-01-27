%bcond_with bootstrap

Name:           assertj-core
Version:        3.26.3
Release:        %autorelease
Summary:        Library of assertions similar to fest-assert
License:        Apache-2.0
URL:            https://joel-costigliola.github.io/assertj/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://github.com/joel-costigliola/assertj-core/archive/assertj-build-%{version}.tar.gz

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(net.bytebuddy:byte-buddy)
BuildRequires:  mvn(org.hamcrest:hamcrest)
BuildRequires:  mvn(org.junit.jupiter:junit-jupiter-api)
BuildRequires:  mvn(org.opentest4j:opentest4j)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 3.26.3-8

%description
A rich and intuitive set of strongly-typed assertions to use for unit testing
(either with JUnit or TestNG).

%prep
%autosetup -p1 -C

%pom_remove_plugin -r :maven-javadoc-plugin
%pom_remove_plugin -r :maven-enforcer-plugin
%pom_remove_plugin -r :jacoco-maven-plugin
%pom_remove_plugin -r :spotless-maven-plugin
%pom_remove_plugin -r :bnd-maven-plugin
%pom_remove_plugin -r :bnd-resolver-maven-plugin
%pom_remove_plugin -r :bnd-testing-maven-plugin
%pom_remove_plugin -r :nexus-staging-maven-plugin
%pom_remove_plugin -r :license-maven-plugin
%pom_remove_plugin -r :flatten-maven-plugin
%pom_remove_dep -r :mockito-bom
%pom_remove_dep -r :junit-bom

%pom_disable_module assertj-core-kotlin assertj-tests/assertj-integration-tests
%pom_disable_module assertj-core-groovy assertj-tests/assertj-integration-tests

%pom_xpath_inject pom:plugins '
<plugin>
  <groupId>org.apache.maven.plugins</groupId>
  <artifactId>maven-jar-plugin</artifactId>
  <version>any</version>
  <configuration>
    <archive>
      <manifestEntries>
        <Multi-Release>true</Multi-Release>
      </manifestEntries>
    </archive>
  </configuration>
</plugin>' assertj-core

%build
%mvn_build -j -f -- -Dproject.build.sourceEncoding=UTF-8

%install
%mvn_install

%files -f .mfiles
%doc README.md CONTRIBUTING.md
%license LICENSE.txt

%changelog
%autochangelog
