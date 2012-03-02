Name:           kmediafactory
Version:        0.8.0
Release:        3%{?dist}
Summary:        A template based DVD authoring tool

Group:          User Interface/Desktops
License:        GPLv2+
URL:            http://code.google.com/p/kmediafactory/ 
Source0:        http://kmediafactory.googlecode.com/files/kmediafactory-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# rpmfusion's mlt binary is named mlt-melt:
Patch1: kmediafactory-0.8.0-mlt-melt.patch

## upstreamable patches
Patch50: kmediafactory-0.8.0-docbook_fix.patch
Patch51: kmediafactory-0.8.0-dso.patch

BuildRequires:  kdelibs4-devel
BuildRequires:  dvdauthor
BuildRequires:  dvd-slideshow
BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  giflib-devel
BuildRequires:  libdvdread-devel 
BuildRequires:  mlt
BuildRequires:  mjpegtools 
BuildRequires:  pcre-devel
BuildRequires:  zip 

Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: kdebase-runtime%{?_kde4_version: >= %{_kde4_version}}
%{?_kde4_macros_api:Requires: kde4-macros(api) = %{_kde4_macros_api} }

# needed for normal functionality
Requires: dvdauthor
Requires: dvd-slideshow
Requires: ffmpeg
Requires: mjpegtools
Requires: mplayer
# optional bits
#Requires(hint): mlt

%description
Kmediafactory is an easy to use template based dvd authoring tool. 
You can quickly create DVD menus for home videos and TV 
recordings in three simple steps.

%package libs
Summary: Runtime libraries for %{name}
Group:   System Environment/Libraries
Requires: %{name} = %{version}-%{release}
%description libs
%{summary}.

%package devel
Summary: Development files for kmediafactory
Group: Development/Libraries
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
%description devel
Development files for %{name}.


%prep
%setup -q

%patch1 -p1 -b .mlt-melt
%patch50 -p1
%patch51 -p1 -b .dso


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot}
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

# validate desktop file
desktop-file-install --vendor=""                          \
        --dir %{buildroot}%{_kde4_datadir}/applications/kde4   \
        --remove-category="Application"                   \
        --add-category="X-OutputGeneration"               \
        %{buildroot}%{_kde4_datadir}/applications/kde4/kmediafactory.desktop

# locale
%find_lang kmediafactory --with-kde
%find_lang kmediafactory_kstore
%find_lang kmediafactory_output
%find_lang kmediafactory_slideshow
%find_lang kmediafactory_template
%find_lang kmediafactory_video
%find_lang libkmf
cat kmediafactory*.lang > kmediafactory-all.lang


%clean
rm -rf %{buildroot}


%post
touch --no-create %{_kde4_iconsdir}/hicolor || :

%postun
if [ $1 -eq 0 ]; then
update-desktop-database &> /dev/null ||:
update-mime-database %{_datadir}/mime &> /dev/null || :
touch --no-create %{_kde4_iconsdir}/hicolor || :
gtk-update-icon-cache --quiet %{_kde4_iconsdir}/hicolor &> /dev/null || :
fi

