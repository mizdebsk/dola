Declarative Spec File Template
------------------------------

```
Name:           ...
Version:        ...
Release:        %autorelease
Summary:        ...
License:        ...
URL:            ...
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source:         ...

BuildSystem:    maven
BuildOption:    ...

%description
...

%files -f .mfiles
%license ...

%changelog
%autochangelog
```

Example:

```
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
```


Maven options
-------------

Profile activation/disactivation:

    BuildOption:    -Prun-its
    BuildOption:    -P!quality,!ci

Defining Maven properties:

    BuildOption:    -Dmaven.compiler.release=21


Options for BuildRequires generation
------------------------------------

Generate additional BuildRequires on Maven artifact:

    BuildOption:    -Bjunit:junit
    BuildOption:    -Borg.slf4j:slf4j-simple::sources:

Filter generated BuildRequires:

    BuildOption:    -B!org.mortbay.jetty:jetty-server


Options for model transformation
--------------------------------

Model transformaton options start with either `/` (removal options) or
with `+` (addition options).

Remove dependency from Maven POM:

    BuildOption:    /dep=org.apache.commons:commons-lang@mygid:myaid
    BuildOption:    /dep=:commons-lang@:myaid
    BuildOption:    /dep=:commons-*
    BuildOption:    /:commons-*

Remove plugin:

    BuildOption:    /plug=org.apache.maven:maven-antrun-plugin@mygid:myaid
    BuildOption:    /plug=:maven-antrun-plugin@:some-project-aid
    BuildOption:    /plug=:maven-antrun-plugin
    BuildOption:    /:maven-antrun-plugin

Remove parent:

    BuildOption:    /parent=org.codehaus.plexus:plexus-pom@some-project-gid:some-project-aid
    BuildOption:    /parent=:@:some-project-aid

Remove subproject:

    BuildOption:    /mod=integration-tests
    BuildOption:    /integration-tests

Add dependency:

    BuildOption:    +dep=org.easymock:easymock:5.6.0:test@mygid:impl
    BuildOption:    +dep=org.apache.maven:maven-model@:modello-core
    BuildOption:    +org.apache.maven:maven-model@:modello-core


Packaging options
-----------------

Packaging options start with `=`

Specify target package for artifact:

    BuildOption:    =gid:aid@subpkgid

Specify artifact alias:

    BuildOption:    =gid:aid|aliasGid:aliasAid
    BuildOption:    =gid:aid|aliasGid:
    BuildOption:    =gid:aid|:aliasAid

Specify artifact file locations:

    BuildOption:    =gid:aid>file
    BuildOption:    =gid:aid>file1>file2

Specify artifact compat versions:

    BuildOption:    =gid:aid;1.2.3
    BuildOption:    =gid:aid;1.2.3;1

Glob matching and backreferences:

    BuildOption:    =gid:{*}|:legacy-@1

Several packaging options at once:

    BuildOption:    =gid:my-artifact>file1>file2@subpkg|:alias
