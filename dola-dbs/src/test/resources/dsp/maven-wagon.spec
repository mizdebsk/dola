%bcond_with bootstrap

Name:           maven-wagon
Version:        3.5.3
Release:        %autorelease
Summary:        Tools to manage artifacts and deployment
License:        Apache-2.0
URL:            https://maven.apache.org/wagon
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://repo1.maven.org/maven2/org/apache/maven/wagon/wagon/%{version}/wagon-%{version}-source-release.zip

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(org.apache.httpcomponents:httpclient)
BuildRequires:  mvn(org.apache.httpcomponents:httpcore)
BuildRequires:  mvn(org.apache.maven:maven-parent:pom:)
BuildRequires:  mvn(org.codehaus.plexus:plexus-component-metadata)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:  mvn(org.slf4j:jcl-over-slf4j)
BuildRequires:  mvn(org.slf4j:slf4j-api)
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 3.5.3-21
Provides:       maven-wagon-file = %{version}-%{release}
Provides:       maven-wagon-http = %{version}-%{release}
Provides:       maven-wagon-http-shared = %{version}-%{release}
Provides:       maven-wagon-provider-api = %{version}-%{release}
Provides:       maven-wagon-providers = %{version}-%{release}

%description
Maven Wagon is a transport abstraction that is used in Maven's
artifact and repository handling code. Currently wagon has the
following providers:
* File
* HTTP
* FTP
* SSH/SCP
* WebDAV
* SCM (in progress)

%prep
%autosetup -p1 -C

%pom_remove_plugin :animal-sniffer-maven-plugin
%pom_remove_plugin :maven-enforcer-plugin
%pom_remove_dep :wagon-tck-http wagon-providers/wagon-http

# disable tests, missing dependencies
%pom_disable_module wagon-tcks
%pom_disable_module wagon-ssh-common-test wagon-providers
%pom_disable_module wagon-provider-test
%pom_remove_dep :wagon-provider-test
%pom_remove_dep :wagon-provider-test wagon-providers

# missing dependencies
%pom_disable_module wagon-ftp wagon-providers
%pom_disable_module wagon-http-lightweight wagon-providers
%pom_disable_module wagon-scm wagon-providers
%pom_disable_module wagon-ssh wagon-providers
%pom_disable_module wagon-ssh-common wagon-providers
%pom_disable_module wagon-ssh-external wagon-providers
%pom_disable_module wagon-webdav-jackrabbit wagon-providers

# Adjust dependency scopes for better interoperability with Maven 4
%pom_change_dep :jcl-over-slf4j :::test wagon-providers/wagon-http
%pom_change_dep :slf4j-api :::provided wagon-providers/wagon-http-shared
%pom_change_dep -r :plexus-utils :::provided

%pom_remove_plugin :maven-shade-plugin wagon-providers/wagon-http

%mvn_file ":wagon-{*}" %{name}/@1
%mvn_package ":wagon"

%build
# tests are disabled because of missing dependencies
%mvn_build -j -f -- -DjavaVersion=8

# Maven requires Wagon HTTP with classifier "shaded"
%mvn_alias :wagon-http :::shaded:

%install
%mvn_install

%files -f .mfiles
%license LICENSE NOTICE
%doc DEPENDENCIES

%changelog
%autochangelog
