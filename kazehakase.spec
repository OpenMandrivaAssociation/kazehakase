%define	name      kazehakase
%define	version   0.4.6
%define	release   %mkrel 1

%define libname_orig lib%{name}
%define libname %mklibname %{name} 0

Name:      %{name}
Summary:   A fast and light tabbed web browser using gecko
Version:   %{version}
Release:   %{release}
URL:       http://kazehakase.sourceforge.jp
Source0:   %{name}-%{version}.tar.gz
# icons
Source10:  %{name}-16.png
Source11:  %{name}-32.png
Source12:  %{name}-48.png
Group:     Networking/WWW
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
License:   GPL
Requires:        %{libname} = %{version}
Requires:        mozilla-firefox
BuildRequires:   intltool
BuildRequires:   mozilla-firefox-devel desktop-file-utils
BuildRequires:   gtk+2-devel automake1.8 gnutls-devel

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
cp /usr/share/automake-1.9/mkinstalldirs .
./autogen.sh
%configure2_5x \
	--enable-migemo 
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

%find_lang %{name}

# icons
mkdir -p %buildroot/{%_liconsdir,%_iconsdir,%_miconsdir}
install -m 644 %SOURCE10 %buildroot/%_miconsdir/%name.png
install -m 644 %SOURCE11 %buildroot/%_iconsdir/%name.png
install -m 644 %SOURCE12 %buildroot/%_liconsdir/%name.png

# remove devel files
rm -f %{buildroot}/%{_libdir}/kazehakase/*.{la,so}

# menu
mkdir -p $RPM_BUILD_ROOT%{_menudir}
cat > $RPM_BUILD_ROOT%{_menudir}/%{name} << _EOF_
?package(%{name}): \
 icon="%{name}.png" \
 title="Kazehakase" \
 longtitle="A fast and light tabbed web browser using gecko" \
 needs="x11" \
 section="Internet/Web Browsers" \
 command="%{name}"\
 xdg="true"
_EOF_

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="GTK" \
  --add-category="X-MandrivaLinux-Internet-WebBrowsers"\
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*


%post
%{update_menus}

%postun
%{clean_menus}

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING COPYING.README 
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
%_menudir/%name
%_liconsdir/%name.png
%_miconsdir/%name.png
%_iconsdir/%name.png

%files -n %{libname}
%defattr(-,root,root)
%doc COPYING
%{_libdir}/kazehakase/*.so.0*


