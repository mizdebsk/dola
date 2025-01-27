%bcond_with bootstrap

Name:           maven-shared-utils
Version:        3.4.2
Release:        %autorelease
Summary:        Maven shared utility classes
License:        Apache-2.0
URL:            https://maven.apache.org/shared/maven-shared-utils
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://repo1.maven.org/maven2/org/apache/maven/shared/%{name}/%{version}/%{name}-%{version}-source-release.zip

Patch:          0001-Avoid-setting-POSIX-attributes-for-symbolic-links.patch

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(com.google.code.findbugs:jsr305)
BuildRequires:  mvn(commons-io:commons-io)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.maven.shared:maven-shared-components:pom:)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:  mvn(org.fusesource.jansi:jansi)
BuildRequires:  mvn(org.hamcrest:hamcrest-core)
BuildRequires:  mvn(org.slf4j:slf4j-api)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 3.4.2-22

%description
This project aims to be a functional replacement for plexus-utils in Maven.

It is not a 100% API compatible replacement though but a replacement with
improvements: lots of methods got cleaned up, generics got added and we dropped
a lot of unused code.

%prep
%autosetup -p1 -C

find -name '*.java' -exec sed -i 's/\r//' {} +


%pom_remove_dep org.apache.commons:commons-text
rm src/test/java/org/apache/maven/shared/utils/CaseTest.java

%build
%mvn_build -j

%install
%mvn_install

%files -f .mfiles
%license LICENSE NOTICE

%changelog
%autochangelog
