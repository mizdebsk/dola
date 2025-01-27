%bcond_with bootstrap

Name:           xmlunit
Version:        2.10.0
Release:        %autorelease
Summary:        Provides classes to do asserts on xml
# The whole package is ASL 2.0 except for xmlunit-legacy which is BSD
License:        Apache-2.0
URL:            https://www.xmlunit.org/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

# ./generate-tarball.sh
Source0:        %{name}-%{version}.tar.gz
# Remove bundled binaries which cannot be easily verified for licensing
Source1:        generate-tarball.sh

Patch:          0001-Disable-tests-requiring-network-access.patch
# This also solves the problem of tests requiring network. The files that would
# be fetched are identical to the local file
Patch:          0002-Use-local-schema.patch
Patch:          0003-Drop-support-for-JAXB.patch
Patch:          0004-Port-to-assertj-core-3.patch

BuildRequires:  jurand
%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.assertj:assertj-core)
BuildRequires:  mvn(org.hamcrest:hamcrest-core)
BuildRequires:  mvn(org.hamcrest:hamcrest-library)
BuildRequires:  mvn(org.mockito:mockito-core)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 2.10.0-8

%description
XMLUnit provides you with the tools to verify the XML you emit is the one you
want to create. It provides helpers to validate against an XML Schema, assert
the values of XPath queries or compare XML documents against expected outcomes.

%package assertj
Summary:        Assertj for %{name}

%description assertj
This package provides %{summary}.

%package core
Summary:        Core package for %{name}

%description core
This package provides %{summary}.

%package legacy
Summary:        Legacy package for %{name}
License:        BSD-3-Clause

%description legacy
This package provides %{summary}.

%package matchers
Summary:        Matchers for %{name}

%description matchers
This package provides %{summary}.

%package placeholders
Summary:        Placeholders for %{name}

%description placeholders
This package provides %{summary}.

%prep
%autosetup -p1 -C


rm -r xmlunit-core/src/main/java/org/xmlunit/builder/javax_jaxb\
 xmlunit-core/src/main/java/org/xmlunit/builder/JaxbBuilderFactory.java\
 xmlunit-core/src/main/java/org/xmlunit/builder/JaxbBuilderFactoryLocator.java\
 xmlunit-core/src/test/java/org/xmlunit/builder/javax_jaxb\
;


# Port to hamcrest 2.1
%java_remove_annotations xmlunit-matchers -p org[.]hamcrest[.]Factory

%pom_disable_module xmlunit-assertj
%pom_disable_module xmlunit-jakarta-jaxb-impl

%pom_remove_plugin org.codehaus.mojo:buildnumber-maven-plugin
%pom_remove_plugin :maven-assembly-plugin
%pom_remove_plugin -r :maven-shade-plugin
%pom_remove_plugin -r org.cyclonedx:cyclonedx-maven-plugin

%mvn_alias org.xmlunit:xmlunit-legacy xmlunit:xmlunit
%mvn_alias org.xmlunit:xmlunit-assertj3 org.xmlunit:xmlunit-assertj

# JAXB and JAF are not available in JDK11
%pom_remove_dep org.glassfish.jaxb: xmlunit-core
%pom_remove_dep jakarta.xml.bind: xmlunit-core
rm -rf xmlunit-core/src/{main,test}/java/org/xmlunit/builder/{jaxb/,JaxbBuilder.java,JaxbBuilderTest.java}

%build
%mvn_build -j -s -- -Dmaven.compile.source=1.8 -Dmaven.compile.target=1.8

%install
%mvn_install

%files -f .mfiles-xmlunit-parent
%doc README.md CONTRIBUTING.md RELEASE_NOTES.md
%license LICENSE

%files assertj -f .mfiles-xmlunit-assertj3

%files core -f .mfiles-xmlunit-core

%files legacy -f .mfiles-xmlunit-legacy

%files matchers -f .mfiles-xmlunit-matchers

%files placeholders -f .mfiles-xmlunit-placeholders

%changelog
%autochangelog
