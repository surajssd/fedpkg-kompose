Name: kompose
Summary: Provides a full screen view of all open windows
Version: 0.5.3
Release: 3%{?dist}
License: GPL
Group: User Interface/X
Url: http://kompose.berlios.de
Source: http://download.berlios.de/kompose/%{name}-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: kdelibs-devel >= 3.2, imlib2-devel
Requires: kdebase

%description
Komposé currently allows a fullscreen view of all your virtual desktops where
every window is represented by a scaled screenshot of it's own.

The Composite extension is used if available from the X server.


%prep
%setup -q

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
       --add-category=X-Fedora \
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
