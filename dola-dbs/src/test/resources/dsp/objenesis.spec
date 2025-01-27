%bcond_with bootstrap

Name:           objenesis
Version:        3.4
Release:        %autorelease
Summary:        A library for instantiating Java objects
License:        Apache-2.0
URL:            https://objenesis.org
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://github.com/easymock/%{name}/archive/%{version}.tar.gz

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-remote-resources-plugin)
BuildRequires:  mvn(org.junit.jupiter:junit-jupiter)
%endif
%if %{without bootstrap}
# xmvn-builddep misses this:
BuildRequires:  mvn(org.apache:apache-jar-resource-bundle)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 3.4-15

%description
Objenesis is a small Java library that serves one purpose: to instantiate 
a new object of a particular class.
Java supports dynamic instantiation of classes using Class.newInstance(); 
however, this only works if the class has an appropriate constructor. There 
are many times when a class cannot be instantiated this way, such as when 
the class contains constructors that require arguments, that have side effects,
and/or that throw exceptions. As a result, it is common to see restrictions 
in libraries stating that classes must require a default constructor. 
Objenesis aims to overcome these restrictions by bypassing the constructor 
on object instantiation. Needing to instantiate an object without calling 
the constructor is a fairly specialized task, however there are certain cases 
when this is useful:
* Serialization, Remoting and Persistence - Objects need to be instantiated 
  and restored to a specific state, without invoking code.
* Proxies, AOP Libraries and Mock Objects - Classes can be sub-classed without 
  needing to worry about the super() constructor.
* Container Frameworks - Objects can be dynamically instantiated in 
  non-standard ways.

%prep
%autosetup -p1 -C

%pom_remove_dep :junit-bom

# Enable generation of pom.properties (rhbz#1017850)
%pom_xpath_remove pom:addMavenDescriptor

%pom_remove_plugin :maven-timestamp-plugin
%pom_remove_plugin :maven-enforcer-plugin
%pom_remove_plugin -r :maven-shade-plugin
%pom_remove_plugin -r org.sonatype.plugins:nexus-staging-maven-plugin
%pom_xpath_remove "pom:dependency[pom:scope='test']" tck

%pom_xpath_remove pom:build/pom:extensions

%pom_disable_module module-test

# Missing dependencies
rm tck/src/test/java/org/objenesis/tck/OsgiTest.java

%build
%mvn_build -j

%install
%mvn_install

%files -f .mfiles
%license LICENSE.txt

%changelog
%autochangelog
