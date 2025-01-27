%bcond_with bootstrap

Name:           apache-commons-codec
Version:        1.17.1
Release:        %autorelease
Summary:        Implementations of common encoders and decoders
License:        Apache-2.0
URL:            https://commons.apache.org/proper/commons-codec/
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source0:        https://archive.apache.org/dist/commons/codec/source/commons-codec-%{version}-src.tar.gz
# Data in DoubleMetaphoneTest.java originally has an inadmissible license.
# The author gives MIT in e-mail communication.
Source1:        aspell-mail.txt

BuildSystem:    maven
BuildOption:    =:>commons-codec>%{name}|commons-codec:commons-codec
BuildOption:    -Dcommons.osgi.symbolicName=org.apache.commons.codec

%description
Commons Codec is an attempt to provide definitive implementations of
commonly used encoders and decoders. Examples include Base64, Hex,
Phonetic and URLs.

%prep -a
cp %{SOURCE1} aspell-mail.txt
sed -i 's/\r//' RELEASE-NOTES*.txt LICENSE.txt NOTICE.txt

%files -f .mfiles
%license LICENSE.txt NOTICE.txt aspell-mail.txt
%doc RELEASE-NOTES*

%changelog
%autochangelog
