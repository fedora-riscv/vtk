# Disable OSMesa builds for now - see Bug 744434
%bcond_with OSMesa
# Make Java conditional
%bcond_without java

%{!?tcl_version: %global tcl_version %(echo 'puts $tcl_version' | tclsh)}
%{!?tcl_sitelib: %global tcl_sitelib %{_datadir}/tcl%{tcl_version}}

Summary: The Visualization Toolkit - A high level 3D visualization library
Name: vtk
Version: 6.1.0
Release: 20%{?dist}
# This is a variant BSD license, a cross between BSD and ZLIB.
# For all intents, it has the same rights and restrictions as BSD.
# http://fedoraproject.org/wiki/Licensing/BSD#VTKBSDVariant
License: BSD
Group: System Environment/Libraries
Source: http://www.vtk.org/files/release/6.1/VTK-%{version}.tar.gz
# Use system libraries
# http://public.kitware.com/Bug/view.php?id=11823
Patch0: vtk-6.1.0-system.patch
# Install some more needed cmake files to try to support paraview build
# http://www.vtk.org/Bug/view.php?id=14157
Patch1: vtk-install.patch
# Patch to vtk to use system netcdf library
Patch2: vtk-6.1.0-netcdf.patch
# Fix compilation with mesa 10.4
# https://bugzilla.redhat.com/show_bug.cgi?id=1138466
Patch3: vtk-glext.patch
# Fix types for std::min/man
# http://www.vtk.org/Bug/view.php?id=15249
Patch4: vtk-type.patch

URL: http://vtk.org/

BuildRequires: cmake
BuildRequires: gcc-c++
#%{?with_java:BuildRequires: gcc-java, libgcj-devel, java-devel}
%{?with_java:BuildRequires: java-devel}
BuildRequires: libX11-devel, libXt-devel, libXext-devel
BuildRequires: libICE-devel, libGL-devel
%{?with_OSMesa:BuildRequires: mesa-libOSMesa-devel}
BuildRequires: tk-devel, tcl-devel
BuildRequires: python-devel
BuildRequires: expat-devel, freetype-devel, libjpeg-devel, libpng-devel
BuildRequires: gl2ps-devel
BuildRequires: libtiff-devel, zlib-devel
BuildRequires: libxml2-devel
BuildRequires: qt4-devel
BuildRequires: qtwebkit-devel
BuildRequires: chrpath
BuildRequires: doxygen, graphviz
BuildRequires: gnuplot
BuildRequires: boost-devel
BuildRequires: hdf5-devel
BuildRequires: jsoncpp-devel
BuildRequires: libtheora-devel
BuildRequires: mysql-devel
BuildRequires: netcdf-cxx-devel
BuildRequires: postgresql-devel
BuildRequires: R-devel
BuildRequires: PyQt4-devel
BuildRequires: sip-devel
BuildRequires: sqlite-devel
BuildRequires: wget
BuildRequires: %{_includedir}/Xm
BuildRequires: blas-devel
BuildRequires: lapack-devel
%{!?with_java:Conflicts: vtk-java}
Requires: hdf5 = %{_hdf5_version}

# Do not check .so files in the python_sitearch directory
%global __provides_exclude_from ^%{python_sitearch}/.*\\.so$

%description
VTK is an open-source software system for image processing, 3D
graphics, volume rendering and visualization. VTK includes many
advanced algorithms (e.g., surface reconstruction, implicit modeling,
decimation) and rendering techniques (e.g., hardware-accelerated
volume rendering, LOD control).

%package devel
Summary: VTK header files for building C++ code
Requires: vtk%{?_isa} = %{version}-%{release}
%{?with_OSMesa:Requires: mesa-libOSMesa-devel%{?_isa}}
Requires: cmake
Requires: blas-devel%{?_isa}
Requires: gl2ps-devel%{?_isa}
Requires: expat-devel%{?_isa}
Requires: freetype-devel%{?_isa}
Requires: hdf5-devel%{?_isa}
Requires: lapack-devel%{?_isa}
Requires: libjpeg-devel%{?_isa}
Requires: libpng-devel%{?_isa}
Requires: libogg-devel%{?_isa}
Requires: libtheora-devel%{?_isa}
Requires: libtiff-devel%{?_isa}
Requires: libxml2-devel%{?_isa}
Requires: postgresql-devel%{?_isa}
Requires: mysql-devel%{?_isa}
Requires: qt4-devel%{?_isa}
Requires: qtwebkit-devel%{?_isa}
Requires: jsoncpp-devel%{?_isa}
Requires: python2-devel%{?_isa}
Group: Development/Libraries

