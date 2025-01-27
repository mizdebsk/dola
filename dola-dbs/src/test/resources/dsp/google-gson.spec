%global dola_debug 1

Name:           google-gson
Version:        2.12.1
Release:        %autorelease
Summary:        Java lib for conversion of Java objects into JSON representation
# Automatically converted from old format: ASL 2.0 - review is highly recommended.
License:        Apache-2.0
URL:            https://github.com/google/gson
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://github.com/google/gson/archive/gson-parent-%{version}.tar.gz

Patch:          0001-Fix-build.patch

BuildRequires:  jurand
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 2.12.1-3

BuildSystem:    maven
BuildOption:    -B!org.xolstice.maven.plugins:protobuf-maven-plugin
BuildOption:    -Borg.apache.maven.plugins:maven-resources-plugin
BuildOption:    -Borg.apache.maven.plugins:maven-compiler-plugin
BuildOption:    -Borg.apache.maven.plugins:maven-surefire-plugin
BuildOption:    -Borg.apache.maven.plugins:maven-jar-plugin
BuildOption:    /:maven-enforcer-plugin
BuildOption:    /:spotless-maven-plugin
BuildOption:    /:maven-artifact-plugin
BuildOption:    /:maven-failsafe-plugin
BuildOption:    /:bnd-maven-plugin
BuildOption:    /:error_prone_annotations
# The test EnumWithObfuscatedTest requires the plugins copy-rename-maven-plugin, proguard-maven-plugin and maven-resources-plugin to work correctly because it tests Gson interaction with a class obfuscated by ProGuard.
# https://github.com/google/gson/issues/2045
BuildOption:    !EnumWithObfuscatedTest
# to check later
BuildOption:    !DefaultDateTypeAdapterTest
BuildOption:    /:copy-rename-maven-plugin
BuildOption:    /:proguard-maven-plugin
BuildOption:    /:moditect-maven-plugin
# Remove dependency on unavailable templating-maven-plugin
BuildOption:    /:templating-maven-plugin
# depends on com.google.caliper
BuildOption:    /metrics
# depends on com.google.protobuf:protobuf-java:jar:4.0.0-rc-2 and com.google.truth:truth:jar:1.1.3
BuildOption:    /proto
BuildOption:    /test-jpms
BuildOption:    /test-graal-native-image
BuildOption:    /test-shrinker

%description
Gson is a Java library that can be used to convert a Java object into its
JSON representation. It can also be used to convert a JSON string into an
equivalent Java object. Gson can work with arbitrary Java objects including
pre-existing objects that you do not have source-code of.

%prep -a
%java_remove_annotations gson extras -s \
  -p com[.]google[.]errorprone[.]annotations[.] \

# Remove dependency on unavailable templating-maven-plugin
sed 's/${project.version}/%{version}/' gson/src/main/java-templates/com/google/gson/internal/GsonBuildConfig.java >gson/src/main/java/com/google/gson/internal/GsonBuildConfig.java

%files -f .mfiles
%license LICENSE
%doc README.md CHANGELOG.md UserGuide.md

%changelog
%autochangelog
