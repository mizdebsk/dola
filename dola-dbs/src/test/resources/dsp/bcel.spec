Name:           bcel
Version:        6.8.1
Release:        %autorelease
Summary:        Byte Code Engineering Library
License:        Apache-2.0
URL:            https://commons.apache.org/proper/commons-bcel/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        http://archive.apache.org/dist/commons/bcel/source/bcel-%{version}-src.tar.gz

BuildRequires:  maven-local
BuildRequires:  mvn(org.apache.commons:commons-lang3)
BuildRequires:  mvn(org.apache.commons:commons-parent:pom:)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 6.8.1-14

%description
The Byte Code Engineering Library (formerly known as JavaClass) is
intended to give users a convenient possibility to analyze, create, and
manipulate (binary) Java class files (those ending with .class). Classes
are represented by objects which contain all the symbolic information of
the given class: methods, fields and byte code instructions, in
particular.  Such objects can be read from an existing file, be
transformed by a program (e.g. a class loader at run-time) and dumped to
a file again. An even more interesting application is the creation of
classes from scratch at run-time. The Byte Code Engineering Library
(BCEL) may be also useful if you want to learn about the Java Virtual
Machine (JVM) and the format of Java .class files.  BCEL is already
being used successfully in several projects such as compilers,
optimizers, obsfuscators and analysis tools, the most popular probably
being the Xalan XSLT processor at Apache.

%prep
%autosetup -p1 -C

%pom_remove_plugin :maven-source-plugin
%pom_remove_plugin :spotbugs-maven-plugin
%pom_remove_plugin :jacoco-maven-plugin

%mvn_alias : bcel: apache:
%mvn_file : %{name}

%build
%mvn_build -j -f

%install
%mvn_install

%files -f .mfiles
%doc RELEASE-NOTES.txt
%license LICENSE.txt NOTICE.txt

%changelog
%autochangelog
