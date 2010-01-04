%define name gambas2
%define version 2.19.0
%define release %mkrel 1

Name: %{name}
Summary: Complete IDE based on a BASIC interpreter with object extensions
Version: %{version}
Release: %{release}
License: GPLv2+
Group: Development/Other
URL: http://gambas.sourceforge.net/
Source0: http://ovh.dl.sourceforge.net/sourceforge/gambas/%{name}-%version.tar.bz2
BuildRoot: %{_tmppath}/%{name}-buildroot
BuildRequires: bzip2-devel
BuildRequires: firebird-devel
BuildRequires: libunixODBC-devel
BuildRequires: libsqlite-devel
BuildRequires: libsqlite3-devel
BuildRequires: gtk+2-devel
BuildRequires: libmesagl-devel
BuildRequires: libmesaglu-devel
BuildRequires: libpcre-devel
BuildRequires: libSDL_image-devel
BuildRequires: libSDL_gfx-devel
BuildRequires: libSDL_ttf-devel
BuildRequires: nas-devel
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: libxml2-devel
BuildRequires: libxslt-devel
BuildRequires: gettext-devel
BuildRequires: qt3-devel
%if %mdkversion < 201000
BuildRequires: kdelibs-devel
%endif
BuildRequires: libcurl-devel
BuildRequires: libgettextmisc
BuildRequires: libopenssl-devel
BuildRequires: libSDL-devel
BuildRequires: libpoppler-devel
BuildRequires: mysql-devel
BuildRequires: postgresql-devel
BuildRequires: SDL_mixer-devel
BuildRequires: acl-devel
BuildRequires: imagemagick
BuildRequires: ffi-devel

Obsoletes: gambas < 2.0.0

%description
Gambas is a free development environment based on a Basic interpreter
with object extensions, like Visual Basic(tm) (but it is NOT a clone!). 
With Gambas, you can quickly design your program GUI, access MySQL or
PostgreSQL databases, control KDE applications with DCOP, translate
your program into many languages, create network applications easily,
build RPMs of your apps automatically, and so on...

%prep
%setup -q -n %{name}-%version

%build
%configure2_5x \
	--disable-corba --disable-qte
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

mkdir -p $RPM_BUILD_ROOT/%{_miconsdir}
mkdir -p $RPM_BUILD_ROOT/%{_iconsdir}
mkdir -p $RPM_BUILD_ROOT/%{_liconsdir}
mkdir -p $RPM_BUILD_ROOT/%{_iconsdir}/hicolor/{16x16,32x32,48x48,128x128}/{apps,mimetypes}
install -m644 app/src/gambas2/img/logo/new-logo-16.png $RPM_BUILD_ROOT/%{_miconsdir}/%{name}.png
install -m644 app/src/gambas2/img/logo/new-logo-16.png $RPM_BUILD_ROOT/%{_iconsdir}/hicolor/16x16/apps/%{name}.png
install -m644 app/src/gambas2/img/logo/new-logo-32.png $RPM_BUILD_ROOT/%{_iconsdir}/%{name}.png
install -m644 app/src/gambas2/img/logo/new-logo-32.png $RPM_BUILD_ROOT/%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert -resize 48x48 app/src/gambas2/img/logo/new-logo.png $RPM_BUILD_ROOT/%{_liconsdir}/%{name}.png
convert -resize 48x48 app/src/gambas2/img/logo/new-logo.png $RPM_BUILD_ROOT/%{_iconsdir}/hicolor/48x48/apps/%{name}.png
install -m644 app/src/gambas2/img/logo/new-logo.png $RPM_BUILD_ROOT/%{_iconsdir}/hicolor/128x128/apps/%{name}.png

