%bcond_with bootstrap
# Component versions, taken from gradle.properties
%global platform_version 1.%(v=%{version}; echo ${v:2})
%global jupiter_version %{version}
%global vintage_version %{version}

Name:           junit5
Version:        5.10.2
Release:        %autorelease
Summary:        Java regression testing framework
License:        EPL-2.0
URL:            https://junit.org/junit5/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://github.com/junit-team/junit5/archive/r%{version}/junit5-%{version}.tar.gz
# Aggregator POM (used for packaging only)
Source100:      aggregator.pom
# Platform POMs
Source200:      https://repo1.maven.org/maven2/org/junit/platform/junit-platform-commons/%{platform_version}/junit-platform-commons-%{platform_version}.pom
Source201:      https://repo1.maven.org/maven2/org/junit/platform/junit-platform-console/%{platform_version}/junit-platform-console-%{platform_version}.pom
Source202:      https://repo1.maven.org/maven2/org/junit/platform/junit-platform-console-standalone/%{platform_version}/junit-platform-console-standalone-%{platform_version}.pom
Source203:      https://repo1.maven.org/maven2/org/junit/platform/junit-platform-engine/%{platform_version}/junit-platform-engine-%{platform_version}.pom
Source205:      https://repo1.maven.org/maven2/org/junit/platform/junit-platform-launcher/%{platform_version}/junit-platform-launcher-%{platform_version}.pom
Source206:      https://repo1.maven.org/maven2/org/junit/platform/junit-platform-runner/%{platform_version}/junit-platform-runner-%{platform_version}.pom
Source207:      https://repo1.maven.org/maven2/org/junit/platform/junit-platform-suite-api/%{platform_version}/junit-platform-suite-api-%{platform_version}.pom
Source209:      https://repo1.maven.org/maven2/org/junit/platform/junit-platform-testkit/%{platform_version}/junit-platform-testkit-%{platform_version}.pom
Source210:      https://repo1.maven.org/maven2/org/junit/platform/junit-platform-suite-commons/%{platform_version}/junit-platform-suite-commons-%{platform_version}.pom
# Jupiter POMs
Source300:      https://repo1.maven.org/maven2/org/junit/jupiter/junit-jupiter/%{jupiter_version}/junit-jupiter-%{jupiter_version}.pom
Source301:      https://repo1.maven.org/maven2/org/junit/jupiter/junit-jupiter-api/%{jupiter_version}/junit-jupiter-api-%{jupiter_version}.pom
Source302:      https://repo1.maven.org/maven2/org/junit/jupiter/junit-jupiter-engine/%{jupiter_version}/junit-jupiter-engine-%{jupiter_version}.pom
Source303:      https://repo1.maven.org/maven2/org/junit/jupiter/junit-jupiter-migrationsupport/%{jupiter_version}/junit-jupiter-migrationsupport-%{jupiter_version}.pom
Source304:      https://repo1.maven.org/maven2/org/junit/jupiter/junit-jupiter-params/%{jupiter_version}/junit-jupiter-params-%{jupiter_version}.pom
# Vintage POM
Source400:      https://repo1.maven.org/maven2/org/junit/vintage/junit-vintage-engine/%{vintage_version}/junit-vintage-engine-%{vintage_version}.pom
# BOM POM
Source500:      https://repo1.maven.org/maven2/org/junit/junit-bom/%{version}/junit-bom-%{version}.pom

Patch:          0001-Drop-transitive-requirement-on-apiguardian.patch
Patch:          0002-Add-missing-module-static-requires.patch
Patch:          0003-Remove-legacy-XML-console-support.patch

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(com.univocity:univocity-parsers)
BuildRequires:  mvn(info.picocli:picocli)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apiguardian:apiguardian-api)
BuildRequires:  mvn(org.assertj:assertj-core)
BuildRequires:  mvn(org.codehaus.mojo:build-helper-maven-plugin)
BuildRequires:  mvn(org.opentest4j:opentest4j)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-guide < 5.10.2-16
Obsoletes:      %{name}-javadoc < 5.10.2-16

%description
JUnit is a popular regression testing framework for Java platform.

%prep
%autosetup -p1 -C
find -name '*.jar' -delete


cp -p %{SOURCE100} pom.xml

for source in $(echo %{sources} | cut -d ' ' -f3-); do
  module=${source}
  module=${module##*/}
  module=${module%%-*}
  if [ -d ${module}/src/module ]; then
    mkdir -p ${module}/src/main/java
    mv -t ${module}/src/main/java ${module}/src/module/*/module-info.java
  fi
  cp -p ${source} ${module}/pom.xml
  %pom_add_parent org.fedoraproject.xmvn.junit5:aggregator:any ${module}
  # OSGi BSN
  bsn=org.${module//-/.}
  %pom_xpath_inject pom:project "<properties><osgi.bsn>${bsn}</osgi.bsn></properties>" ${module}
  # Incorrect scope - API guardian is just annotation, needed only during compilation
  %pom_xpath_set -f "pom:dependency[pom:artifactId='apiguardian-api']/pom:scope" provided ${module}
  %pom_xpath_set -f "pom:dependency[pom:scope='runtime']/pom:scope" compile ${module}
done

%pom_remove_parent junit-bom

# Add deps which are shaded by upstream and therefore not present in POMs.
%pom_add_dep org.junit.platform:junit-platform-commons:%{platform_version} junit-platform-console
%pom_add_dep org.junit.platform:junit-platform-launcher:%{platform_version} junit-platform-console
%pom_add_dep info.picocli:picocli junit-platform-console
%pom_add_dep com.univocity:univocity-parsers:2.5.4 junit-jupiter-params

%pom_disable_module junit-platform-console-standalone
%pom_remove_dep org.junit.platform:junit-platform-reporting junit-platform-console

%mvn_package :aggregator __noinstall

%build
%mvn_build -j -f

%install
%mvn_install

%jpackage_script org.junit.platform.console.ConsoleLauncher "" "" junit5:opentest4j:picocli:junit:hamcrest junit-platform-console

%files -f .mfiles
%{_bindir}/junit-platform-console
%license LICENSE.md LICENSE-notice.md

%changelog
%autochangelog
