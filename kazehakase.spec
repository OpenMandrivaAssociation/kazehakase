%define	name      kazehakase
%define	version   0.5.0
%define	release   %mkrel 2

%define libname_orig	lib%{name}
%define major		0
%define libname		%mklibname %{name} %{major}

Name:		%{name}
Summary:	A fast and light tabbed web browser using gecko
Version:	%{version}
Release:	%{release}
URL:		http://kazehakase.sourceforge.jp
Source0:	%{name}-%{version}.tar.gz
# icons
Source10:	%{name}-16.png
Source11:	%{name}-32.png
Source12:	%{name}-48.png
Group:		Networking/WWW
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
License:	GPLv2+
Requires:	%{libname} = %{version}
Requires:	mozilla-firefox
BuildRequires:	intltool
BuildRequires:	mozilla-firefox-devel
BuildRequires:	desktop-file-utils
BuildRequires:	gtk+2-devel
BuildRequires:	automake
BuildRequires:	gnutls-devel

%description
Kazehakase is a fast and light tabbed browser using gecko.
"Kaze" means "wind", and "Hakase" means "Dr." in Japanese.


%package -n %{libname}
Summary:	Kazehakase library
Group:		System/Internationalization
Provides:	%{libname_orig} = %{version}-%{release}

%description -n %{libname}
Kazehakase library.


%prep
%setup -q

%build
# force to regenerate configure
cp /usr/share/automake-1.10/mkinstalldirs .
./autogen.sh
%configure2_5x \
	--enable-migemo 
%make

%install
rm -rf %{buildroot}
%makeinstall_std

%find_lang %{name}

# icons
mkdir -p %{buildroot}/%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
install -m 644 %SOURCE10 %{buildroot}/%{_iconsdir}/hicolor/16x16/apps/%{name}.png
install -m 644 %SOURCE11 %{buildroot}/%{_iconsdir}/hicolor/32x32/apps/%{name}.png
install -m 644 %SOURCE12 %{buildroot}/%{_iconsdir}/hicolor/48x48/apps/%{name}.png

# remove devel files
rm -f %{buildroot}/%{_libdir}/kazehakase/*.{la,so}

# menu
perl -pi -e 's,kazehakase-icon.png,%{name},g' %{buildroot}%{_datadir}/applications/*
desktop-file-install --vendor="" \
  --remove-key="Encoding" \
  --remove-category="Application" \
  --add-category="GTK" \
  --add-category="WebBrowser" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

%post
%{update_menus}
%{update_icon_cache hicolor}

%postun
%{clean_menus}
%{clean_icon_cache hicolor}

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING.README 
%doc README README.ja TODO.ja
%config(noreplace) %{_sysconfdir}/kazehakase/*
%{_bindir}/*
%{_datadir}/applications/*
%{_datadir}/kazehakase/kz-no-thumbnail.png
%{_datadir}/kazehakase/search-result.css
%{_datadir}/kazehakase/icons/*
%{_datadir}/pixmaps/*
%dir %{_libdir}/kazehakase
%dir %{_libdir}/kazehakase/embed
%{_libdir}/kazehakase/embed/gecko.la
%{_libdir}/kazehakase/embed/gecko.so
%dir %{_libdir}/kazehakase/search
%{_mandir}/man1/*
%{_iconsdir}/hicolor/*/apps/%{name}.png

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/kazehakase/*.so.%{major}*