install -m644 app/mime/application-x-gambasscript.png %buildroot%{_iconsdir}/hicolor/48x48/mimetypes/application-x-gambasscript.png
convert -resize 16x16 app/mime/application-x-gambasscript.png %buildroot%{_iconsdir}/hicolor/16x16/mimetypes/application-x-gambasscript.png
convert -resize 32x32 app/mime/application-x-gambasscript.png %buildroot%{_iconsdir}/hicolor/32x32/mimetypes/application-x-gambasscript.png
install -m644 main/mime/application-x-gambas.png %buildroot%{_iconsdir}/hicolor/48x48/mimetypes/
convert -resize 16x16 main/mime/application-x-gambas.png %buildroot%{_iconsdir}/hicolor/16x16/mimetypes/application-x-gambas.png
convert -resize 32x32 main/mime/application-x-gambas.png %buildroot%{_iconsdir}/hicolor/32x32/mimetypes/application-x-gambas.png

# Clean some files that do not need to be packaged according to docs

rm -f $RPM_BUILD_ROOT%_libdir/%{name}/gb.la $RPM_BUILD_ROOT%_libdir/%{name}/gb.so*

# Menu

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop <<EOF
[Desktop Entry]
Name=Gambas 2
Comment=Gambas 2 IDE
Exec=%{_bindir}/%{name} 
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=GNOME;GTK;Development;IDE;
EOF

# XDG MIME type
install -D app/mime/application-x-gambasscript.xml %buildroot%{_datadir}/mime/packages/application-x-gambasscript.xml
install -D main/mime/application-x-gambas.xml %buildroot%{_datadir}/mime/packages/application-x-gambas.xml

#-----------------------------------------------------------------------------

%package runtime
Summary: The Gambas runtime
Group: Development/Other
Obsoletes: gambas2-gb-draw
Obsoletes: gambas-gb-eval < 2.0.0
Obsoletes: gambas-gb-debug < 2.0.0
Obsoletes: gambas-runtime < 2.0.0

%description runtime
This package includes the Gambas interpreter needed to run Gambas applications.

%if %mdkversion < 200900
%post runtime
%update_mime_database
%update_icon_cache hicolor
%endif

%if %mdkversion < 200900
%postun runtime
%update_mime_database
%update_icon_cache hicolor
%endif

%files runtime
%defattr(-, root, root, 0755)
%doc README AUTHORS ChangeLog
%{_bindir}/gbx2
%{_bindir}/gbr2
%{_libdir}/%{name}/gb.component
%{_libdir}/%{name}/gb.debug.*
%{_libdir}/%{name}/gb.eval.*
%{_libdir}/%{name}/gb.draw.*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/info/gb.info
%{_datadir}/%{name}/info/gb.list
%{_datadir}/%{name}/info/gb.debug.*
%{_datadir}/%{name}/info/gb.eval.*
%{_datadir}/%{name}/icons/application-x-gambas.png
%{_datadir}/mime/packages/application-x-gambas.xml
%{_iconsdir}/hicolor/*/mimetypes/application-x-gambas.png

#-----------------------------------------------------------------------------

%package devel
Summary: The Gambas development package
Group: Development/Other

%description devel
This package includes all tools needed to compile Gambas projects
without having to install the complete development environment.

%files devel
%defattr(-, root, root, 0755)
%{_bindir}/gbc2
%{_bindir}/gba2
%{_bindir}/gbi2

#-----------------------------------------------------------------------------

%package script
Summary: The Gambas scripter package
Group: Development/Other
Requires: %{name}-runtime = %{version}
Requires: %{name}-devel = %{version}

%description script
This package includes the scripter program that allows to write script files
in Gambas.

%if %mdkversion < 200900
%post script
%update_mime_database
%update_icon_cache hicolor
%endif

%if %mdkversion < 200900
%postun script
%clean_mime_database
%clean_icon_cache hicolor
%endif

%files script
%defattr(-, root, root, 0755)
%{_bindir}/gbs2
%{_bindir}/gbs2.gambas
%{_datadir}/%{name}/icons/application-x-gambasscript.png
%{_datadir}/%{name}/icons/application-x-gambasserverpage.png
%{_datadir}/mime/packages/application-x-gambasscript.xml
%{_iconsdir}/hicolor/*/mimetypes/application-x-gambasscript.png

#-----------------------------------------------------------------------------

