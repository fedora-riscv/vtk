%bcond_without OSMesa
%bcond_with qt4
%bcond_with java

%{!?python_sitearch:%global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary: The Visualization Toolkit - A high level 3D visualization library
Name: vtk
Version: 5.0.3
Release: 23%{?dist}
License: BSD-like
Group: System Environment/Libraries
Source: http://www.vtk.org/files/release/5.0/%{name}-%{version}.tar.gz
Patch0: vtk-5.0.0-pythondestdir.patch
URL: http://vtk.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: cmake >= 2.0.4
BuildRequires: gcc-c++
%{?with_java:BuildRequires: java-devel}
BuildRequires: libX11-devel, libXt-devel, libXext-devel
BuildRequires: libICE-devel, libGL-devel
%{?with_OSMesa:BuildRequires: mesa-libOSMesa-devel}
BuildRequires: tk-devel, tcl-devel
BuildRequires: python-devel
BuildRequires: expat-devel, freetype-devel, libjpeg-devel, libpng-devel
BuildRequires: libtiff-devel, zlib-devel
BuildRequires: qt-devel
%{?with_qt4:BuildRequires: qt4-devel}
BuildRequires: chrpath

%description
VTK is an open-source software system for image processing, 3D
graphics, volume rendering and visualization. VTK includes many
advanced algorithms (e.g., surface reconstruction, implicit modelling,
decimation) and rendering techniques (e.g., hardware-accelerated
volume rendering, LOD control).

%package devel
Summary: VTK header files for building C++ code
Requires: vtk = %{version}-%{release}
Group: Development/Libraries

%description devel 
This provides the VTK header files required to compile C++ programs that
use VTK to do 3D visualisation.

%package tcl
Summary: Tcl bindings for VTK
Requires: vtk = %{version}-%{release}
Group: System Environment/Libraries

%description tcl
tcl bindings for VTK

%package python
Summary: Python bindings for VTK
Requires: vtk = %{version}-%{release}
Group: System Environment/Libraries

%description python
python bindings for VTK

%if %{with java}
%package java
Summary: Java bindings for VTK
Requires: vtk = %{version}-%{release}
Group: System Environment/Libraries

%description java
Java bindings for VTK
%endif

%package qt
Summary: Qt bindings for VTK
Requires: vtk = %{version}-%{release}
Group: System Environment/Libraries

%description qt
Qt bindings for VTK

%package testing
Summary: Testing programs for VTK
Requires: vtk = %{version}-%{release}, vtkdata = %{version}
Group: Applications/Engineering

%description testing
Testing programs for VTK

%package examples
Summary: Examples for VTK
Requires: vtk = %{version}-%{release}, vtkdata = %{version}
Group: Applications/Engineering

%description examples
This package contains many well-commented examples showing how to use
VTK. Examples are available in the C++, Tcl, Python and Java
programming languages.


%prep
%setup -q -n VTK
%patch0 -p1

# Replace relative path ../../../VTKData with %{_datadir}/vtkdata-%{version}
# otherwise it will break on symlinks.
grep -rl '\.\./\.\./\.\./\.\./VTKData' . | xargs \
  perl -pi -e's,\.\./\.\./\.\./\.\./VTKData,%{_datadir}/vtkdata-%{version},g'

# Remove executable bits from sources
find . -name \*.c -or -name \*.cxx -or -name \*.h | xargs chmod -x

# Save an unbuilt copy of the Example's sources for %doc
mkdir vtk-examples-5.0
cp -a Examples vtk-examples-5.0
find vtk-examples-5.0 -type f | xargs chmod -R a-x

%build
export CFLAGS="%{optflags} -D_UNICODE"
export CXXFLAGS="%{optflags} -D_UNICODE"
%if %{with java}
export JAVA_HOME=/usr/lib/jvm/java
%endif
%if %{with qt4}
unset QTINC QTLIB QTPATH_LRELEASE QMAKESPEC
export QTDIR=%{_libdir}/qt4
%endif

tmpinstall=`pwd`/tmpinstall

cmake_command="cmake . \
 -DBUILD_SHARED_LIBS:BOOL=ON \
 -DBUILD_DOCUMENTATION:BOOL=ON \
 -DBUILD_EXAMPLES:BOOL=ON \
 -DBUILD_TESTING:BOOL=ON \
 -DCMAKE_INSTALL_PREFIX:PATH=$tmpinstall \
 -DVTK_INSTALL_BIN_DIR:PATH=%{_bindir} \
 -DVTK_INSTALL_INCLUDE_DIR:PATH=%{_includedir}/vtk \
 -DVTK_INSTALL_LIB_DIR:PATH=%{_libdir} \
 -DVTK_DATA_ROOT:PATH=%{_datadir}/vtkdata-%{version} \
 -DTK_INTERNAL_PATH:PATH=/usr/include/tk-private/generic \
%if %{with OSMesa}
 -DVTK_OPENGL_HAS_OSMESA:BOOL=ON \
%endif
 -DVTK_WRAP_PYTHON:BOOL=ON \
%if %{with java}
 -DVTK_WRAP_JAVA:BOOL=ON \
 -DJAVA_INCLUDE_PATH:PATH=$JAVA_HOME/include \
 -DJAVA_INCLUDE_PATH2:PATH=$JAVA_HOME/include/linux \
 -DJAVA_AWT_INCLUDE_PATH:PATH=$JAVA_HOME/include \
%else
 -DVTK_WRAP_JAVA:BOOL=OFF \
%endif
 -DVTK_WRAP_TCL:BOOL=ON \
 -DVTK_USE_GL2PS:BOOL=ON \
 -DVTK_USE_GUISUPPORT:BOOL=ON \
 -DVTK_USE_PARALLEL:BOOL=ON \
 -DVTK_USE_SYSTEM_EXPAT=ON \
 -DVTK_USE_SYSTEM_FREETYPE=ON \
 -DVTK_USE_SYSTEM_JPEG=ON \
 -DVTK_USE_SYSTEM_PNG=ON \
 -DVTK_USE_SYSTEM_TIFF=ON \
 -DVTK_USE_SYSTEM_ZLIB=ON \
 -DVTK_USE_QVTK=ON \
%if %{with qt4}
 -DDESIRED_QT_VERSION=4 \
 -DQT_MOC_EXECUTABLE=%{_libdir}/qt4/bin/moc \
 -DVTK_INSTALL_QT_DIR=`qmake-qt4 -query QT_INSTALL_PREFIX`/plugins/designer \
%else
 -DVTK_INSTALL_QT_DIR=`qmake -query QT_INSTALL_PREFIX`/plugins/designer \
%endif
"
# Second cmake is neccessary for vtk
eval $cmake_command
eval $cmake_command

# Commented old flags in case we'd like to reactive some of them
# -DVTK_USE_DISPLAY:BOOL=OFF \ # This prevents building of graphics tests
# -DVTK_USE_HYBRID:BOOL=ON \
# -DVTK_USE_PATENTED:BOOL=ON \
# -DVTK_USE_RENDERING:BOOL=ON \
# -DVTK_USE_MPI:BOOL=OFF \
# -DVTK_USE_X:BOOL=ON \
# -DOPENGL_INCLUDE_DIR:PATH=/usr/include/GL \

make

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
make install
mv tmpinstall/* %{buildroot}/

if [ "%{_lib}" != lib -a "`ls %{buildroot}%{_prefix}/lib/*`" != "" ]; then
  mkdir -p %{buildroot}%{_libdir}
  mv %{buildroot}%{_prefix}/lib/* %{buildroot}%{_libdir}/
fi

# Gather list of non-python/tcl libraries
ls %{buildroot}%{_libdir}/*.so.* \
  | grep -Ev '(Java|QVTK|PythonD|TCL)' | sed -e's,^%{buildroot},,' > libs.list

mkdir -p %{buildroot}%{_libdir}/vtk-examples-5.0 \
         %{buildroot}%{_libdir}/vtk-testing-5.0

# List of executable utilities
cat > utils.list << EOF
vtkParseOGLExt
vtkVREncodeString
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

# List of executable test binaries
cat > testing.list << EOF
CommonCxxTests
TestCxxFeatures
TestInstantiator
FilteringCxxTests
GraphicsCxxTests
GenericFilteringCxxTests
ImagingCxxTests
IOCxxTests
RenderingCxxTests
VTKBenchMark
VolumeRenderingCxxTests
WidgetsCxxTests
SocketClient
SocketServer
EOF

# Install utils/examples/testing, too
for filelist in utils.list examples.list testing.list; do
  for file in `cat $filelist`; do
    install -p bin/$file %{buildroot}%{_bindir}
  done
  perl -pi -e's,^,%{_bindir}/,' $filelist
done

# Remove any remnants of rpaths
for file in `cat examples.list`; do
  chrpath -d %{buildroot}$file
done

# Main package contains utils and core libs
cat libs.list utils.list > main.list

# Make shared libs and scripts executable
chmod a+x %{buildroot}%{_libdir}/lib*.so.*
chmod a+x %{buildroot}%{_libdir}/vtk-5.0/doxygen/*.pl
chmod a+x %{buildroot}%{_libdir}/vtk-5.0/testing/*.{py,tcl}

# Remove exec bit from non-scripts and %%doc
for file in `find %{buildroot} -type f -perm 0755 \
  | xargs -r file | grep ASCII | awk -F: '{print $1}'`; do
  head -1 $file | grep '^#!' > /dev/null && continue
  chmod 0644 $file
done
find Utilities/Upgrading -type f | xargs chmod -x

# Add exec bits to shared libs ...
chmod 0755 %{buildroot}%{_libdir}/vtk-5.0/CMake/*.so

%check || :
#LD_LIBARARY_PATH=`pwd`/bin ctest -V

%clean
rm -rf %{buildroot}

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

%files -f main.list
%defattr(-,root,root,-)
%doc --parents Copyright.txt README.html vtkLogo.jpg vtkBanner.gif Wrapping/*/README*

%files devel
%defattr(-,root,root,-)
%doc Utilities/Upgrading
%{_libdir}/vtk-5.0/doxygen
%{_includedir}/vtk
%{_libdir}/*.so
%{_libdir}/vtk-5.0/CMake
%{_libdir}/vtk-5.0/*.cmake
%{_libdir}/vtk-5.0/hints

%files tcl
%defattr(-,root,root,-)
%{_libdir}/*TCL.so.*
%{_bindir}/vtk
%{_bindir}/vtkWrapTcl
%{_bindir}/vtkWrapTclInit
%{_libdir}/vtk-5.0/pkgIndex.tcl
%{_libdir}/vtk-5.0/tcl

%files python
%defattr(-,root,root,-)
%{python_sitearch}/vtk
%if 0%{?fedora} >= 9
%{python_sitearch}/*egg-info
%endif
%{_libdir}/*PythonD.so.*
%{_bindir}/vtkpython
%{_bindir}/vtkWrapPython
%{_bindir}/vtkWrapPythonInit

%if %{with java}
%files java
%defattr(-,root,root,-)
%{_libdir}/*Java.so.*
%{_bindir}/vtkParseJava
%{_bindir}/vtkWrapJava
%endif

%files qt
%defattr(-,root,root,-)
%{_libdir}/libQVTK.so.*
%{_libdir}/qt*/plugins/designer/libQVTKWidgetPlugin.so

%files testing -f testing.list
%defattr(-,root,root,-)
%{_libdir}/vtk-5.0/testing
%{_libdir}/vtk-testing-5.0

%files examples -f examples.list
%defattr(-,root,root,-)
%doc vtk-examples-5.0/Examples
%{_libdir}/vtk-examples-5.0

%changelog
* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 5.0.3-23
- Autorebuild for GCC 4.3

* Tue Jan 15 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 5.0.3-22
- Add Python Eggs for F9+

* Thu Jan 10 2008 Caolan McNamara <caolanm@redhat.com> - 5.0.3-21
- Rebuild for new tcl/tk

* Tue Aug 28 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 5.0.3-20
- Rebuild for selinux ppc32 issue.

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

* Mon Apr 04 2004 Intrinsic Spin <spin@freakbait.com> 2.mr
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
