Name:           jaxb-istack-commons
Version:        4.2.0
Release:        %autorelease
Summary:        iStack Common Utility Code
License:        BSD-3-Clause
URL:            https://github.com/eclipse-ee4j/jaxb-istack-commons
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  maven-local
BuildRequires:  mvn(jakarta.activation:jakarta.activation-api)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.ant:ant)
BuildRequires:  mvn(org.apache.ant:ant-junit)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-assembly-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-dependency-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-plugin-plugin)
BuildRequires:  mvn(org.glassfish.jaxb:codemodel)

%description
Code shared between JAXP, JAXB, SAAJ, and JAX-WS projects.

%package maven-plugin
Summary:        istack-commons maven-plugin

%description maven-plugin
This package contains istack-commons maven-plugin.

%package runtime
Summary:        istack-commons runtime

%description runtime
This package contains istack-commons runtime.

%package test
Summary:        istack-commons test

%description test
This package contains istack-commons test.

%package tools
Summary:        istack-commons tools

%description tools
This package contains istack-commons tools.

%prep
%autosetup -p1 -C

pushd istack-commons

%pom_remove_parent

%pom_remove_plugin :buildnumber-maven-plugin
%pom_remove_plugin :glassfish-copyright-maven-plugin
%pom_remove_plugin :maven-enforcer-plugin
%pom_remove_plugin :maven-javadoc-plugin . test tools
%pom_remove_plugin :maven-source-plugin
%pom_remove_plugin :spotbugs-maven-plugin

# Missing dependency on args4j
%pom_disable_module soimp

%pom_disable_module buildtools
%pom_disable_module import-properties-plugin

%mvn_package :istack-commons __noinstall
popd

%build
pushd istack-commons
# Javadoc fails on module.info files: "error: too many module declarations found"
%mvn_build -f -s -j
popd

%install
pushd istack-commons
%mvn_install
popd

%files maven-plugin -f istack-commons/.mfiles-istack-commons-maven-plugin
%license LICENSE.md NOTICE.md

%files runtime -f istack-commons/.mfiles-istack-commons-runtime
%license LICENSE.md NOTICE.md

%files test -f istack-commons/.mfiles-istack-commons-test
%license LICENSE.md NOTICE.md

%files tools -f istack-commons/.mfiles-istack-commons-tools
%license LICENSE.md NOTICE.md

%changelog
%autochangelog