%description devel 
This provides the VTK header files required to compile C++ programs that
use VTK to do 3D visualization.

%package tcl
Summary: Tcl bindings for VTK
Requires: vtk%{?_isa} = %{version}-%{release}
Group: System Environment/Libraries

%description tcl
tcl bindings for VTK

%package python
Summary: Python bindings for VTK
Requires: vtk%{?_isa} = %{version}-%{release}
Group: System Environment/Libraries

%description python
python bindings for VTK

%if %{with java}
%package java
Summary: Java bindings for VTK
Requires: vtk%{?_isa} = %{version}-%{release}
Group: System Environment/Libraries

%description java
Java bindings for VTK
%endif

%package qt
Summary: Qt bindings for VTK
Requires: vtk%{?_isa} = %{version}-%{release}
Group: System Environment/Libraries

%description qt
Qt bindings for VTK

%package qt-python
Summary: Qt Python bindings for VTK
Requires: vtk%{?_isa} = %{version}-%{release}
Group: System Environment/Libraries

%description qt-python
Qt Python bindings for VTK

%package qt-tcl
Summary: Qt TCL bindings for VTK
Requires: vtk%{?_isa} = %{version}-%{release}
Group: System Environment/Libraries

%description qt-tcl
Qt TCL bindings for VTK

%package testing
Summary: Testing programs for VTK
Requires: vtk%{?_isa} = %{version}-%{release}, vtkdata = %{version}
Group: Applications/Engineering

%description testing
Testing programs for VTK

%package examples
Summary: Examples for VTK
Requires: vtk%{?_isa} = %{version}-%{release}, vtkdata = %{version}
Group: Applications/Engineering

%description examples
This package contains many well-commented examples showing how to use
VTK. Examples are available in the C++, Tcl, Python and Java
programming languages.


