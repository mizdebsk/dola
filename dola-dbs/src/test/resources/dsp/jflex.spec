%bcond_with bootstrap

Name:           jflex
Version:        1.7.0
Release:        %autorelease
Summary:        Fast Scanner Generator
License:        BSD-3-Clause
URL:            https://jflex.de/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

# ./create-tarball.sh %%{version}
Source0:        %{name}-%{version}-clean.tar.gz
Source4:        %{name}.1
Source5:        create-tarball.sh

%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  maven-local
BuildRequires:  mvn(java_cup:java_cup)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.ant:ant)
%endif
%if %{without bootstrap}
BuildRequires:  jflex
%endif
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 1.7.0-44

%description
JFlex is a lexical analyzer generator (also known as scanner
generator) for Java, written in Java.  It is also a rewrite of the
very useful tool JLex which was developed by Elliot Berk at Princeton
University.  As Vern Paxson states for his C/C++ tool flex: They do
not share any code though.  JFlex is designed to work together with
the LALR parser generator CUP by Scott Hudson, and the Java
modification of Berkeley Yacc BYacc/J by Bob Jamison.  It can also be
used together with other parser generators like ANTLR or as a
standalone tool.

%prep
%autosetup -p1 -C
%mvn_file : %{name}
%pom_add_dep java_cup:java_cup

%pom_remove_plugin :jflex-maven-plugin
%pom_remove_plugin :cup-maven-plugin
%pom_remove_plugin :maven-shade-plugin
%pom_remove_dep :cup_runtime

# Tests fail with 320k stacks (default on i686), so lets increase
# stack to 16M to avoid stack overflows.  See rhbz#1119308
%pom_xpath_inject "pom:plugin[pom:artifactId='maven-surefire-plugin']/pom:configuration" "<argLine>-Xss16384k</argLine>"

%pom_xpath_remove "pom:plugin[pom:artifactId='maven-site-plugin']" parent.xml
%pom_xpath_remove "pom:plugin[pom:artifactId='fmt-maven-plugin']" parent.xml
%pom_xpath_remove "pom:plugin[pom:artifactId='cup-maven-plugin']" parent.xml
%pom_xpath_remove "pom:plugin[pom:artifactId='maven-shade-plugin']" parent.xml

%pom_xpath_remove "pom:dependency[pom:artifactId='plexus-compiler-javac-errorprone']" parent.xml
%pom_xpath_remove "pom:dependency[pom:artifactId='error_prone_core']" parent.xml
%pom_xpath_remove "pom:compilerId" parent.xml
%pom_xpath_remove "pom:compilerArgs" parent.xml

sed -i /%%inputstreamctor/d src/main/jflex/LexScan.flex

%build
%{?jpb_env}
cup -parser LexParse -interface -destdir src/main/java src/main/cup/LexParse.cup
jflex -d src/main/java/jflex --skel src/main/jflex/skeleton.nested src/main/jflex/LexScan.flex
%mvn_build -j -- -P\!error-prone -Djflex.jdk.version=1.8

%install
%mvn_install

# wrapper script for direct execution
%jpackage_script jflex.Main "" "" jflex:java_cup jflex true

# manpage
install -d -m 755 %{buildroot}%{_mandir}/man1
install -p -m 644 %{SOURCE4} %{buildroot}%{_mandir}/man1

%files -f .mfiles
%doc doc
%license COPYRIGHT
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*

%changelog
%autochangelog