%package ide
Summary: The Gambas IDE
Group: Development/Other
Requires: %{name}-runtime = %{version}
Requires: %{name}-devel = %{version}
Requires: %{name}-gb-chart = %{version}
Requires: %{name}-gb-compress = %{version}
Requires: %{name}-gb-crypt = %{version}
Requires: %{name}-gb-db = %{version}
Requires: %{name}-gb-db-firebird = %{version}
Requires: %{name}-gb-db-form = %{version}
Requires: %{name}-gb-db-mysql = %{version}
Requires: %{name}-gb-db-odbc = %{version}
Requires: %{name}-gb-db-postgresql = %{version}
Requires: %{name}-gb-db-sqlite2 = %{version}
Requires: %{name}-gb-db-sqlite3 = %{version}
Requires: %{name}-gb-desktop = %{version}
Requires: %{name}-gb-form = %{version}
Requires: %{name}-gb-form-dialog = %{version}
Requires: %{name}-gb-form-mdi = %{version}
Requires: %{name}-gb-gtk = %{version}
Requires: %{name}-gb-gui = %{version}
Requires: %{name}-gb-image = %{version}
Requires: %{name}-gb-info = %{version}
Obsoletes: %{name}-gb-ldap
Requires: %{name}-gb-net = %{version}
Requires: %{name}-gb-net-curl = %{version}
Requires: %{name}-gb-net-smtp = %{version}
Requires: %{name}-gb-opengl = %{version}
Requires: %{name}-gb-option = %{version}
Requires: %{name}-gb-pcre = %{version}
Requires: %{name}-gb-pdf = %{version}
Requires: %{name}-gb-qt = %{version}
Requires: %{name}-gb-qt-ext = %{version}
%if %mdkversion < 201000
Requires: %{name}-gb-qt-kde = %{version}
Requires: %{name}-gb-qt-kde-html = %{version}
%endif
Requires: %{name}-gb-qt-opengl = %{version}
Requires: %{name}-gb-report = %{version}
Requires: %{name}-gb-sdl = %{version}
Requires: %{name}-gb-sdl-sound = %{version}
Requires: %{name}-gb-settings = %{version}
Requires: %{name}-gb-v4l = %{version}
Requires: %{name}-gb-vb = %{version}
Requires: %{name}-gb-web = %{version}
Requires: %{name}-gb-xml = %{version}
Requires: %{name}-gb-xml-rpc = %{version}
Requires: %{name}-gb-xml-xslt = %{version}
Requires: rpm-build
Obsoletes: gambas-ide < 2.0.0

%description ide
This package includes the complete Gambas Development Environment, with the
database manager, the help files, and all components.

%if %mdkversion < 200900
%post ide
%update_menus
%update_icon_cache hicolor
%endif

%if %mdkversion < 200900
%postun ide
%clean_menus
%clean_icon_cache hicolor
%endif

%files ide
%defattr(-, root, root, 0755)
%{_bindir}/%{name}
%{_bindir}/%{name}.gambas
%{_bindir}/%{name}-database-manager.gambas
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_datadir}/applications/mandriva-%{name}.desktop

#-----------------------------------------------------------------------------

%package examples
Summary: The Gambas examples
Group: Development/Other
Requires: %{name}-ide = %{version}
Conflicts: %{name}-ide < 2.6.0-2

%description examples
This package includes all the example projects provided with Gambas.

%files examples
%defattr(-,root,root)
%{_datadir}/%{name}/examples

#-----------------------------------------------------------------------------

%package help
Summary: The Gambas Help files
Group: Development/Other
Requires: %{name}-ide = %{version}
Conflicts: %{name}-ide < 2.6.0-2

%description help
This package includes the help files generated from the wiki located at http://gambasdoc.org.

%files help
%defattr(-,root,root)
%{_datadir}/%{name}/help

#-----------------------------------------------------------------------------

%package gb-chart
Summary: The Gambas chart component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-chart
This is a component that draws charts.

