%bcond_with bootstrap

Name:           httpcomponents-core
Version:        4.4.16
Release:        %autorelease
Summary:        Set of low level Java HTTP transport components for HTTP services
License:        Apache-2.0
URL:            https://hc.apache.org
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://repo1.maven.org/maven2/org/apache/httpcomponents/httpcomponents-core/%{version}/httpcomponents-core-%{version}-source-release.zip

Patch:          0001-Port-to-mockito-2.patch
Patch:          0002-Port-to-Mockito-5.patch

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(commons-logging:commons-logging)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.httpcomponents:httpcomponents-parent:pom:)
BuildRequires:  mvn(org.codehaus.mojo:build-helper-maven-plugin)
BuildRequires:  mvn(org.mockito:mockito-core)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 4.4.16-25

%description
HttpCore is a set of low level HTTP transport components that can be
used to build custom client and server side HTTP services with a
minimal footprint. HttpCore supports two I/O models: blocking I/O
model based on the classic Java I/O and non-blocking, event driven I/O
model based on Java NIO.

The blocking I/O model may be more appropriate for data intensive, low
latency scenarios, whereas the non-blocking model may be more
appropriate for high latency scenarios where raw data throughput is
less important than the ability to handle thousands of simultaneous
HTTP connections in a resource efficient manner.

%prep
%autosetup -p1 -C

# Tests failing without networking
sed -i '/testHttpsCreateConnection/i@org.junit.Ignore' httpcore/src/test/java/org/apache/http/impl/pool/TestBasicConnPool.java

# Tests failing with Java 17
sed -i '/testAwaitInputInBuffer\|testAwaitInputInSocket\|testNotStaleWhenHasData\|testWriteSmallFragmentBuffering\|testWriteSmallFragmentNoBuffering/i@org.junit.Ignore' httpcore/src/test/java/org/apache/http/impl/{TestBHttpConnectionBase,io/TestSessionInOutBuffers}.java

%pom_remove_plugin :maven-checkstyle-plugin
%pom_remove_plugin :apache-rat-plugin
%pom_remove_plugin :maven-source-plugin
%pom_remove_plugin :maven-javadoc-plugin

# We don't have conscrypt for testing
%pom_remove_dep :conscrypt-openjdk-uber httpcore-nio
rm httpcore-nio/src/test/java/org/apache/http/nio/integration/TestJSSEProviderIntegration.java

# we don't need these artifacts right now
%pom_disable_module httpcore-osgi
%pom_disable_module httpcore-ab

# OSGify modules
for module in httpcore httpcore-nio; do
    %pom_xpath_remove "pom:project/pom:packaging" $module
    %pom_xpath_inject "pom:project" "<packaging>bundle</packaging>" $module
    %pom_remove_plugin :maven-jar-plugin $module
    %pom_xpath_inject "pom:build/pom:plugins" "
        <plugin>
          <groupId>org.apache.felix</groupId>
          <artifactId>maven-bundle-plugin</artifactId>
          <extensions>true</extensions>
          <configuration>
            <instructions>
              <Export-Package>*</Export-Package>
              <Private-Package></Private-Package>
              <Automatic-Module-Name>org.apache.httpcomponents.$module</Automatic-Module-Name>
              <_nouses>true</_nouses>
            </instructions>
          </configuration>
        </plugin>" $module
done

# install JARs to httpcomponents/ for compatibility reasons
# several other packages expect to find the JARs there
%mvn_file ":{*}" httpcomponents/@1

# tests fail with OpenJDK 21 due to mocking of sealed classes
sed -i '/testRequestTargetHostFallback()/i@org.junit.Ignore' httpcore/src/test/java/org/apache/http/protocol/TestStandardInterceptors.java
rm httpcore-nio/src/test/java/org/apache/http/impl/nio/TestContentChannel.java

%build
%mvn_build -j -- -Dmaven.compiler.release=8

%install
%mvn_install

%files -f .mfiles
%license LICENSE.txt NOTICE.txt
%doc README.txt RELEASE_NOTES.txt

%changelog
%autochangelog
