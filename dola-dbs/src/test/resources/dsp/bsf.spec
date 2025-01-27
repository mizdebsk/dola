Name:           bsf
Version:        2.4.0
Release:        %autorelease
Summary:        Bean Scripting Framework
License:        Apache-2.0
URL:            https://commons.apache.org/bsf/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://archive.apache.org/dist/commons/bsf/source/bsf-src-%{version}.tar.gz
Source1:        %{name}-pom.xml

Patch:          build-file.patch
Patch:          build.properties.patch

BuildRequires:  javapackages-local
BuildRequires:  ant
BuildRequires:  apache-commons-logging
BuildRequires:  apache-parent
BuildRequires:  xalan-j2
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 2.4.0-63

%description
Bean Scripting Framework (BSF) is a set of Java classes which provides
scripting language support within Java applications, and access to Java
objects and methods from scripting languages. BSF allows one to write
JSPs in languages other than Java while providing access to the Java
class library. In addition, BSF permits any Java application to be
implemented in part (or dynamically extended) by a language that is
embedded within it. This is achieved by providing an API that permits
calling scripting language engines from within Java, as well as an
object registry that exposes Java objects to these scripting language
engines.

BSF supports several scripting languages currently:
* Javascript (using Rhino ECMAScript, from the Mozilla project)
* Python (using either Jython or JPython)
* Tcl (using Jacl)
* NetRexx (an extension of the IBM REXX scripting language in Java)
* XSLT Stylesheets (as a component of Apache XML project's Xalan and
Xerces)

In addition, the following languages are supported with their own BSF
engines:
* Java (using BeanShell, from the BeanShell project)
* JRuby
* JudoScript

%prep
%autosetup -p1 -C
find -name \*.jar -delete

%mvn_file : %{name}
%mvn_alias : org.apache.bsf:

%build
build-jar-repository -s lib apache-commons-logging xalan-j2
%ant -Dsource.level=1.8 -Dant.build.javac.target=1.8 jar

%mvn_artifact %{SOURCE1} build/lib/%{name}.jar

%install
%mvn_install

%files -f .mfiles
%license LICENSE.txt NOTICE.txt
%doc AUTHORS.txt CHANGES.txt README.txt TODO.txt RELEASE-NOTE.txt

%changelog
%autochangelog