%files gb-chart
%defattr(-,root,root)
%{_libdir}/%{name}/gb.chart.*
%{_datadir}/%{name}/info/gb.chart.*

#-----------------------------------------------------------------------------

%package gb-compress
Summary: The Gambas compression component
Group: Development/Other
Requires: %{name}-runtime = %{version}
Obsoletes: gambas-gb-compress < 2.0.0

%description gb-compress
This component allows you to compress/uncompress data or files with
the bzip2 and zip algorithms.

%files gb-compress
%defattr(-,root,root)
%{_libdir}/%{name}/gb.compress.*
%{_datadir}/%{name}/info/gb.compress.*

#-----------------------------------------------------------------------------

%package gb-crypt
Summary: The Gambas cryptography component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-crypt
This component allows you to use cryptography in your projects.

%files gb-crypt
%defattr(-,root,root)
%{_libdir}/%{name}/gb.crypt.*
%{_datadir}/%{name}/info/gb.crypt.*

#-----------------------------------------------------------------------------

%package gb-db
Summary: The Gambas database component
Group: Development/Other
Requires: %{name}-runtime = %{version}
Obsoletes: gambas-gb-db < 2.0.0

%description gb-db
This component allows you to access many databases management systems,
provided that you install the needed driver packages.

%files gb-db
%defattr(-,root,root)
%{_libdir}/%{name}/gb.db.la
%{_libdir}/%{name}/gb.db.so*
%{_libdir}/%{name}/gb.db.component
%{_datadir}/%{name}/info/gb.db.info
%{_datadir}/%{name}/info/gb.db.list

#-----------------------------------------------------------------------------

%package gb-db-firebird
Summary: The Firebird driver for the Gambas database component
Group: Development/Other
Requires: %{name}-runtime = %{version},%{name}-gb-db = %{version}

%description gb-db-firebird
This component allows you to access Firebird databases.

%files gb-db-firebird
%defattr(-,root,root)
%{_libdir}/%{name}/gb.db.firebird.*

#-----------------------------------------------------------------------------

%package gb-db-form
Summary: The bound controls for the Gambas database component
Group: Development/Other
Requires: %{name}-runtime = %{version},%{name}-gb-db = %{version}

%description gb-db-form
This component implements data bound controls. It provides the
following new controls: DataSource, DataBrowser, DataView, 
DataControl and DataCombo.

%files gb-db-form
%defattr(-,root,root)
%{_libdir}/%{name}/gb.db.form.*
%{_datadir}/%{name}/info/gb.db.form.*

#-----------------------------------------------------------------------------

%package gb-db-mysql
Summary: The MySQL driver for the Gambas database component
Group: Development/Other
Requires: %{name}-runtime = %{version},%{name}-gb-db = %{version}
Obsoletes: gambas-gb-db-mysql < 2.0.0

%description gb-db-mysql
This component allows you to access MySQL databases.

%files gb-db-mysql
%defattr(-,root,root)
%{_libdir}/%{name}/gb.db.mysql.*

#-----------------------------------------------------------------------------

%package gb-db-odbc
Summary: The ODBC driver for the Gambas database component
Group: Development/Other
Requires: %{name}-runtime = %{version},%{name}-gb-db = %{version}

%description gb-db-odbc
This component allows you to access ODBC databases.

%files gb-db-odbc
%defattr(-,root,root)
%{_libdir}/%{name}/gb.db.odbc.*

#-----------------------------------------------------------------------------

%package gb-db-postgresql
Summary: The PostgreSQL driver for the Gambas database component
Group: Development/Other
Requires: %{name}-runtime = %{version},%{name}-gb-db = %{version}
Obsoletes: gambas-gb-db-postgresql < 2.0.0

%description gb-db-postgresql
This component allows you to access PostgreSQL databases.

%files gb-db-postgresql
%defattr(-,root,root)
%{_libdir}/%{name}/gb.db.postgresql.*

#-----------------------------------------------------------------------------

