%define major		0
%define libname		%mklibname %{name} %{major}

Name:		kazehakase
Summary:	A fast and light tabbed web browser using webkit
Version:	0.5.8
Release:	%mkrel 4
URL:		http://kazehakase.sourceforge.jp
Source0:	http://jaist.dl.sourceforge.jp/kazehakase/43802/%{name}-%{version}.tar.gz
Source10:	%{name}-16.png
Source11:	%{name}-32.png
Source12:	%{name}-48.png
Patch0:		kazehakase-0.5.8-fix-linkage.patch
Patch1:		kazehakase-0.5.8-gtk2.20.patch
Group:		Networking/WWW
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
License:	GPLv2+
Requires:	%{libname} = %{version}
BuildRequires:	intltool
BuildRequires:	webkitgtk-devel
BuildRequires:	desktop-file-utils
BuildRequires:	gtk+2-devel
BuildRequires:	automake
BuildRequires:	gnutls-devel

%description
Kazehakase is a fast and light tabbed browser using webkit.
"Kaze" means "wind", and "Hakase" means "Dr." in Japanese.

%package -n %{libname}
Summary:	Kazehakase library
Group:		System/Internationalization

%description -n %{libname}
Kazehakase library.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p0
%patch1 -p2

%build
./autogen.sh
%configure2_5x \
	--enable-migemo \
	--with-gecko-engine=no
make

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
rm -f %{buildroot}/%{_libdir}/kazehakase/*.{la,so} %{buildroot}/%{_libdir}/kazehakase/*/*.la

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
%{_libdir}/kazehakase/embed/webkit_gtk.so
%{_libdir}/kazehakase/embed/per_process.so
%dir %{_libdir}/kazehakase/search
%{_mandir}/man1/*
%{_iconsdir}/hicolor/*/apps/%{name}.png

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/kazehakase/*.so.%{major}*