%posttrans
update-desktop-database &> /dev/null ||:
update-mime-database %{_datadir}/mime &> /dev/null || :
gtk-update-icon-cache --quiet %{_kde4_iconsdir}/hicolor &> /dev/null || :

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%files -f kmediafactory-all.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING CREDITS NEWS README TODO
%{_kde4_bindir}/kmediafactory
%{_kde4_appsdir}/kmediafactory/
%{_kde4_appsdir}/kmediafactory_template/
%{_kde4_appsdir}/kmfwidgets/
%{_kde4_datadir}/config.kcfg/*
%{_kde4_datadir}/config/*
%{_kde4_datadir}/kde4/services/*
%{_kde4_datadir}/kde4/servicetypes/*
%{_kde4_iconsdir}/hicolor/*/*/*
%{_kde4_libdir}/kde4/kmediafactory_*
%{_kde4_libdir}/kde4/plugins/designer/kmfwidgets.so
%{_kde4_datadir}/applications/kde4/kmediafactory.desktop
%{_datadir}/mime/packages/kmediafactory.xml

%files libs -f libkmf.lang
%defattr(-,root,root,-)
%{_kde4_libdir}/libkmediafactoryinterfaces.so.0*
%{_kde4_libdir}/libkmediafactorykstore.so.0*
%{_kde4_libdir}/libkmf.so.0*

%files devel
%defattr(-,root,root,-)
%{_kde4_includedir}/kmediafactory/
%{_kde4_libdir}/lib*.so


%changelog
* Fri Mar 02 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.8.0-3
- Rebuilt for c++ ABI breakage

* Wed Feb 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 14 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.8.0-1
- kmediafactory-0.8.0
- optimize scriptlets

* Fri Oct 23 2009 Orcan Ogetbil <oged[DOT]fedora[AT]gmail[DOT]com> - 0.7.1-2
- Update desktop file according to F-12 FedoraStudio feature

* Wed Apr 08 2009 Sebastian Vahl <fedora@deadbabylon.de> - 0.7.1-1
- new upstream version: 0.7.1

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.7.0-0.3.rc2
- rebuild for new F11 features

* Thu Sep 04 2008 Sebastian Vahl <fedora@deadbabylon.de> - 0.7.0-0.2.rc2
- fix url

* Thu Aug 21 2008 Sebastian Vahl <fedora@deadbabylon.de> - 0.7.0-0.1.rc2
- new upstream version: 0.7.0-rc2

* Tue Jul 22 2008 Sebastian Vahl <fedora@deadbabylon.de> - 0.6.0-5
- import into rpmfusion

* Thu Apr 03 2008 Rex Dieter <rdieter@fedoraproject.org> - 0.6.0-4
- -libs subpkg (multilib friendly)
- restore upstream (kde4) desktop-file vendor
- rebuild (again) for NDEBUG
- drop Requires: kdelibs4 (let rpm autoreq this)

* Tue Apr 01 2008 Sebastian Vahl <fedora@deadbabylon.de> - 0.6.0-3
- rebuild for NDEBUG and _kde4_libexecdir
- use correct versioned require on kdelibs4

* Mon Feb 25 2008 Sebastian Vahl <fedora@deadbabylon.de> - 0.6.0-2
- fix %%post and %%postun
- BR: desktop-file-utils
- desktop-file: use vendor "rpmfusion"
- desktop-file: remove category "Application"
- fix wrong directory ownerships

* Mon Feb 18 2008 Sebastian Vahl <fedora@deadbabylon.de> - 0.6.0-1
- Update to KDE4 version: 0.6.0

* Wed Oct 25 2006 Sebastian Vahl <fedora@deadbabylon.de> - 0.5.2-2
- Rebuild for FC6

* Mon Jun 19 2006 Sebastian Vahl <fedora@deadbabylon.de> - 0.5.2-1
- New upstream Version: 0.5.2

* Fri Apr 07 2006 Sebastian Vahl <fedora@deadbabylon.de> - 0.5.1-1
- Version 0.5.1 (final)

* Wed Apr 05 2006 Sebastian Vahl <fedora@deadbabylon.de> - 0.5.1-0.1.rc3
- Release Candidat rc3

* Wed Mar 29 2006 Sebastian Vahl <fedora@deadbabylon.de> - 0.5.1-0.1.rc1
- Release Candidat rc1

* Tue Mar 21 2006 Sebastian Vahl <fedora@deadbabylon.de> - 0.5.0-1.20060311
- Updated to snapshot version

* Tue Jan 24 2006 Sebastian Vahl <fedora@deadbabylon.de> - 0.5.0-1
- Updated to new version
- Added README.fedora

* Mon Oct 03 2005 Sebastian Vahl <fedora@deadbabylon.de> - 0.4.1-1
- Updated to new version
- Recode some doc files from ISO-8859 to UTF-8
- Some spec cleanup
- Added libtheora-devel to BuildRequires
- Added Patch to get mjpegtools to work

* Wed Aug 24 2005 Sebastian Vahl <fedora@deadbabylon.de> - 0.4.0-2
- Added zip to BuildRequires ann Requires
- Added sox to Requires

* Tue Aug 16 2005 Sebastian Vahl <fedora@deadbabylon.de> - 0.4.0-1
- Initial Release