%prep
%setup -q -n VTK-%{version}
%patch0 -p1 -b .system
%patch1 -p1 -b .install
%patch2 -p1 -b .netcdf
%patch3 -p1 -b .glext
%patch4 -p1 -b .type
# Remove included thirdparty sources just to be sure
# TODO - vtksqlite
for x in autobahn vtkexpat vtkfreetype vtkgl2ps vtkhdf5 vtkjpeg vtklibxml2 vtknetcdf vtkoggtheora vtkpng vtktiff twisted vtkzlib zope
do
  rm -r ThirdParty/*/${x}
done

# Replace relative path ../../../VTKData with %{_datadir}/vtkdata-%{version}
# otherwise it will break on symlinks.
grep -rl '\.\./\.\./\.\./\.\./VTKData' . | xargs \
  perl -pi -e's,\.\./\.\./\.\./\.\./VTKData,%{_datadir}/vtkdata-%{version},g'

# Save an unbuilt copy of the Example's sources for %doc
mkdir vtk-examples
cp -a Examples vtk-examples
# Don't ship Win32 examples
rm -r vtk-examples/Examples/GUI/Win32
find vtk-examples -type f | xargs chmod -R a-x

%build
export CFLAGS="%{optflags} -D_UNICODE"
export CXXFLAGS="%{optflags} -D_UNICODE"
%if %{with java}
export JAVA_HOME=/usr/lib/jvm/java
# Arm/Aarch64 builders have less ram
# https://bugzilla.redhat.com/show_bug.cgi?id=1115920
%ifnarch s390
export JAVA_TOOL_OPTIONS=-Xmx2048m
%endif
%endif

mkdir build
pushd build
%{cmake} .. \
 -DBUILD_DOCUMENTATION:BOOL=ON \
 -DBUILD_EXAMPLES:BOOL=ON \
 -DBUILD_TESTING:BOOL=OFF \
 -DVTK_CUSTOM_LIBRARY_SUFFIX="" \
 -DVTK_INSTALL_ARCHIVE_DIR:PATH=%{_lib}/vtk \
 -DVTK_INSTALL_DATA_DIR=share/vtk \
 -DVTK_INSTALL_INCLUDE_DIR:PATH=include/vtk \
 -DVTK_INSTALL_LIBRARY_DIR:PATH=%{_lib}/vtk \
 -DVTK_INSTALL_PACKAGE_DIR:PATH=%{_lib}/cmake/vtk \
 -DVTK_INSTALL_PYTHON_MODULE_DIR:PATH=%{_lib}/python%{python_version}/site-packages \
 -DVTK_INSTALL_QT_DIR:PATH=/%{_lib}/qt4/plugins/designer \
 -DVTK_INSTALL_TCL_DIR:PATH=share/tcl%{tcl_version}/vtk \
 -DTK_INTERNAL_PATH:PATH=/usr/include/tk-private/generic \
%if %{with OSMesa}
 -DVTK_OPENGL_HAS_OSMESA:BOOL=ON \
%endif
%if %{with java}
 -DVTK_WRAP_JAVA:BOOL=ON \
 -DJAVA_INCLUDE_PATH:PATH=$JAVA_HOME/include \
 -DJAVA_INCLUDE_PATH2:PATH=$JAVA_HOME/include/linux \
 -DJAVA_AWT_INCLUDE_PATH:PATH=$JAVA_HOME/include \
%else
 -DVTK_WRAP_JAVA:BOOL=OFF \
%endif
 -DVTK_WRAP_PYTHON:BOOL=ON \
 -DVTK_WRAP_PYTHON_SIP:BOOL=ON \
 -DSIP_INCLUDE_DIR:PATH=/usr/include/python%{python_version} \
 -DVTK_WRAP_TCL:BOOL=ON \
 -DVTK_Group_Imaging:BOOL=ON \
 -DVTK_Group_Qt:BOOL=ON \
 -DVTK_Group_Rendering:BOOL=ON \
 -DVTK_Group_StandAlone:BOOL=ON \
 -DVTK_Group_Tk:BOOL=ON \
 -DVTK_Group_Views:BOOL=ON \
 -DModule_vtkFiltersStatisticsGnuR:BOOL=ON \
 -DModule_vtkTestingCore:BOOL=ON \
 -DModule_vtkTestingRendering:BOOL=ON \
 -DVTK_USE_OGGTHEORA_ENCODER=ON \
 -DVTK_USE_SYSTEM_LIBRARIES=ON \
 -DVTK_USE_SYSTEM_HDF5:BOOL=ON \
 -DVTK_USE_SYSTEM_LIBPROJ4:BOOL=OFF \
 -DVTK_USE_SYSTEM_NETCDF:BOOL=ON

# TODO - MPI
#-DVTK_Group_MPI:BOOL=ON \
# Needed for some tests.  Fails to compile at the moment.  We don't run test though.
#  -DVTK_DATA_ROOT:PATH=%{_datadir}/vtkdata-%{version} \
# Not working, see http://public.kitware.com/Bug/view.php?id=11978
# -DVTK_USE_ODBC=ON \
# Commented old flags in case we'd like to reactive some of them
# -DVTK_USE_DISPLAY:BOOL=OFF \ # This prevents building of graphics tests
# -DVTK_USE_MPI:BOOL=ON \

# Got intermittent build error with -j
make %{?_smp_mflags}

# Remove executable bits from sources (some of which are generated)
find . -name \*.c -or -name \*.cxx -or -name \*.h -or -name \*.hxx -or \
       -name \*.gif | xargs chmod -x

%install
mkdir -p %{buildroot}
pushd build
make install DESTDIR=%{buildroot}

# ld config
mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d
echo %{_libdir}/vtk > %{buildroot}%{_sysconfdir}/ld.so.conf.d/vtk-%{_arch}.conf

# Gather list of non-python/tcl libraries
ls %{buildroot}%{_libdir}/vtk/*.so.* \
  | grep -Ev '(Java|Qt|Python27D|TCL)' | sed -e's,^%{buildroot},,' > libs.list

# List of executable utilities
cat > utils.list << EOF
vtkEncodeString
EOF

# List of executable examples
cat > examples.list << EOF
HierarchicalBoxPipeline
MultiBlock
Arrays
Cube
RGrid
SGrid
Medical1
Medical2
Medical3
finance
AmbientSpheres
Cylinder
DiffuseSpheres
SpecularSpheres
Cone
Cone2
Cone3
Cone4
Cone5
Cone6
EOF

# Install examples too
for filelist in examples.list; do
  for file in `cat $filelist`; do
    install -p bin/$file %{buildroot}%{_bindir}
  done
done

# Fix up filelist paths
for filelist in utils.list examples.list; do
  perl -pi -e's,^,%{_bindir}/,' $filelist
done

# Remove any remnants of rpaths on files we install
# Seems to be some kind of java path
for file in `cat examples.list`; do
  chrpath -d %{buildroot}$file
done
chrpath -d  %{buildroot}%{_libdir}/qt4/plugins/designer/libQVTKWidgetPlugin.so

# Main package contains utils and core libs
cat libs.list utils.list > main.list
popd

# Make scripts executable
#chmod a+x %{buildroot}%{_libdir}/vtk/doxygen/*.pl
#chmod a+x %{buildroot}%{_libdir}/vtk/testing/*.{py,tcl}

# Remove exec bit from non-scripts and %%doc
for file in `find %{buildroot} -type f -perm 0755 \
  | xargs -r file | grep ASCII | awk -F: '{print $1}'`; do
  head -1 $file | grep '^#!' > /dev/null && continue
  chmod 0644 $file
done
find Utilities/Upgrading -type f | xargs chmod -x

# Setup Wrapping docs tree
mkdir _docs
cp -pr --parents Wrapping/*/README* _docs/ 