%package gb-db-sqlite2
Summary: The SQLite 2 driver for the Gambas database component
Group: Development/Other
Requires: %{name}-runtime = %{version},%{name}-gb-db = %{version}
Obsoletes: gambas-gb-db-sqlite < 2.0.0

%description gb-db-sqlite2
This component allows you to access SQLite 2 databases.

%files gb-db-sqlite2
%defattr(-,root,root)
%{_libdir}/%{name}/gb.db.sqlite2.*

#-----------------------------------------------------------------------------

%package gb-db-sqlite3
Summary: The SQLite 3 driver for the Gambas database component
Group: Development/Other
Requires: %{name}-runtime = %{version},%{name}-gb-db = %{version}

%description gb-db-sqlite3
This component allows you to access SQLite 3 databases.

%files gb-db-sqlite3
%defattr(-,root,root)
%{_libdir}/%{name}/gb.db.sqlite3.*

#-----------------------------------------------------------------------------

%package gb-desktop
Summary: The Gambas XDG component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-desktop
This component allows you to use desktop-agnostic routines based on 
the xdg-utils scripts of the Portland project.

%files gb-desktop
%defattr(-,root,root)
%{_libdir}/%{name}/gb.desktop.*
%{_datadir}/%{name}/info/gb.desktop.*

#-----------------------------------------------------------------------------

%package gb-form
Summary: The Gambas form component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-form
This component serves as base for graphic components.

%files gb-form
%defattr(-,root,root)
%{_libdir}/%{name}/gb.form.component
%{_libdir}/%{name}/gb.form.gambas
%{_datadir}/%{name}/info/gb.form.info
%{_datadir}/%{name}/info/gb.form.list

#-----------------------------------------------------------------------------

%package gb-form-dialog
Summary: The Gambas dialog form component
Group: Development/Other
Requires: %{name}-runtime = %{version},%{name}-gb-form = %{version}
Conflicts: %{name}-gb-form < %{version}

%description gb-form-dialog
This component implements the Workspace control.

%files gb-form-dialog
%defattr(-,root,root)
%{_libdir}/%{name}/gb.form.dialog.*
%{_datadir}/%{name}/info/gb.form.dialog.*

#-----------------------------------------------------------------------------

%package gb-form-mdi
Summary: The Gambas MDI form component
Group: Development/Other
Requires: %{name}-runtime = %{version},%{name}-gb-form = %{version}

%description gb-form-mdi
This component implements the Workspace control.

%files gb-form-mdi
%defattr(-,root,root)
%{_libdir}/%{name}/gb.form.mdi.*
%{_datadir}/%{name}/info/gb.form.mdi.*

#-----------------------------------------------------------------------------

%package gb-gtk
Summary: The Gambas GTK+ GUI component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-gtk
This package contains the Gambas GTK+ GUI components.

%files gb-gtk
%defattr(-,root,root)
%{_libdir}/%{name}/gb.gtk.*
%{_datadir}/%{name}/info/gb.gtk.*

#-----------------------------------------------------------------------------

%package gb-gui
Summary: The Gambas GUI component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-gui
This is a component that just loads gb.qt if you are running KDE or
gb.gtk in the other cases.

%files gb-gui
%defattr(-,root,root)
%{_libdir}/%{name}/gb.gui.*
%{_datadir}/%{name}/info/gb.gui.*

#-----------------------------------------------------------------------------

%package gb-image
Summary: The Gambas image manipulation component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-image
This component allows you to apply various effects to images.

%files gb-image
%defattr(-,root,root)
%{_libdir}/%{name}/gb.image.*
%{_datadir}/%{name}/info/gb.image.*

#-----------------------------------------------------------------------------

%package gb-info
Summary: The Gambas system information component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-info
This component provides a lot of information about the system where
the application is executed.

%files gb-info
%defattr(-,root,root)
%{_libdir}/%{name}/gb.info.*
%{_datadir}/%{name}/info/gb.info.*

#-----------------------------------------------------------------------------

#%package gb-ldap
#Summary: The Gambas LDAP component
#Group: Development/Other
#Requires: %{name}-runtime = %{version}

