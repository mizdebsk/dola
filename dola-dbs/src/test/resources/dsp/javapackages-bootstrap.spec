# Exclude automatically generated requires on java interpreter which is not
# owned by any package
%global __requires_exclude ^%{_jvmdir}/jre
# Generated list of bundled packages
%global _local_file_attrs local_generator
%global __local_generator_provides cat %{_builddir}/%{buildsubdir}/bundled-provides.txt
%global __local_generator_path ^%{metadataPath}/.*$
%global debug_package %{nil}
%global javaHomePath %{_jvmdir}/jre-21-openjdk
%global mavenHomePath %{_datadir}/%{name}
%global metadataPath %{mavenHomePath}/maven-metadata
%global artifactsPath %{_prefix}/lib
%global launchersPath %{_libexecdir}/%{name}

Name:           javapackages-bootstrap
Version:        1.22.0
Release:        %autorelease
Summary:        A means of bootstrapping Java Packages Tools
# For detailed info see the file javapackages-bootstrap-PACKAGE-LICENSING
License:        Apache-1.1 AND Apache-2.0 AND (Apache-2.0 OR EPL-2.0) AND (Apache-2.0 OR LGPL-2.0-or-later) AND BSD-2-Clause AND BSD-3-Clause AND CC0-1.0 AND CPL-1.0 AND EPL-1.0 AND EPL-2.0 AND (EPL-2.0 OR GPL-2.0-only WITH Classpath-exception-2.0) AND LicenseRef-Fedora-Public-Domain AND MIT AND Plexus AND SMLNJ AND Saxpath AND xpp
URL:            https://github.com/fedora-java/javapackages-bootstrap
ExclusiveArch:  %{java_arches}