%check
#LD_LIBARARY_PATH=`pwd`/bin ctest -V


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post tcl -p /sbin/ldconfig

%postun tcl -p /sbin/ldconfig

%post python -p /sbin/ldconfig

%postun python -p /sbin/ldconfig

%if %{with java}
%post java -p /sbin/ldconfig

%postun java -p /sbin/ldconfig
%endif

%post qt -p /sbin/ldconfig

%postun qt -p /sbin/ldconfig

%post qt-python -p /sbin/ldconfig

%postun qt-python -p /sbin/ldconfig

%post qt-tcl -p /sbin/ldconfig

%postun qt-tcl -p /sbin/ldconfig

%files -f build/main.list
%doc Copyright.txt README.html vtkLogo.jpg vtkBanner.gif _docs/Wrapping
%config(noreplace) %{_sysconfdir}/ld.so.conf.d/vtk-%{_arch}.conf
%{_datadir}/vtk
%dir %{_libdir}/vtk

%files devel
%doc Utilities/Upgrading
%{_bindir}/vtkHashSource
%{_bindir}/vtkWrapHierarchy
%{_includedir}/vtk
%{_libdir}/vtk/*.so
%{_libdir}/vtk/libvtkWrappingTools.a
%{_libdir}/cmake/vtk/
%{_bindir}/vtkParseOGLExt
%{_docdir}/vtk-6.1/
%{tcl_sitelib}/vtk/vtktcl.c

%files tcl
%{_libdir}/vtk/*TCL.so.*
%exclude %{_libdir}/vtk/*QtTCL.so.*
%{_bindir}/vtk
%{_bindir}/vtkWrapTcl
%{_bindir}/vtkWrapTclInit
%{tcl_sitelib}/vtk/
%exclude %{tcl_sitelib}/vtk/vtktcl.c

%files python
%{python_sitearch}/*
%{_libdir}/vtk/*Python27D.so.*
%exclude %{_libdir}/vtk/*QtPython27D.so.*
%{_bindir}/vtkpython
%{_bindir}/vtkWrapPython
%{_bindir}/vtkWrapPythonInit

%if %{with java}
%files java
%{_libdir}/vtk/*Java.so.*
%{_libdir}/vtk/vtk.jar
%{_bindir}/vtkParseJava
%{_bindir}/vtkWrapJava
%endif

%files qt
%{_libdir}/vtk/lib*Qt*.so.*
%exclude %{_libdir}/vtk/*TCL.so.*
%exclude %{_libdir}/vtk/*Python27D.so.*
%{_libdir}/qt4/plugins/designer/libQVTKWidgetPlugin.so

%files qt-python
%{_libdir}/vtk/*QtPython27D.so.*

%files qt-tcl
%{_libdir}/vtk/*QtTCL.so.*

%files testing

%files examples -f build/examples.list
%doc vtk-examples/Examples

%changelog
* Sat Jan 17 2015 François Cami <fcami@fedoraproject.org> - 6.1.0-20
- Add jsoncpp-devel and python2-devel to vtk-devel Requires (bug #1183210)

* Thu Jan 08 2015 Orion Poplawski <orion@cora.nwra.com> - 6.1.0-19
- Rebuild for hdf5 1.8.14
- Add patch to fix compilation error

* Thu Nov 20 2014 Dan Horák <dan[at]danny.cz> - 6.1.0-18
- Don't override Java memory settings on s390 (related to bug #1115920)

* Wed Nov 19 2014 Orion Poplawski <orion@cora.nwra.com> - 6.1.0-17
- Add patch to fix compilation with mesa 10.4 (bug #1138466)

* Fri Oct 31 2014 Orion Poplawski <orion@cora.nwra.com> - 6.1.0-16
- No longer need cmake28 on RHEL6

* Thu Sep 4 2014 Orion Poplawski <orion@cora.nwra.com> - 6.1.0-15
- Increase java heap space for builds (bug #1115920)

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.1.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jun 10 2014 Orion Poplawski <orion@cora.nwra.com> - 6.1.0-13
- Rebuild for hdf 1.8.13

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.1.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jun 5 2014 Orion Poplawski <orion@cora.nwra.com> - 6.1.0-11
- Add requires on blas-devel and lapack-devel to vtk-devel (bug #1105004)

* Tue May 27 2014 Orion Poplawski <orion@cora.nwra.com> - 6.1.0-10
- Rebuild for Tcl 8.6

* Fri May 23 2014 Petr Machata <pmachata@redhat.com> - 6.1.0-9
- Rebuild for boost 1.55.0

* Wed May 21 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 6.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Changes/f21tcl86

* Tue May  6 2014 Tom Callaway <spot@fedoraproject.org> - 6.1.0-7
- rebuild against R 3.1.0 (without bundled blas/lapack)

* Wed Mar 26 2014 Orion Poplawski <orion@cora.nwra.com> - 6.1.0-5
- Add Requires: qtwebkit-devel and hdf5-devel to vtk-devel (bug #1080781)

* Tue Jan 28 2014 Orion Poplawski <orion@cora.nwra.com> - 6.1.0-4
- Really fix requires freetype-devel

* Mon Jan 27 2014 Orion Poplawski <orion@cora.nwra.com> - 6.1.0-3
- Fix requires freetype-devel

* Sun Jan 26 2014 Orion Poplawski <orion@cora.nwra.com> - 6.1.0-2
- Add Requires: libfreetype-devel; libxml2-devel to vtk-devel (bug #1057924)

* Thu Jan 23 2014 Orion Poplawski <orion@cora.nwra.com> - 6.1.0-1
- Update to 6.1.0
- Rebase patches, drop vtkpython patch
- Disable BUILD_TESTING for now until we can provide test data

* Fri Dec 27 2013 Orion Poplawski <orion@cora.nwra.com> - 6.0.0-10
- Add patch to use system netcdf

* Sun Dec 22 2013 Kevin Fenzi <kevin@scrye.com> 6.0.0-9
- Add BuildRequires on blas-devel and lapack-devel

* Sun Dec 22 2013 François Cami <fcami@fedoraproject.org> - 6.0.0-8
* Rebuild for rawhide.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 30 2013 Petr Machata <pmachata@redhat.com> - 6.0.0-6
- Rebuild for boost 1.54.0

* Mon Jul 29 2013 Orion Poplawski <orion@cora.nwra.com> - 6.0.0-5
- Enable VTK_WRAP_PYTHON_SIP

* Fri Jul 26 2013 Orion Poplawski <orion@cora.nwra.com> - 6.0.0-4
- Add patch to install vtkpython

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 6.0.0-3
- Perl 5.18 rebuild

* Mon Jul 15 2013 Orion Poplawski <orion@cora.nwra.com> - 6.0.0-2
- Install vtkMakeInstantiator files for gdcm build

* Fri Jul 12 2013 Orion Poplawski <orion@cora.nwra.com> - 6.0.0-1
- Add BR on R-devel

* Thu Jun 27 2013 Orion Poplawski <orion@cora.nwra.com> - 6.0.0-1
- Update to 6.0.0

* Thu May 16 2013 Orion Poplawski <orion@cora.nwra.com> - 5.10.1-5
- Rebuild for hdf5 1.8.11

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.10.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 21 2013 Adam Tkac <atkac redhat com> - 5.10.1-3
- rebuild due to "jpeg8-ABI" feature drop

* Mon Dec 03 2012 Orion Poplawski <orion@cora.nwra.com> - 5.10.1-2
- Rebuild for hdf5 1.8.10
- Change doc handling

* Thu Nov 1 2012 Orion Poplawski <orion@cora.nwra.com> - 5.10.1-1
- Update to 5.10.1

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu May 24 2012 Orion Poplawski <orion@cora.nwra.com> - 5.10.0-2
- Add patch to add soname to libvtkNetCDF_cxx

* Tue May 15 2012 Orion Poplawski <orion@cora.nwra.com> - 5.10.0-1
- Update to 5.10.0

* Tue May 15 2012 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 5.8.0-6
- Add cmake28 usage when building for EL6
- Disable -java build on PPC64 as it fails to build

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.8.0-5
- Rebuilt for c++ ABI breakage

* Sun Jan 8 2012 Orion Poplawski <orion@cora.nwra.com> - 5.8.0-4
- Rebuild with gcc 4.7

* Fri Nov 18 2011 Orion Poplawski <orion@cora.nwra.com> - 5.8.0-3
- Rebuild for hdf5 1.8.8, add explicit requires

* Tue Nov 1 2011 Orion Poplawski <orion@cora.nwra.com> - 5.8.0-2
- Keep libraries in %%{_libdir}/vtk, use ld.so.conf.d

* Fri Oct 7 2011 Orion Poplawski <orion@cora.nwra.com> - 5.8.0-1
- Update to 5.8.0
- Drop version from directory names
- Use VTK_PYTHON_SETUP_ARGS instead of patch to set python install dir
- Drop several patches fixed upstream
- Remove rpaths from all hand installed binaries (Bug 744437)
- Don't link against OSMesa (Bug 744434)

* Thu Jun 23 2011 Orion Poplawski <orion@cora.nwra.com> - 5.6.1-10
- Add BR qtwebkit-devel, fixes FTBS bug 715770

* Thu May 19 2011 Orion Poplawski <orion@cora.nwra.com> - 5.6.1-9
- Update soversion patch to add soversion to libvtkNetCDF.so

* Mon Mar 28 2011 Orion Poplawski <orion@cora.nwra.com> - 5.6.1-8
- Rebuild for new mysql

* Thu Mar 17 2011 Orion Poplawski <orion@cora.nwra.com> - 5.6.1-7
- Add needed requires to vtk-devel

* Wed Mar 16 2011 Orion Poplawski <orion@cora.nwra.com> - 5.6.1-6
- Turn on boost, mysql, postgres, ogg theora, and text analysis support,
  bug 688275.

* Wed Mar 16 2011 Marek Kasik <mkasik@redhat.com> - 5.6.1-5
- Add backslashes to VTK_INSTALL_LIB_DIR and
- VTK_INSTALL_INCLUDE_DIR (#687895)

* Tue Mar 15 2011 Orion Poplawski <orion@cora.nwra.com> - 5.6.1-4
- Set VTK_INSTALL_LIB_DIR, fix bug 687895

* Fri Feb 18 2011 Orion Poplawski <orion@cora.nwra.com> - 5.6.1-3
- Add patch to support gcc 4.6
- Add patch to make using system libraries easier
- Update pythondestdir patch to use --prefix and --root
- Use system gl2ps and libxml2
- Use standard cmake build macro, out of tree builds
- Add patch from upstream to add sonames to libCosmo and libVPIC (bug #622840)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 7 2010 Orion Poplawski <orion@cora.nwra.com> - 5.6.1-1
- Update to 5.6.1
- Enable qt4 support, drop qt3 support

* Wed Oct 20 2010 Adam Jackson <ajax@redhat.com> 5.6.0-37
- Rebuild for new libOSMesa soname

* Sat Jul 31 2010 David Malcolm <dmalcolm@redhat.com> - 5.6.0-36
- add python 2.7 compat patch

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 5.6.0-35
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Jul  5 2010 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.6.0-34
- Update to 5.6.0.

* Sat Jun  6 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.4.2-30
- Update to 5.4.2.

* Thu Mar 12 2009 Orion Poplawski <orion@cora.nwra.com> - 5.2.1-29
- Update to 5.2.1

* Fri Mar 06 2009 Jesse Keating <jkeating@redhat.com> - 5.2.0-28
- Remove chmod on examples .so files, none are built.  This needs
  more attention.

* Sun Oct  5 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.2.0-26
- Update to 5.2.0.

* Wed Oct 1 2008 Orion Poplawski <orion@cora.nwra.com> - 5.0.2-25
- Fix patch fuzz

* Mon Aug 25 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.0.4-24
- Change java build dependencies from java-devel to gcj.

* Sun Aug 24 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.0.4-23
- %%check || : does not work anymore.
- enable java by default.

* Wed May 21 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 5.0.4-22
- fix license tag

* Sat Apr 12 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.0.4-21
- Fixes for gcc 4.3 by Orion Poplawski.

* Sat Apr  5 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.0.4-20
- Change BR to qt-devel to qt3-devel.

* Sat Feb 23 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.0.4-19
- Update to 5.0.4.

* Mon May 28 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.0.3-18
- Move headers to %%{_includedir}/vtk.
- Remove executable bit from sources.

* Mon Apr 16 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.0.3-17
- Make java build conditional.
- Add ldconfig %%post/%%postun for java/qt subpackages.

* Sun Apr 15 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.0.3-16
- Remove %%ghosting pyc/pyo.

* Wed Apr 04 2007 Paulo Roma <roma@lcg.ufrj.br> - 5.0.3-15
- Update to 5.0.4.
- Added support for qt4 plugin.

* Wed Feb  7 2007 Orion Poplawski <orion@cora.nwra.com> - 5.0.2-14
- Enable Java, Qt, GL2PS, OSMESA

* Mon Sep 11 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.0.2-13
- Update to 5.0.2.

* Sun Aug  6 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.0.1-12
- cmake needs to be >= 2.0.4.

* Fri Aug  4 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.0.1-11
- Fix some python issues including pyo management.

* Sun Jul 23 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.0.1-10
- Embed feedback from bug 199405 comment 5.
- Fix some Group entries.
- Remove redundant dependencies.
- Use system libs.
- Comment specfile more.
- Change buildroot handling with CMAKE_INSTALL_PREFIX.
- Enable qt designer plugin.

* Wed Jul 19 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.0.1-7
- Fix some permissions for rpmlint and debuginfo.

* Sun Jul 16 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.0.1-7
- Remove rpath and some further rpmlint warnings.

* Thu Jul 13 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.0.1-6
- Update to 5.0.1.

* Wed May 31 2006 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 5.0.

* Mon Apr 05 2004 Intrinsic Spin <spin@freakbait.com> 2.mr
- built on a machine with a stock libGL.so

* Sun Apr 04 2004 Intrinsic Spin <spin@freakbait.com>
- little cleanups
- Built for FC1

* Sun Jan 11 2004 Intrinsic Spin <spin@freakbait.com>
- Built against a reasonably good (according to dashboard) CVS version so-as
 to get GL2PS support.
- Rearranged. Cleaned up. Added some comments. 

* Sat Jan 10 2004 Intrinsic Spin <spin@freakbait.com>
- Blatently stole this spec file for my own nefarious purposes.
- Removed Java (for now). Merged the Python and Tcl stuff into 
 the main rpm.

* Fri Dec 05 2003 Fabrice Bellet <Fabrice.Bellet@creatis.insa-lyon.fr>
- (See Fabrice's RPMs for any more comments --Spin)