#%description gb-ldap
#This component provides access to LDAP servers.

#%files gb-ldap
#%defattr(-,root,root)
#%{_libdir}/%{name}/gb.ldap.*
#%{_datadir}/%{name}/info/gb.ldap.*

#-----------------------------------------------------------------------------

%package gb-net
Summary: The Gambas networking component
Group: Development/Other
Requires: %{name}-runtime = %{version}
Obsoletes: gambas-gb-net < 2.0.0

%description gb-net
This component allows you to use TCP/IP and UDP sockets, and to access
any serial ports.

%files gb-net
%defattr(-,root,root)
%{_libdir}/%{name}/gb.net.la
%{_libdir}/%{name}/gb.net.so*
%{_libdir}/%{name}/gb.net.component
%{_datadir}/%{name}/info/gb.net.info
%{_datadir}/%{name}/info/gb.net.list

#-----------------------------------------------------------------------------

%package gb-net-curl
Summary: The Gambas advanced networking component
Group: Development/Other
Requires: %{name}-runtime = %{version},%{name}-gb-net = %{version}
Obsoletes: gambas-gb-net-curl < 2.0.0

%description gb-net-curl
This component allows your programs to easily become FTP or HTTP clients.

%files gb-net-curl
%defattr(-,root,root)
%{_libdir}/%{name}/gb.net.curl.la
%{_libdir}/%{name}/gb.net.curl.so*
%{_libdir}/%{name}/gb.net.curl.component
%{_datadir}/%{name}/info/gb.net.curl.info
%{_datadir}/%{name}/info/gb.net.curl.list

#-----------------------------------------------------------------------------

%package gb-net-smtp
Summary: The Gambas SMTP component
Group: Development/Other
Requires: %{name}-runtime = %{version},%{name}-gb-net = %{version}

%description gb-net-smtp
This component allows you to send emails using the SMTP protocol.

%files gb-net-smtp
%defattr(-,root,root)
%{_libdir}/%{name}/gb.net.smtp.*
%{_datadir}/%{name}/info/gb.net.smtp.*

#-----------------------------------------------------------------------------

%package gb-opengl
Summary: The Gambas OpenGL component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-opengl
This component allows you to use the Mesa libraries to do 3D operations.

%files gb-opengl
%defattr(-,root,root)
%{_libdir}/%{name}/gb.opengl.*
%{_datadir}/%{name}/info/gb.opengl.*

#-----------------------------------------------------------------------------

%package gb-option
Summary: The Gambas command-line option component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-option
This component allows you to interpret command-line options.

%files gb-option
%defattr(-,root,root)
%{_libdir}/%{name}/gb.option.*
%{_datadir}/%{name}/info/gb.option.*

#-----------------------------------------------------------------------------

%package gb-pcre
Summary: The Gambas PCRE component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-pcre
This component allows you to use Perl compatible regular expresions
within Gambas code.

%files gb-pcre
%defattr(-,root,root)
%{_libdir}/%{name}/gb.pcre.*
%{_datadir}/%{name}/info/gb.pcre.*

#-----------------------------------------------------------------------------

%package gb-pdf
Summary: The Gambas PDF component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-pdf
This component allows you to manipulate pdf files with Gambas code.

%files gb-pdf
%defattr(-,root,root)
%{_libdir}/%{name}/gb.pdf.*
%{_datadir}/%{name}/info/gb.pdf.*

#-----------------------------------------------------------------------------

%package gb-qt
Summary: The Gambas Qt GUI component
Group: Development/Other
Requires: %{name}-runtime = %{version}
Obsoletes: gambas-gb-qt < 2.0.0
Obsoletes: gambas-gb-qt-editor < 2.0.0

%description gb-qt
This package includes the Gambas QT GUI component.

%files gb-qt
%defattr(-,root,root)
%{_libdir}/%{name}/gb.qt.la
%{_libdir}/%{name}/gb.qt.so*
%{_libdir}/%{name}/gb.qt.component
%{_libdir}/%{name}/gb.qt.gambas
%{_datadir}/%{name}/info/gb.qt.info
%{_datadir}/%{name}/info/gb.qt.list

