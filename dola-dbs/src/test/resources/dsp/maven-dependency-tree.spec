%global dola_debug 1
%bcond_with bootstrap

Name:           maven-dependency-tree
Version:        3.2.1
Release:        %autorelease
Summary:        Maven dependency tree artifact
License:        Apache-2.0
URL:            https://maven.apache.org/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://repo1.maven.org/maven2/org/apache/maven/shared/%{name}/%{version}/%{name}-%{version}-source-release.zip

BuildSystem:    maven
BuildOption:    /:apache-rat-plugin
BuildOption:    /:maven-invoker-plugin
BuildOption:    /parent=:@:maven-dependency-tree

%description
Apache Maven dependency tree artifact. Originally part of maven-shared.

%files -f .mfiles
%license LICENSE NOTICE

%changelog
%autochangelog
