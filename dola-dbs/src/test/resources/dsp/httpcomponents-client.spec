%bcond_with bootstrap

Name:           httpcomponents-client
Version:        4.5.14
Release:        %autorelease
Summary:        HTTP agent implementation based on httpcomponents HttpCore
License:        Apache-2.0
URL:            https://hc.apache.org
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://repo1.maven.org/maven2/org/apache/httpcomponents/httpcomponents-client/%{version}/httpcomponents-client-%{version}-source-release.zip

Patch:          0001-Use-system-copy-of-effective_tld_names.dat.patch
Patch:          0002-Port-to-mockito-2.patch
Patch:          0003-Port-to-Mockito-5.patch

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(commons-codec:commons-codec)
BuildRequires:  mvn(commons-logging:commons-logging)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.httpcomponents:httpcomponents-parent:pom:)
BuildRequires:  mvn(org.apache.httpcomponents:httpcore)
BuildRequires:  mvn(org.codehaus.mojo:build-helper-maven-plugin)
BuildRequires:  mvn(org.mockito:mockito-core)
%endif
%if %{without bootstrap}
BuildRequires:  publicsuffix-list
%endif
Requires:       publicsuffix-list
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 4.5.14-25

%description
HttpClient is a HTTP/1.1 compliant HTTP agent implementation based on
httpcomponents HttpCore. It also provides reusable components for
client-side authentication, HTTP state management, and HTTP connection
management. HttpComponents Client is a successor of and replacement
for Commons HttpClient 3.x. Users of Commons HttpClient are strongly
encouraged to upgrade.

%prep
%autosetup -p1 -C

%mvn_package :::tests: __noinstall

# Change scope of commons-logging to provided
%pom_change_dep :commons-logging :::provided httpclient

# Remove optional build deps not available in Fedora
%pom_disable_module httpclient-osgi
%pom_disable_module httpclient-win
%pom_disable_module fluent-hc
%pom_disable_module httpmime
%pom_disable_module httpclient-cache
%pom_remove_plugin :docbkx-maven-plugin
%pom_remove_plugin :clirr-maven-plugin
%pom_remove_plugin :maven-checkstyle-plugin
%pom_remove_plugin :apache-rat-plugin
%pom_remove_plugin :maven-source-plugin
%pom_remove_plugin :maven-javadoc-plugin
%pom_remove_plugin :animal-sniffer-maven-plugin

# Fails due to strict crypto policy - uses DSA in test data
rm httpclient/src/test/java/org/apache/http/conn/ssl/TestSSLSocketFactory.java

%pom_remove_plugin :download-maven-plugin httpclient

%pom_xpath_inject "pom:archive" "
    <manifestFile>\${project.build.outputDirectory}/META-INF/MANIFEST.MF</manifestFile>"

%pom_xpath_inject pom:build/pom:plugins "
    <plugin>
      <groupId>org.apache.felix</groupId>
      <artifactId>maven-bundle-plugin</artifactId>
      <executions>
        <execution>
          <id>bundle-manifest</id>
          <phase>process-classes</phase>
          <goals>
            <goal>manifest</goal>
          </goals>
        </execution>
      </executions>
    </plugin>"

%pom_xpath_inject pom:build "
<pluginManagement>
  <plugins>
    <plugin>
      <groupId>org.apache.felix</groupId>
      <artifactId>maven-bundle-plugin</artifactId>
      <configuration>
        <instructions>
          <Export-Package>org.apache.http.*,!org.apache.http.param</Export-Package>
          <Private-Package></Private-Package>
          <_nouses>true</_nouses>
          <Import-Package>!org.apache.avalon.framework.logger,!org.apache.log,!org.apache.log4j,*</Import-Package>
        </instructions>
        <excludeDependencies>true</excludeDependencies>
      </configuration>
    </plugin>
  </plugins>
</pluginManagement>
" httpclient

# requires network
rm httpclient/src/test/java/org/apache/http/client/config/TestRequestConfig.java

%build
%mvn_file ":{*}" httpcomponents/@1

%mvn_build -j -- -Dmaven.compiler.release=8

%install
%mvn_install

%files -f .mfiles
%license LICENSE.txt NOTICE.txt
%doc README.txt RELEASE_NOTES.txt

%changelog
%autochangelog
