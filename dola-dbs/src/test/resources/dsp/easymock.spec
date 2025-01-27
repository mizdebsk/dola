%bcond_with bootstrap

Name:           easymock
Version:        4.3
Release:        %autorelease
Summary:        Easy mock objects
License:        Apache-2.0
URL:            https://www.easymock.org
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

# ./generate-tarball.sh
Source0:        %{name}-%{version}.tar.gz
# Remove bundled binaries which cannot be easily verified for licensing
Source1:        generate-tarball.sh

Patch:          0001-Disable-android-support.patch
Patch:          0002-Unshade-cglib-and-asm.patch
Patch:          0003-Fix-OSGi-manifest.patch
Patch:          0004-Port-to-hamcrest-2.1.patch

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(cglib:cglib)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-remote-resources-plugin)
BuildRequires:  mvn(org.apache.maven.surefire:surefire-junit-platform)
BuildRequires:  mvn(org.apache.maven.surefire:surefire-testng)
BuildRequires:  mvn(org.codehaus.mojo:build-helper-maven-plugin)
BuildRequires:  mvn(org.junit.jupiter:junit-jupiter)
BuildRequires:  mvn(org.junit.vintage:junit-vintage-engine)
BuildRequires:  mvn(org.objenesis:objenesis)
BuildRequires:  mvn(org.ow2.asm:asm)
BuildRequires:  mvn(org.testng:testng)
%endif
%if %{without bootstrap}
# xmvn-builddep misses this:
BuildRequires:  mvn(org.apache:apache-jar-resource-bundle)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 4.3-23
Provides:       %{name}3 = %{version}-%{release}

%description
EasyMock provides Mock Objects for interfaces in JUnit tests by generating
them on the fly using Java's proxy mechanism. Due to EasyMock's unique style
of recording expectations, most refactorings will not affect the Mock Objects.
So EasyMock is a perfect fit for Test-Driven Development.

%prep
%autosetup -p1 -C


%pom_remove_plugin :license-maven-plugin
%pom_remove_plugin :maven-enforcer-plugin
%pom_remove_plugin :animal-sniffer-maven-plugin
%pom_remove_plugin :animal-sniffer-maven-plugin core

%pom_remove_plugin :maven-gpg-plugin test-testng
%pom_remove_plugin :maven-gpg-plugin test-java8
%pom_remove_plugin :maven-gpg-plugin test-junit5

# remove android support
rm core/src/main/java/org/easymock/internal/Android*.java
rm core/src/test/java/org/easymock/tests2/ClassExtensionHelperTest.java
%pom_disable_module test-android
%pom_remove_dep :dexmaker core

# unbundle asm and cglib
%pom_disable_module test-nodeps
%pom_remove_plugin :maven-shade-plugin core

# missing test deps
%pom_disable_module test-integration
%pom_disable_module test-osgi

# remove some warning caused by unavailable plugin
%pom_remove_plugin org.codehaus.mojo:versions-maven-plugin

# retired
%pom_remove_plugin :maven-timestamp-plugin

# For compatibility reasons
%mvn_file ":easymock{*}" easymock@1 easymock3@1

# ssh not needed during our builds
%pom_xpath_remove pom:extensions

# Force Surefire to run tests with JUnit, not with TestNG
%pom_xpath_inject "pom:plugin[pom:artifactId='maven-surefire-plugin']" \
    "<configuration><testNGArtifactName>none:none</testNGArtifactName></configuration>" core

# Workaround Java 17 compatibility issue that should be fixed in
# easymock 4.4: https://github.com/easymock/easymock/issues/274
%pom_xpath_inject "pom:plugin[pom:artifactId='maven-surefire-plugin']/pom:configuration" \
    "<argLine>--add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/java.io=ALL-UNNAMED</argLine>" core
%pom_xpath_inject "pom:plugin[pom:artifactId='maven-surefire-plugin']/pom:configuration" \
    "<argLine>--add-opens=java.base/java.lang=ALL-UNNAMED</argLine>" test-testng
%pom_add_plugin :maven-surefire-plugin test-java8 "<configuration>
    <argLine>--add-opens=java.base/java.lang=ALL-UNNAMED</argLine></configuration>"
%pom_add_plugin :maven-surefire-plugin test-junit5 "<configuration>
    <argLine>--add-opens=java.base/java.lang=ALL-UNNAMED</argLine></configuration>"

%build
%mvn_build -j

%install
%mvn_install

%files -f .mfiles
%license core/LICENSE.txt

%changelog
%autochangelog
