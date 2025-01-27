%bcond_with bootstrap
%global tarball_name RELEASE_%(echo '%{version}' | tr . _)

Name:           cglib
Version:        3.3.0
Release:        %autorelease
Summary:        Code Generation Library for Java
# ASM MethodVisitor is based on ASM code and therefore
# BSD-licensed. Everything else is ASL 2.0.
License:        Apache-2.0 AND BSD-3-Clause
URL:            https://github.com/cglib/cglib
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://github.com/cglib/cglib/archive/%{tarball_name}.tar.gz

Patch:          0001-Remove-unused-import.patch

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(org.apache.ant:ant)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.ow2.asm:asm)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 3.3.0-38

%description
cglib is a powerful, high performance and quality code generation library
for Java. It is used to extend Java classes and implements interfaces
at run-time.

%prep
%autosetup -p1 -C

# remove unnecessary dependency on parent POM
%pom_remove_parent

%pom_disable_module cglib-nodep
%pom_disable_module cglib-integration-test
%pom_disable_module cglib-jmh
%pom_xpath_set pom:packaging 'bundle' cglib
%pom_xpath_inject pom:build/pom:plugins '<plugin>
                                           <groupId>org.apache.felix</groupId>
                                           <artifactId>maven-bundle-plugin</artifactId>
                                           <version>1.4.0</version>
                                           <extensions>true</extensions>
                                           <configuration>
                                             <instructions>
                                               <Bundle-SymbolicName>net.sf.cglib.core</Bundle-SymbolicName>
                                               <Export-Package>net.*</Export-Package>
                                               <Import-Package>org.apache.tools.*;resolution:=optional,*</Import-Package>
                                             </instructions>
                                           </configuration>
                                         </plugin>' cglib
%pom_remove_plugin org.apache.maven.plugins:maven-gpg-plugin
%pom_remove_plugin org.apache.maven.plugins:maven-jarsigner-plugin cglib-sample
%pom_remove_plugin -r :maven-javadoc-plugin

%mvn_alias :cglib "net.sf.cglib:cglib" "cglib:cglib-full" "cglib:cglib-nodep" "org.sonatype.sisu.inject:cglib"

%build
# 5 tests fail with OpenJDK 11
# Forwarded upstream: https://github.com/cglib/cglib/issues/119
%mvn_build -j -f -- -Djava.version.source=1.8 -Djava.version.target=1.8

%install
%mvn_install

%files -f .mfiles
%license LICENSE NOTICE

%changelog
%autochangelog
