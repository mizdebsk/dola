Name:           xalan-j2
Version:        2.7.3
Release:        %autorelease
Summary:        Java XSLT processor
# src/org/apache/xpath/domapi/XPathStylesheetDOM3Exception.java is W3C
License:        Apache-2.0 AND W3C
URL:            https://xalan.apache.org
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

# ./generate-tarball.sh
Source0:        %{name}-%{version}.tar.gz
Source2:        https://repo1.maven.org/maven2/xalan/xalan/%{version}/xalan-%{version}.pom
Source3:        https://repo1.maven.org/maven2/xalan/serializer/%{version}/serializer-%{version}.pom
Source4:        xsltc-%{version}.pom
# Remove bundled binaries which cannot be easily verified for licensing
Source6:        generate-tarball.sh

Patch:          xalan-j2-noxsltcdeps.patch

BuildRequires:  javapackages-local
BuildRequires:  ant
BuildRequires:  apache-parent
BuildRequires:  bcel
BuildRequires:  java_cup
BuildRequires:  regexp
BuildRequires:  sed
BuildRequires:  xerces-j2 >= 0:2.7.1
BuildRequires:  xml-commons-apis >= 0:1.3
Requires:       xerces-j2
Provides:       jaxp_transform_impl

%description
Xalan is an XSLT processor for transforming XML documents into HTML,
text, or other XML document types. It implements the W3C Recommendations
for XSL Transformations (XSLT) and the XML Path Language (XPath). It can
be used from the command line, in an applet or a servlet, or as a module
in other program.

%package xsltc
Summary:        XSLT compiler
License:        Apache-2.0
Requires:       bcel
Requires:       java_cup
Requires:       regexp
Requires:       xerces-j2

%description xsltc
The XSLT Compiler is a Java-based tool for compiling XSLT stylesheets into
lightweight and portable Java byte codes called translets.

%package manual
Summary:        Manual for %{name}
License:        Apache-2.0

%description manual
Documentation for %{name}.

%prep
%autosetup -p1 -C

sed -i '/<bootclasspath/d' build.xml

# Remove classpaths from manifests
sed -i '/class-path/I d' $(find -iname '*manifest*')

# Convert CR-LF to LF-only
sed -i 's/\r//' KEYS LICENSE.txt NOTICE.txt xdocs/style/resources/script.js \
    xdocs/sources/xsltc/README* `find -name '*.sh'`

%mvn_file :xalan %{name} jaxp_transform_impl
%mvn_file :serializer %{name}-serializer
%mvn_file :xsltc xsltc
%mvn_package :xsltc xsltc

%build
%ant \
  -Dcompiler.source=1.8 \
  -Dcompiler.target=1.8 \
  -Djava.awt.headless=true \
  -Dbuild.xalan-interpretive.jar=build/xalan-interpretive.jar \
  -Dxmlapis.jar=$(build-classpath xml-commons-apis) \
  -Dparser.jar=$(build-classpath xerces-j2) \
  -Dbcel.jar=$(build-classpath bcel) \
  -Druntime.jar=$(build-classpath java_cup-runtime) \
  -Dregexp.jar=$(build-classpath regexp) \
  -Djava_cup.jar=$(build-classpath java_cup) \
  xalan-interpretive.jar \
  xsltc.unbundledjar \
  docs

%mvn_artifact %{SOURCE2} build/xalan-interpretive.jar
%mvn_artifact %{SOURCE3} build/serializer.jar
%mvn_artifact %{SOURCE4} build/xsltc.jar

%install
%mvn_install

%files -f .mfiles
%license LICENSE.txt NOTICE.txt
%doc KEYS README

%files xsltc -f .mfiles-xsltc
%license LICENSE.txt NOTICE.txt

%files manual
%license LICENSE.txt NOTICE.txt
%doc build/docs/*

%changelog
%autochangelog
