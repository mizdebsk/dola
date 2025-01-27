%define __requires_exclude system.bundle
%global cvs_version %(tr . _ <<< %{version})

Name:           xerces-j2
Version:        2.12.2
Release:        %autorelease
Summary:        Java XML parser
# Most of the source is ASL 2.0
# W3C licensed files:
# src/org/apache/xerces/dom3/as
# src/org/w3c/dom/html/HTMLDOMImplementation.java
License:        Apache-2.0 AND W3C
URL:            https://xerces.apache.org/xerces2-j/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        http://mirror.ox.ac.uk/sites/rsync.apache.org/xerces/j/source/Xerces-J-src.%{version}.tar.gz
# Custom javac ant task used by the build
Source3:        https://svn.apache.org/repos/asf/xerces/java/tags/Xerces-J_%{cvs_version}/tools/src/XJavac.java
Source7:        %{name}-pom.xml
Source11:       %{name}-version.1
Source12:       %{name}-constants.1

# Patch the build so that it doesn't try to use bundled xml-commons source
Patch:          %{name}-build.patch
# Patch the manifest so that it includes OSGi stuff
Patch:          %{name}-manifest.patch

BuildRequires:  javapackages-local
BuildRequires:  ant
BuildRequires:  apache-parent
BuildRequires:  xml-commons-apis >= 1.4.01
BuildRequires:  xml-commons-resolver >= 1.2
Requires:       xml-commons-apis >= 1.4.01
Requires:       xml-commons-resolver >= 1.2
# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 2.12.2-32
Provides:       %{name}-scripts = %{version}-%{release}
Provides:       jaxp_parser_impl = 1.4

%description
Welcome to the future! Xerces2 is the next generation of high performance,
fully compliant XML parsers in the Apache Xerces family. This new version of
Xerces introduces the Xerces Native Interface (XNI), a complete framework for
building parser components and configurations that is extremely modular and
easy to program.

The Apache Xerces2 parser is the reference implementation of XNI but other
parser components, configurations, and parsers can be written using the Xerces
Native Interface. For complete design and implementation documents, refer to
the XNI Manual.

Xerces2 is a fully conforming XML Schema processor. For more information,
refer to the XML Schema page.

Xerces2 also provides a complete implementation of the Document Object Model
Level 3 Core and Load/Save W3C Recommendations and provides a complete
implementation of the XML Inclusions (XInclude) W3C Recommendation. It also
provides support for OASIS XML Catalogs v1.1.

Xerces2 is able to parse documents written according to the XML 1.1
Recommendation, except that it does not yet provide an option to enable
normalization checking as described in section 2.13 of this specification. It
also handles name spaces according to the XML Namespaces 1.1 Recommendation,
and will correctly serialize XML 1.1 documents if the DOM level 3 load/save
APIs are in use.

%package demo
Summary:        Demonstrations and samples for %{name}
Requires:       %{name} = %{version}-%{release}

%description demo
%{summary}.

%prep
%autosetup -p1 -C

# Copy the custom ant task into place
mkdir -p tools/org/apache/xerces/util
mkdir -p tools/bin
cp -a %{SOURCE3} tools/org/apache/xerces/util

# Make sure upstream hasn't sneaked in any jars we don't know about
find . \( -name '*.class' -o -name '*.jar' \) -delete

sed -i 's/\r//' LICENSE README NOTICE

# Disable javadoc linting
sed -i -e "s|additionalparam='|additionalparam='-Xdoclint:none |" build.xml

# legacy aliases for compatability
%mvn_alias : xerces:xerces xerces:xmlParserAPIs apache:xerces-j2
%mvn_file : %{name} jaxp_parser_impl

%build
pushd tools

# Build custom ant tasks
%javac -classpath $(build-classpath ant) org/apache/xerces/util/XJavac.java
%jar cf bin/xjavac.jar org/apache/xerces/util/XJavac.class

%jar cmf /dev/null serializer.jar
ln -sf $(build-classpath xml-commons-apis) xml-apis.jar
ln -sf $(build-classpath xml-commons-resolver) resolver.jar
popd

# Build everything
export ANT_OPTS="-Xmx512m -Djava.awt.headless=true -Dbuild.sysclasspath=first -Ddisconnected=true"
%ant -Djavac.source=1.8 -Djavac.target=1.8 \
    -Dbuild.compiler=modern \
    clean jars

%mvn_artifact %{SOURCE7} build/xercesImpl.jar

%install
%mvn_install

# scripts
%jpackage_script org.apache.xerces.impl.Version "" "" %{name} %{name}-version 1
%jpackage_script org.apache.xerces.impl.Constants "" "" %{name} %{name}-constants 1

# manual pages
install -d -m 755 %{buildroot}%{_mandir}/man1
install -p -m 644 %{SOURCE11} %{buildroot}%{_mandir}/man1
install -p -m 644 %{SOURCE12} %{buildroot}%{_mandir}/man1

# demo
install -d -m 755 %{buildroot}%{_datadir}/%{name}/
install -p -m 644 build/xercesSamples.jar %{buildroot}%{_datadir}/%{name}/%{name}-samples.jar
cp -pr data %{buildroot}%{_datadir}/%{name}

%files -f .mfiles
%doc LICENSE NOTICE README
%{_bindir}/*
%{_mandir}/*/*

%files demo
%{_datadir}/%{name}

%changelog
%autochangelog
