%define _requires_exceptions libnspr4\\|libplc4\\|libplds4\\|libnss\\|libsmime3\\|libsoftokn\\|libssl3\\|libgtkembedmoz\\|libxpcom
%define xulrunner 1.9
%define xulname %mklibname xulrunner %xulrunner
%define xulver %(rpm -q --queryformat %%{VERSION} %xulname)

%define major		0
%define libname		%mklibname %{name} %{major}

%define rel	3
%define svn	0

%if %svn
%define release		%mkrel 0.%{svn}.%{rel}
%define distname	%{name}-%{svn}.tar.lzma
%define dirname		%{name}
%else
%define release		%mkrel %{rel}
%define distname	%{name}-%{version}.tar.gz
%define dirname		%{name}-%{version}
%endif

Name:		kazehakase
Summary:	A fast and light tabbed web browser using gecko
Version:	0.5.6
Release:	%{release}
URL:		http://kazehakase.sourceforge.jp
Source0:	%{distname}
# icons
Source10:	%{name}-16.png
Source11:	%{name}-32.png
Source12:	%{name}-48.png
Patch0:		kazehakase-0.5.5-gentoo-xulrunner19.patch
Patch1:		kazehakase-0.5.5-underlink.patch
Patch2:		kazehakase-0.5.6-fix-str-fmt.patch
Group:		Networking/WWW
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
License:	GPLv2+
Requires:	%{libname} = %{version}
Requires:	%{xulname} = %{xulver}
BuildRequires:	intltool
BuildRequires:	xulrunner-devel-unstable
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

%description -n %{libname}
Kazehakase library.


%prep
%setup -q -n %{dirname}
%patch0 -p1 -b .xul
%patch1 -p1 -b .underlink
%patch2 -p0 -b .str

%build
./autogen.sh
%configure2_5x \
	--enable-migemo \
	--with-gecko-engine=libxul
%make

%install
rm -rf %{buildroot}
%makeinstall_std

%find_lang %{name}

# icons
mkdir -p %{buildroot}/%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
install -m 644 %{SOURCE10} %{buildroot}/%{_iconsdir}/hicolor/16x16/apps/%{name}.png
install -m 644 %{SOURCE11} %{buildroot}/%{_iconsdir}/hicolor/32x32/apps/%{name}.png
install -m 644 %{SOURCE12} %{buildroot}/%{_iconsdir}/hicolor/48x48/apps/%{name}.png

# remove devel files
rm -f %{buildroot}/%{_libdir}/kazehakase/*.{la,so}

# menu
sed -i -e 's,kazehakase-icon.png,%{name},g' %{buildroot}%{_datadir}/applications/*
desktop-file-install --vendor="" \
  --remove-key="Encoding" \
  --remove-category="Application" \
  --add-category="GTK" \
  --add-category="WebBrowser" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

%if %mdkversion < 200900
%post
%{update_menus}
%{update_icon_cache hicolor}
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%{clean_icon_cache hicolor}
%endif

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING.README 
%doc README README.ja TODO.ja
%config(noreplace) %{_sysconfdir}/kazehakase/*
%{_bindir}/*
%{_datadir}/applications/*
%{_datadir}/%{name}
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
