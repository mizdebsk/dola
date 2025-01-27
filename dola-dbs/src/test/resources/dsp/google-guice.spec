%bcond_with bootstrap

Name:           google-guice
Version:        5.1.0
Release:        %autorelease
Summary:        Lightweight dependency injection framework for Java 5 and above
License:        Apache-2.0
URL:            https://github.com/google/guice
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

# ./create-tarball.sh %%{version}
Source0:        %{name}-%{version}.tar.xz
Source1:        create-tarball.sh

BuildRequires:  jurand
%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(aopalliance:aopalliance)
BuildRequires:  mvn(com.google.code.findbugs:jsr305)
BuildRequires:  mvn(com.google.guava:guava)
BuildRequires:  mvn(javax.inject:javax.inject)
BuildRequires:  mvn(javax.servlet:servlet-api)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-remote-resources-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-source-plugin)
BuildRequires:  mvn(org.ow2.asm:asm)
%endif
%if %{without bootstrap}
# xmvn-builddep misses this:
BuildRequires:  mvn(org.apache:apache-jar-resource-bundle)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 5.1.0-27

%description
Put simply, Guice alleviates the need for factories and the use of new
in your Java code. Think of Guice's @Inject as the new new. You will
still need to write factories in some cases, but your code will not
depend directly on them. Your code will be easier to change, unit test
and reuse in other contexts.

Guice embraces Java's type safe nature, especially when it comes to
features introduced in Java 5 such as generics and annotations. You
might think of Guice as filling in missing features for core
Java. Ideally, the language itself would provide most of the same
features, but until such a language comes along, we have Guice.

Guice helps you design better APIs, and the Guice API itself sets a
good example. Guice is not a kitchen sink. We justify each feature
with at least three use cases. When in doubt, we leave it out. We
build general functionality which enables you to extend Guice rather
than adding every feature to the core framework.

%package -n guice-parent
Summary:        Guice parent POM

%description -n guice-parent
Guice is a lightweight dependency injection framework for Java 5
and above. This package provides parent POM for Guice modules.

%package -n guice-assistedinject
Summary:        AssistedInject extension module for Guice

%description -n guice-assistedinject
Guice is a lightweight dependency injection framework for Java 5
and above. This package provides AssistedInject module for Guice.

%package -n guice-extensions
Summary:        Extensions for Guice

%description -n guice-extensions
Guice is a lightweight dependency injection framework for Java 5
and above. This package provides extensions POM for Guice.

%package -n guice-grapher
Summary:        Grapher extension module for Guice

%description -n guice-grapher
Guice is a lightweight dependency injection framework for Java 5
and above. This package provides Grapher module for Guice.

%package -n guice-jmx
Summary:        JMX extension module for Guice

%description -n guice-jmx
Guice is a lightweight dependency injection framework for Java 5
and above. This package provides JMX module for Guice.

%package -n guice-jndi
Summary:        JNDI extension module for Guice

%description -n guice-jndi
Guice is a lightweight dependency injection framework for Java 5
and above. This package provides JNDI module for Guice.

%package -n guice-servlet
Summary:        Servlet extension module for Guice

%description -n guice-servlet
Guice is a lightweight dependency injection framework for Java 5
and above. This package provides Servlet module for Guice.

%package -n guice-throwingproviders
Summary:        ThrowingProviders extension module for Guice

%description -n guice-throwingproviders
Guice is a lightweight dependency injection framework for Java 5
and above. This package provides ThrowingProviders module for Guice.

%package -n guice-bom
Summary:        Bill of Materials for Guice

%description -n guice-bom
Guice is a lightweight dependency injection framework for Java 5
and above. This package provides Bill of Materials module for Guice.

%prep
%autosetup -p1 -C

%java_remove_annotations core/src/ \
  -p ^com.google.common.annotations. \
  -p ^com.google.errorprone.annotations. \

# We don't have struts2 in Fedora yet.
%pom_disable_module struts2 extensions
# Android-specific extension
%pom_disable_module dagger-adapter extensions

# Remove additional build profiles, which we don't use anyways
# and which are only pulling additional dependencies.
%pom_xpath_remove "pom:profile[pom:id='guice.with.jarjar']" core

# Fix OSGi metadata due to not using jarjar
%pom_xpath_set "pom:instructions/pom:Import-Package" \
  "!com.google.inject.*,*" core

# Animal sniffer is only causing problems. Disable it for now.
%pom_remove_plugin :animal-sniffer-maven-plugin core
%pom_remove_plugin :animal-sniffer-maven-plugin extensions

%pom_remove_plugin :maven-gpg-plugin

# We don't have the custom doclet used by upstream. Remove
# maven-javadoc-plugin to generate javadocs with default style.
%pom_remove_plugin -r :maven-javadoc-plugin

# remove test dependency to make sure we don't produce requires
# see #1007498
%pom_remove_dep :guava-testlib extensions
%pom_xpath_remove "pom:dependency[pom:classifier='tests']" extensions

%pom_remove_parent

%pom_disable_module persist extensions
%pom_disable_module spring extensions
%pom_disable_module testlib extensions

#%pom_remove_dep :aopalliance core
#%pom_remove_dep :asm core
#%pom_remove_dep :cglib core
#%pom_xpath_remove "pom:plugin[pom:artifactId='maven-jar-plugin']/pom:configuration"
#%pom_xpath_remove "pom:plugin[pom:artifactId='maven-jar-plugin']/pom:executions"
#%pom_xpath_set "pom:plugin[pom:artifactId='munge-maven-plugin']/pom:executions/pom:execution/pom:phase" generate-sources core
#%pom_xpath_set "pom:plugin[pom:artifactId='munge-maven-plugin']/pom:executions/pom:execution/pom:goals/pom:goal" munge core

#%pom_xpath_inject "pom:dependency[pom:artifactId='guice']" "<scope>provided</scope>" extensions

%mvn_alias :guice :::classes:

%build
#%mvn_alias "com.google.inject.extensions:" "org.sonatype.sisu.inject:"

#%mvn_package :::no_aop: guice
#%mvn_package :guice:jar:{}: __noinstall

%mvn_file  ":guice-{*}"  guice/guice-@1
%mvn_file  ":guice" guice/%{name} %{name}
#%mvn_alias ":guice" "org.sonatype.sisu:sisu-guice"
# Skip tests because of missing dependency guice-testlib
%mvn_build -j -f -s

%install
%mvn_install

%files -f .mfiles-guice

%files -n guice-parent -f .mfiles-guice-parent
%license COPYING

%files -n guice-assistedinject -f .mfiles-guice-assistedinject

%files -n guice-extensions -f .mfiles-extensions-parent

%files -n guice-grapher -f .mfiles-guice-grapher

%files -n guice-jmx -f .mfiles-guice-jmx

%files -n guice-jndi -f .mfiles-guice-jndi

%files -n guice-servlet -f .mfiles-guice-servlet

%files -n guice-throwingproviders -f .mfiles-guice-throwingproviders

%files -n guice-bom -f .mfiles-guice-bom

%changelog
%autochangelog
