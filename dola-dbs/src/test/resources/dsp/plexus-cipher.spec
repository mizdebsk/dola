Name:           plexus-cipher
Version:        2.0
Release:        %autorelease
Summary:        Plexus Cipher: encryption/decryption Component
License:        Apache-2.0
URL:            https://github.com/codehaus-plexus/plexus-cipher
BuildArch:      noarch
ExclusiveArch:  %{java_arches} noarch

Source:         %{url}/archive/%{name}-%{version}/%{name}-%{version}.tar.gz

# TODO Remove in Fedora 46
Obsoletes:      %{name}-javadoc < 2.0-28

BuildSystem:    maven
BuildOption:    -DjavaVersion=8

%description
Plexus Cipher: encryption/decryption Component

%files -f .mfiles
%license LICENSE.txt NOTICE.txt

%changelog
%autochangelog