Source:         https://github.com/fedora-java/javapackages-bootstrap/releases/download/%{version}/javapackages-bootstrap-%{version}.tar.zst
# License breakdown
Source:         javapackages-bootstrap-PACKAGE-LICENSING
# To obtain the following sources:
# tar -xf ${name}-${version}.tar.zst
# pushd ${name}-${version}
# ./downstream.sh clone
# ./downstream.sh prep
# ./downstream.sh archive
# The results are in the archive directory
Source:         ant.tar.zst
Source:         aopalliance.tar.zst
Source:         apache-pom.tar.zst
Source:         apiguardian.tar.zst
Source:         asm.tar.zst
Source:         assertj-core.tar.zst
Source:         bnd.tar.zst
Source:         build-helper-maven-plugin.tar.zst
Source:         byte-buddy.tar.zst
Source:         cdi.tar.zst
Source:         cglib.tar.zst
Source:         chhorz-javadoc-parser.tar.zst
Source:         common-annotations-api.tar.zst
Source:         commons-beanutils.tar.zst
Source:         commons-cli.tar.zst
Source:         commons-codec.tar.zst
Source:         commons-collections.tar.zst
Source:         commons-compress.tar.zst
Source:         commons-io.tar.zst
Source:         commons-jxpath.tar.zst
Source:         commons-lang.tar.zst
Source:         commons-logging.tar.zst
Source:         commons-parent-pom.tar.zst
Source:         cup.tar.zst
Source:         disruptor.tar.zst
Source:         easymock.tar.zst
Source:         extra-enforcer-rules.tar.zst
Source:         felix-parent-pom.tar.zst
Source:         felix-utils.tar.zst
Source:         fusesource-pom.tar.zst
Source:         gson.tar.zst
Source:         guava.tar.zst
Source:         guice.tar.zst
Source:         hamcrest.tar.zst
Source:         httpcomponents-client.tar.zst
Source:         httpcomponents-core.tar.zst
Source:         httpcomponents-parent-pom.tar.zst
Source:         injection-api.tar.zst
Source:         jaf-api.tar.zst
Source:         jansi.tar.zst
Source:         javacc-maven-plugin.tar.zst
Source:         javacc.tar.zst
Source:         javaparser.tar.zst
Source:         jcommander.tar.zst
Source:         jctools.tar.zst
Source:         jdom.tar.zst
Source:         jdom2.tar.zst
Source:         jflex.tar.zst
Source:         jline3.tar.zst
Source:         jsoup.tar.zst
Source:         jsr-305.tar.zst
Source:         junit4.tar.zst
Source:         junit5.tar.zst
Source:         kojan-parent.tar.zst
Source:         kojan-xml.tar.zst
Source:         log4j.tar.zst
Source:         mail-api.tar.zst
Source:         maven-antrun-plugin.tar.zst
Source:         maven-apache-resources.tar.zst
Source:         maven-archiver.tar.zst
Source:         maven-artifact-transfer.tar.zst
Source:         maven-assembly-plugin.tar.zst
Source:         maven-bundle-plugin.tar.zst
Source:         maven-common-artifact-filters.tar.zst
Source:         maven-compiler-plugin.tar.zst
Source:         maven-dependency-analyzer.tar.zst
Source:         maven-dependency-plugin.tar.zst
Source:         maven-dependency-tree.tar.zst
Source:         maven-enforcer.tar.zst
Source:         maven-file-management.tar.zst
Source:         maven-filtering.tar.zst
Source:         maven-jar-plugin.tar.zst
Source:         maven-parent-pom.tar.zst
Source:         maven-plugin-testing.tar.zst
Source:         maven-plugin-tools.tar.zst
Source:         maven-remote-resources-plugin.tar.zst
Source:         maven-resolver.tar.zst
Source:         maven-resolver2.tar.zst
Source:         maven-resources-plugin.tar.zst
Source:         maven-shared-incremental.tar.zst
Source:         maven-shared-io.tar.zst
Source:         maven-shared-utils.tar.zst
Source:         maven-source-plugin.tar.zst
Source:         maven-surefire.tar.zst
Source:         maven-verifier.tar.zst
Source:         maven-wagon.tar.zst
Source:         maven.tar.zst
Source:         maven4.tar.zst
Source:         mockito.tar.zst
Source:         modello.tar.zst
Source:         moditect.tar.zst
Source:         modulemaker-maven-plugin.tar.zst
Source:         mojo-parent-pom.tar.zst
Source:         objenesis.tar.zst
Source:         opentest4j.tar.zst
Source:         osgi-annotation.tar.zst
Source:         osgi-cmpn.tar.zst
Source:         osgi-core.tar.zst
Source:         picocli.tar.zst
Source:         plexus-archiver.tar.zst
Source:         plexus-build-api.tar.zst
Source:         plexus-build-api0.tar.zst
Source:         plexus-cipher.tar.zst
Source:         plexus-classworlds.tar.zst
Source:         plexus-compiler.tar.zst
Source:         plexus-containers.tar.zst
Source:         plexus-interactivity.tar.zst
Source:         plexus-interpolation.tar.zst
Source:         plexus-io.tar.zst
Source:         plexus-languages.tar.zst
Source:         plexus-pom.tar.zst
Source:         plexus-resources.tar.zst
Source:         plexus-sec-dispatcher.tar.zst
Source:         plexus-sec-dispatcher4.tar.zst
Source:         plexus-testing.tar.zst
Source:         plexus-utils.tar.zst
Source:         plexus-utils4.tar.zst
Source:         plexus-xml.tar.zst
Source:         qdox.tar.zst
Source:         servlet-api.tar.zst
Source:         sisu.tar.zst
Source:         slf4j.tar.zst
Source:         slf4j2.tar.zst
Source:         stax2-api.tar.zst
Source:         testng.tar.zst
Source:         univocity-parsers.tar.zst
Source:         velocity-engine.tar.zst
Source:         woodstox.tar.zst
Source:         xmlunit.tar.zst
Source:         xmvn-generator.tar.zst
Source:         xmvn.tar.zst
Source:         xz-java.tar.zst

BuildRequires:  byaccj
BuildRequires:  gcc
BuildRequires:  java-21-openjdk-devel
BuildRequires:  jurand
BuildRequires:  rpm-devel
Requires:       bash
Requires:       coreutils
Requires:       java-21-openjdk-devel
Requires:       javapackages-common
Requires:       lujavrite%{?_isa}
Requires:       procps-ng

%description
In a nutshell, Java Packages Bootstrap (JPB) is a standalone build of all Java
software packages that are required for Java Packages Tools (JPT) to work.

In order to achieve reliable and reproducible builds of Java packages while
meeting Fedora policy that requires everything to be built from source, without
using prebuilt binary artifacts, it is necessary to build the packages in a
well-defined, acyclic order. Dependency cycles between packages are the biggest
obstacle to achieving this goal and JPT is the biggest offender -- it requires
more than a hundred of Java packages, all of which in turn build-require JPT.

