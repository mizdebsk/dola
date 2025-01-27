%bcond_with bootstrap

Name:           plexus-utils
Version:        3.5.1
Release:        %autorelease
Summary:        Plexus Common Utilities
# ASL 1.1: several files in src/main/java/org/codehaus/plexus/util/
# xpp: src/main/java/org/codehaus/plexus/util/xml/pull directory
# ASL 2.0 and BSD:
#      src/main/java/org/codehaus/plexus/util/cli/StreamConsumer.java
#      src/main/java/org/codehaus/plexus/util/cli/StreamPumper.java
#      src/main/java/org/codehaus/plexus/util/cli/Commandline.java
# Public domain: src/main/java/org/codehaus/plexus/util/TypeFormat.java
# rest is ASL 2.0
License:        Apache-1.1 AND Apache-2.0 AND xpp AND BSD-3-Clause AND LicenseRef-Fedora-Public-Domain
URL:            https://codehaus-plexus.github.io/plexus-utils/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://github.com/codehaus-plexus/plexus-utils/archive/plexus-utils-%{version}.tar.gz

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(org.codehaus.plexus:plexus:pom:)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 3.5.1-21

%description
The Plexus project seeks to create end-to-end developer tools for
writing applications. At the core is the container, which can be
embedded or for a full scale application server. There are many
reusable components for hibernate, form processing, jndi, i18n,
velocity, etc. Plexus also includes an application server which
is like a J2EE application server, without all the baggage.

%prep
%autosetup -p1 -C

%mvn_file : plexus/utils
%mvn_alias : plexus:plexus-utils

%build
%mvn_build -j -f

%install
%mvn_install

%files -f .mfiles
%license NOTICE.txt LICENSE.txt

%changelog
%autochangelog
