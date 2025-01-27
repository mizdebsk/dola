%bcond_with bootstrap

Name:           disruptor
Version:        3.4.4
Release:        %autorelease
Summary:        Concurrent Programming Framework
License:        Apache-2.0
URL:            https://lmax-exchange.github.io/disruptor/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://github.com/LMAX-Exchange/disruptor/archive/%{version}/%{name}-%{version}.tar.gz
Source1:        https://repo1.maven.org/maven2/com/lmax/%{name}/%{version}/%{name}-%{version}.pom

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 3.4.4-29

%description
A High Performance Inter-Thread Messaging Library.

%prep
%autosetup -p1 -C
# Cleanup
find . -name "*.class" -print -delete
find . -name "*.jar" -type f -print -delete

cp -p %{SOURCE1} pom.xml

# Add OSGi support
%pom_xpath_inject "pom:project" "<packaging>bundle</packaging>"
%pom_add_plugin org.apache.felix:maven-bundle-plugin:2.3.7 . '
<extensions>true</extensions>
<configuration>
  <instructions>
    <Bundle-DocURL>%{url}</Bundle-DocURL>
    <Bundle-Name>${project.name}</Bundle-Name>
    <Bundle-Vendor>LMAX Disruptor Development Team</Bundle-Vendor>
  </instructions>
</configuration>
<executions>
  <execution>
    <id>bundle-manifest</id>
    <phase>process-classes</phase>
    <goals>
      <goal>manifest</goal>
    </goals>
  </execution>
</executions>'

# fail to compile cause: incompatible hamcrest apis
rm -r src/test/java/com/lmax/disruptor/RingBufferTest.java \
 src/test/java/com/lmax/disruptor/RingBufferEventMatcher.java
# Failed to stop thread: Thread[com.lmax.disruptor.BatchEventProcessor@1d057a39,5,main]
rm -r src/test/java/com/lmax/disruptor/dsl/DisruptorTest.java
# Test fails due to incompatible jmock version
#rm -f src/test/java/com/lmax/disruptor/EventPollerTest.java

%mvn_file :%{name} %{name}

%build

%mvn_build -j -- -Dproject.build.sourceEncoding=UTF-8 -Dmaven.compiler.source=1.8 -Dmaven.compiler.target=1.8

%install
%mvn_install

%files -f .mfiles
%doc README.md
%license LICENCE.txt

%changelog
%autochangelog