#-----------------------------------------------------------------------------

%package gb-qt-ext
Summary: The Gambas extended Qt GUI component
Group: Development/Other
Requires: %{name}-runtime = %{version},%{name}-gb-qt = %{version}
Obsoletes: gambas-gb-qt-ext < 2.0.0

%description gb-qt-ext
This component includes somme uncommon QT controls.

%files gb-qt-ext
%defattr(-,root,root)
%{_libdir}/%{name}/gb.qt.ext.la
%{_libdir}/%{name}/gb.qt.ext.so*
%{_libdir}/%{name}/gb.qt.ext.component
%{_datadir}/%{name}/info/gb.qt.ext.info
%{_datadir}/%{name}/info/gb.qt.ext.list

#-----------------------------------------------------------------------------

%if %mdkversion < 201000
%package gb-qt-kde
Summary: The Gambas KDE component
Group: Development/Other
Requires: %{name}-runtime = %{version},%{name}-gb-qt = %{version}
Obsoletes: gambas-gb-qt-kde < 2.0.0

%description gb-qt-kde
This component transforms your QT application in a KDE application, and
allows you to pilot any other KDE application with the DCOP protocol.

%files gb-qt-kde
%defattr(-,root,root)
%{_libdir}/%{name}/gb.qt.kde.la
%{_libdir}/%{name}/gb.qt.kde.so*
%{_libdir}/%{name}/gb.qt.kde.component
%{_datadir}/%{name}/info/gb.qt.kde.info
%{_datadir}/%{name}/info/gb.qt.kde.list

#-----------------------------------------------------------------------------

%package gb-qt-kde-html
Summary: The Gambas KHTML component
Group: Development/Other
Requires: %{name}-runtime = %{version},%{name}-gb-qt-kde = %{version}
Obsoletes: gambas-gb-qt-kde-html < 2.0.0

%description gb-qt-kde-html
This component allows you to use the KHTML Web Browser widget included in KDE

%files gb-qt-kde-html
%defattr(-,root,root)
%{_libdir}/%{name}/gb.qt.kde.html.la
%{_libdir}/%{name}/gb.qt.kde.html.so*
%{_libdir}/%{name}/gb.qt.kde.html.component
%{_datadir}/%{name}/info/gb.qt.kde.html.info
%{_datadir}/%{name}/info/gb.qt.kde.html.list

%endif

#-----------------------------------------------------------------------------

%package gb-qt-opengl
Summary: The Gambas QT OpenGL component
Group: Development/Other
Requires: %{name}-runtime = %{version},%{name}-gb-qt = %{version}

%description gb-qt-opengl
This component allows you integrate OpenGL in qt applications.

%files gb-qt-opengl
%defattr(-,root,root)
%{_libdir}/%{name}/gb.qt.opengl.la
%{_libdir}/%{name}/gb.qt.opengl.so*
%{_libdir}/%{name}/gb.qt.opengl.component
%{_datadir}/%{name}/info/gb.qt.opengl.info
%{_datadir}/%{name}/info/gb.qt.opengl.list

#-----------------------------------------------------------------------------

%package gb-report
Summary: The Gambas report component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-report
This component is for designing reports.

%files gb-report
%defattr(-,root,root)
%{_libdir}/%{name}/gb.report.*
%{_datadir}/%{name}/info/gb.report.*

#-----------------------------------------------------------------------------

%package gb-sdl
Summary: The Gambas SDL component
Group: Development/Other
Requires: %{name}-runtime = %{version}
Obsoletes: gambas-gb-sdl < 2.0.0

%description gb-sdl
This component use the sound, image and TTF fonts parts of the SDL
library. It allows you to simultaneously play many sounds and music
stored in a file. If OpenGL drivers are installed it uses them to 
accelerate 2D and 3D drawing.