JPB comes with a solution to this problem -- it builds everything that JPT needs
to work, without reliance on any Java software other than OpenJDK. JPT can
depend on JPB for everything, without depending on any other Java packages. For
example, JPB contains embedded version of XMvn, removing dependency of JPT on
XMvn, allowing JPT to be used before one builds XMvn package.

%prep
%autosetup -p1 -C
mkdir archive/
cp %{sources} archive/
./downstream.sh prep-from-archive

%build
JAVA_HOME=%{javaHomePath} ./mbi.sh build -parallel

%install
JAVA_HOME=%{javaHomePath} ./mbi.sh dist \
  -javaCmdPath=%{javaHomePath}/bin/java \
  -basePackageName=%{name} \
  -installRoot=%{buildroot} \
  -mavenHomePath=%{mavenHomePath} \
  -metadataPath=%{metadataPath} \
  -artifactsPath=%{artifactsPath} \
  -launchersPath=%{launchersPath} \
  -licensesPath=%{_licensedir}/%{name} \

install -D -p -m 644 downstream/xmvn-generator/src/main/lua/xmvn-generator.lua %{buildroot}%{_rpmluadir}/%{name}-generator.lua
install -D -p -m 644 downstream/xmvn-generator/src/main/rpm/macros.xmvngen %{buildroot}%{_rpmmacrodir}/macros.jpbgen
install -D -p -m 644 downstream/xmvn-generator/src/main/rpm/macros.xmvngenhook %{buildroot}%{_sysconfdir}/rpm/macros.jpbgenhook
install -D -p -m 644 downstream/xmvn-generator/src/main/rpm/xmvngen.attr %{buildroot}%{_fileattrsdir}/jpbgen.attr

echo '
%%__xmvngen_debug 1
%%__xmvngen_libjvm %{javaHomePath}/lib/server/libjvm.so
%%__xmvngen_classpath %{artifactsPath}/%{name}/xmvn-generator.jar:%{artifactsPath}/%{name}/asm.jar:%{artifactsPath}/%{name}/commons-compress.jar:%{artifactsPath}/%{name}/commons-io.jar:%{artifactsPath}/%{name}/xmvn-mojo.jar:%{artifactsPath}/%{name}/kojan-xml.jar:%{artifactsPath}/%{name}/maven-model.jar:%{artifactsPath}/%{name}/plexus-utils.jar
%%__xmvngen_provides_generators org.fedoraproject.xmvn.generator.filesystem.FilesystemGeneratorFactory org.fedoraproject.xmvn.generator.jpscript.JPackageScriptGeneratorFactory org.fedoraproject.xmvn.generator.jpms.JPMSGeneratorFactory org.fedoraproject.xmvn.generator.maven.MavenGeneratorFactory
%%__xmvngen_requires_generators org.fedoraproject.xmvn.generator.filesystem.FilesystemGeneratorFactory org.fedoraproject.xmvn.generator.jpscript.JPackageScriptGeneratorFactory org.fedoraproject.xmvn.generator.maven.MavenGeneratorFactory
%%__xmvngen_post_install_hooks org.fedoraproject.xmvn.generator.transformer.TransformerHookFactory
%%jpb_env PATH=/usr/libexec/javapackages-bootstrap:%{javaHomePath}/bin:$PATH
%%java_home %{javaHomePath}
' >%{buildroot}%{_rpmmacrodir}/macros.jpbgen

sed -i s/xmvn-generator/%{name}-generator/ %{buildroot}%{_sysconfdir}/rpm/macros.jpbgenhook
sed -i s/xmvn-generator/%{name}-generator/ %{buildroot}%{_fileattrsdir}/jpbgen.attr
sed -i s/_xmvngen_/_jpbgen_/ %{buildroot}%{_fileattrsdir}/jpbgen.attr

# Dynamically generate bundled Provides
./downstream.sh bundled-provides >bundled-provides.txt

%check
%{buildroot}%{launchersPath}/xmvn --version

%files
%{mavenHomePath}
%{metadataPath}/*
%{artifactsPath}/*
%{launchersPath}/*
%{_rpmluadir}/*
%{_rpmmacrodir}/*
%{_fileattrsdir}/*
%{_sysconfdir}/rpm/*

%license %{_licensedir}/%{name}
%doc README.md
%doc AUTHORS

%changelog
%autochangelog
