%bcond_with bootstrap

Name:           woodstox-core
Version:        7.1.0
Release:        %autorelease
Summary:        High-performance XML processor
License:        Apache-2.0
URL:            https://github.com/FasterXML/woodstox
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        %{url}/archive/%{name}-%{version}.tar.gz

# Port to latest OSGi APIs
Patch:          0001-Allow-building-against-OSGi-APIs-newer-than-R4.patch
# Drop requirements on defunct optional dependencies: msv and relaxng
Patch:          0002-Patch-out-optional-support-for-msv-and-relax-schema-.patch

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(biz.aQute.bnd:biz.aQute.bnd.annotation)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.codehaus.woodstox:stax2-api)
BuildRequires:  mvn(org.mockito:mockito-core)
BuildRequires:  mvn(org.osgi:osgi.core)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 7.1.0-5

%description
Woodstox is a high-performance namespace-aware StAX-compliant
(JSR-173) Open Source XML-processor written in Java.  XML processor
means that it handles both input (parsing) and output (writing,
serialization), as well as supporting tasks such as validation.

%prep
%autosetup -p1 -C
%pom_remove_parent
%pom_remove_plugin :nexus-staging-maven-plugin
%pom_remove_plugin :jacoco-maven-plugin

# comment in src/moditect/module-info.java explains it...
# // hand-crafted on 14-Jul-2019 -- probably all wrong
%pom_remove_plugin :moditect-maven-plugin

# Patch out optional support for msv and relax schema validation
%pom_remove_dep net.java.dev.msv:
%pom_remove_dep :relaxngDatatype
%pom_remove_dep :isorelax
%pom_remove_plugin :maven-shade-plugin
rm -r src/main/java/com/ctc/wstx/msv
rm src/test/java/failing/{RelaxNGTest,TestRelaxNG189,TestRelaxNG190,TestW3CSchema189,W3CDefaultValuesTest,W3CSchemaTypesTest}.java
rm src/test/java/stax2/vwstream/{W3CSchemaWrite16Test,W3CSchemaWrite23Test}.java
rm src/test/java/wstxtest/msv/{TestW3CSchema,TestW3CSchemaTypes,TestWsdlValidation}.java
rm src/test/java/wstxtest/vstream/{TestRelaxNG,TestW3CSchemaComplexTypes}.java

%build
%mvn_build -j -- -Dversion.junit=4.12

%install
%mvn_install

%files -f .mfiles
%doc README.md
%license LICENSE

%changelog
%autochangelog