%files gb-sdl
%defattr(-,root,root)
%{_libdir}/%{name}/gb.sdl.la
%{_libdir}/%{name}/gb.sdl.so
%{_libdir}/%{name}/gb.sdl.so.*
%{_libdir}/%{name}/gb.sdl.component
%{_datadir}/%{name}/info/gb.sdl.info
%{_datadir}/%{name}/info/gb.sdl.list

#-----------------------------------------------------------------------------

%package gb-sdl-sound
Summary: The Gambas SDL sound component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-sdl-sound
This component allows you to play sounds in Gambas. This component 
manages up to 32 sound tracks that can play sounds from memory, and
one music track that can play music from a file. Everything is mixed
in real time. 

%files gb-sdl-sound
%defattr(-,root,root)
%{_libdir}/%{name}/gb.sdl.sound.*
%{_datadir}/%{name}/info/gb.sdl.sound.*

#-----------------------------------------------------------------------------

%package gb-settings
Summary: The Gambas settings component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-settings
This components allows you to deal with configuration files.

%files gb-settings
%defattr(-,root,root)
%{_libdir}/%{name}/gb.settings.*
%{_datadir}/%{name}/info/gb.settings.*

#-----------------------------------------------------------------------------

%package gb-v4l
Summary: The Gambas Video4Linux component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-v4l
This components allows you to use the Video4Linux interface with
Gambas.

%files gb-v4l
%defattr(-,root,root)
%{_libdir}/%{name}/gb.v4l.*
%{_datadir}/%{name}/info/gb.v4l.*

#-----------------------------------------------------------------------------

%package gb-vb
Summary: The Gambas Visual Basic(tm) compatibility component
Group: Development/Other
Requires: %{name}-runtime = %{version}
Obsoletes: gambas-gb-vb < 2.0.0

%description gb-vb
This component aims at including some functions that imitate the 
behaviour of Visual Basic(TM) functions. Use it only if you want to 
port some VB projects.

%files gb-vb
%defattr(-,root,root)
%{_libdir}/%{name}/gb.vb.la
%{_libdir}/%{name}/gb.vb.so*
%{_libdir}/%{name}/gb.vb.component
%{_datadir}/%{name}/info/gb.vb.info
%{_datadir}/%{name}/info/gb.vb.list

#-----------------------------------------------------------------------------

%package gb-web
Summary: The Gambas CGI component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-web
This components allows you to make CGI web applications using Gambas, 
with an ASP-like interface.

%files gb-web
%defattr(-,root,root)
%{_libdir}/%{name}/gb.web.*
%{_datadir}/%{name}/info/gb.web.*

#-----------------------------------------------------------------------------

%package gb-xml
Summary: The Gambas xml component
Group: Development/Other
Requires: %{name}-runtime = %{version}
Obsoletes: gambas-gb-xml < 2.0.0

%description gb-xml
This component allows you to use xml.

%files gb-xml
%defattr(-,root,root)
%{_libdir}/%{name}/gb.xml.la
%{_libdir}/%{name}/gb.xml.so*
%{_libdir}/%{name}/gb.xml.component
%{_datadir}/%{name}/info/gb.xml.info
%{_datadir}/%{name}/info/gb.xml.list

#-----------------------------------------------------------------------------

%package gb-xml-rpc
Summary: The Gambas xml-rpc component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-xml-rpc
This component allows you to use xml-rpc.

%files gb-xml-rpc
%defattr(-,root,root)
%{_libdir}/%{name}/gb.xml.rpc*
%{_datadir}/%{name}/info/gb.xml.rpc*

#-----------------------------------------------------------------------------

%package gb-xml-xslt
Summary: The Gambas xml-rpc component
Group: Development/Other
Requires: %{name}-runtime = %{version}

%description gb-xml-xslt
This component allows you to use xml-xslt.

%files gb-xml-xslt
%defattr(-,root,root)
%{_libdir}/%{name}/gb.xml.xslt*
%{_datadir}/%{name}/info/gb.xml.xslt*

#-----------------------------------------------------------------------------

%clean
rm -rf $RPM_BUILD_ROOT


