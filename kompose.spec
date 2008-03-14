Name: kompose
Summary: Provides a full screen view of all open windows
Version: 0.5.3
Release: 11%{?dist}
License: GPLv2+
Group: User Interface/X
Url: http://kompose.berlios.de
Source: http://download.berlios.de/kompose/%{name}-%{version}.tar.bz2
Patch0: kompose-0.5.3-x.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: kdelibs3-devel >= 3.2, imlib2-devel
BuildRequires: libXcomposite-devel, libXdamage-devel
Requires: kdebase3

%description
Komposé currently allows a fullscreen view of all your virtual desktops where
every window is represented by a scaled screenshot of it's own.

The Composite extension is used if available from the X server.


%prep
%setup -q
%patch -p1 -b .x


%build
unset QTDIR || : ; . /etc/profile.d/qt.sh
export QTLIB=${QTDIR}/lib QTINC=${QTDIR}/include
%configure --disable-rpath
make %{?_smp_mflags}


%install
%makeinstall
desktop-file-install --vendor=fedora \
       --add-category=Qt \
       --add-category=KDE \
       --add-category=Utility \
       --delete-original --dir %{buildroot}%{_datadir}/applications \
       $RPM_BUILD_ROOT%{_datadir}/applnk/Utilities/kompose.desktop
install -D src/hi32-app-kompose.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/kompose.png
#Fix doc link
ln -sf ../common $RPM_BUILD_ROOT%{_defaultdocdir}/HTML/en/%{name}

## File lists
# locale's
%find_lang %{name} || touch %{name}.lang
# HTML
HTML_DIR=$(kde-config --expandvars --install html)
if [ -d $RPM_BUILD_ROOT$HTML_DIR ]; then
for lang_dir in $RPM_BUILD_ROOT$HTML_DIR/* ; do
   lang=$(basename $lang_dir)
   echo "%lang($lang) %doc $HTML_DIR/$lang/*" >> %{name}.lang
done
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS COPYING README
%{_bindir}/kompose
%{_datadir}/applications/fedora-kompose.desktop
%{_datadir}/apps/kompose/
%{_datadir}/pixmaps/kompose.png

%changelog
* Fri Mar 14 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.5.3-11
- Add BR libXcomposite-devel and libXdamage-devel

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.5.3-10
- Autorebuild for GCC 4.3

* Wed Jan  9 2008 - Orion Poplawski <orion@cora.nwra.com> 0.5.3-9
- Change BR to kdelibs3-devel

* Tue Aug 21 2007 - Orion Poplawski <orion@cora.nwra.com> 0.5.3-8
- Update license tag to GPLv2+
- Rebuild for BuildID

* Mon Oct 30 2006 - Orion Poplawski <orion@cora.nwra.com> 0.5.3-7
- Rebuild for new imlib2
- Remove X-Fedora desktop category

* Tue Aug 29 2006 - Orion Poplawski <orion@cora.nwra.com> 0.5.3-6
- Revert to 0.5.3 and rebuild for FC6.  0.5.4 does not compile

* Mon Jun 12 2006 - Orion Poplawski <orion@cora.nwra.com> 0.5.4-1
- Update to 0.5.4
- Make description UTF-8

* Mon Feb 27 2006 - Orion Poplawski <orion@cora.nwra.com> 0.5.3-5
- Rebuild for FE5

* Thu Dec 22 2005 - Orion Poplawski <orion@cora.nwra.com> 0.5.3-4
- Add patch to remove X checks in configure for modular X

* Mon Jul 25 2005 - Orion Poplawski <orion@cora.nwra.com> 0.5.3-3
- Requires kdebase
- Fix doc symlink.

* Fri Jul 22 2005 - Orion Poplawski <orion@cora.nwra.com> 0.5.3-2
- More spec cleanup

* Fri Jul 22 2005 - Orion Poplawski <orion@cora.nwra.com> 0.5.3-1
- Update to 0.5.3
- Cleanup spec file

* Tue Jul 05 2005 - Orion Poplawski <orion@cora.nwra.com> 0.5.2-0.beta1
- Initial Fedora Extras package
