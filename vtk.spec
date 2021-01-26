%undefine __cmake_in_source_build

# State Nov 11 2020, LTO causes
# TestXMLHyperTreeGridIO.cxx.o (symbol from plugin): undefined reference to symbol
# '_ZZNSt8__detail18__to_chars_10_implIjEEvPcjT_E8__digits@@LLVM_11'
%global _lto_cflags %{nil}

# Disable OSMesa builds for now - see Bug 744434
%bcond_without OSMesa
%bcond_without java
%bcond_without mpich
%bcond_without qt5
%bcond_without openmpi
# s390x on EL8 does not have xorg-x11-drv-dummy
%if 0%{?rhel}
%ifarch s390x
%bcond_with    xdummy
%else
%bcond_without xdummy
%endif
%else
%bcond_without xdummy
%endif

%if 0%{?fedora} >= 33 || 0%{?rhel} >= 9
%bcond_without flexiblas
%endif

# VTK currently is carrying local modifications to gl2ps
%bcond_with gl2ps
%if !%{with gl2ps}
%global vtk_use_system_gl2ps -DVTK_USE_SYSTEM_GL2PS:BOOL=OFF
%endif

Summary: The Visualization Toolkit - A high level 3D visualization library
Name: vtk
Version: 8.2.0
Release: 25%{?dist}
# This is a variant BSD license, a cross between BSD and ZLIB.
# For all intents, it has the same rights and restrictions as BSD.
# http://fedoraproject.org/wiki/Licensing/BSD#VTKBSDVariant
License: BSD
Source0: http://www.vtk.org/files/release/8.2/VTK-%{version}.tar.gz
Source1: http://www.vtk.org/files/release/8.2/VTKData-%{version}.tar.gz
Source2: xorg.conf
Source3: FindPEGTL.cmake
# Python 3.8 support
Patch0: https://gitlab.kitware.com/vtk/vtk/merge_requests/5883.patch
# Proj 6 support
Patch1: vtk-proj6_compat.patch
# GCC 10 support based on:
# https://gitlab.kitware.com/vtk/vtk/-/merge_requests/6420
Patch2: vtk-gcc10.patch
# Qt 5.15 support
# https://gitlab.kitware.com/vtk/vtk/-/issues/18005
Patch3: vtk-qt5.15.patch
# Temporary patch for building against freetype-2.10.4, which removed FT_CALLBACK_DEF,
# but was later re-added in https://git.savannah.gnu.org/cgit/freetype/freetype2.git/commit/?id=b0667d2d36fb134d48030b2a560eaaa37810d6ba
Patch4: vtk_freetype-2.10.4.patch

URL: http://vtk.org/

BuildRequires: cmake
BuildRequires: gcc-c++
%{?with_java:BuildRequires: java-devel}
BuildRequires: libX11-devel, libXt-devel, libXext-devel
BuildRequires: libICE-devel, libGL-devel
%{?with_OSMesa:BuildRequires: mesa-libOSMesa-devel}
BuildRequires: tk-devel, tcl-devel
BuildRequires: python%{python3_pkgversion}-devel
BuildRequires: expat-devel, freetype-devel, libjpeg-devel, libpng-devel
%if 0%{with gl2ps}
BuildRequires: gl2ps-devel
%endif
BuildRequires: libtiff-devel, zlib-devel
BuildRequires: libxml2-devel
%if %{with qt5}
BuildRequires: cmake(Qt5)
BuildRequires: cmake(Qt5UiPlugin)
BuildRequires: cmake(Qt5X11Extras)
BuildRequires: qt5-qtwebkit-devel
BuildRequires: python%{python3_pkgversion}-qt5
%else
BuildRequires: PyQt4-devel
BuildRequires: qt4-devel
BuildRequires: qtwebkit-devel
%endif
BuildRequires: chrpath
BuildRequires: doxygen, graphviz
BuildRequires: gnuplot
BuildRequires: boost-devel
BuildRequires: double-conversion-devel
BuildRequires: eigen3-devel
BuildRequires: glew-devel
BuildRequires: hdf5-devel
BuildRequires: jsoncpp-devel
BuildRequires: libtheora-devel
BuildRequires: mariadb-connector-c-devel
BuildRequires: netcdf-cxx-devel
BuildRequires: libpq-devel
BuildRequires: PEGTL-devel
BuildRequires: proj-devel
BuildRequires: pugixml-devel
BuildRequires: R-devel
BuildRequires: sqlite-devel
BuildRequires: wget
%if %{with flexiblas}
BuildRequires: flexiblas-devel
%else
BuildRequires: blas-devel
BuildRequires: lapack-devel
%endif
# Requires patched libharu https://github.com/libharu/libharu/pull/157
#BuildRequires: libharu-devel
BuildRequires: lz4-devel
BuildRequires: motif-devel
%if %{with mpich}
BuildRequires:  mpich-devel
BuildRequires:  python%{?python3_pkgversion}-mpi4py-mpich
BuildRequires:  netcdf-mpich-devel
%endif
%if %{with openmpi}
BuildRequires:  openmpi-devel
BuildRequires:  python%{?python3_pkgversion}-mpi4py-openmpi
BuildRequires:  netcdf-openmpi-devel
%endif
# For %check
%if %{with xdummy}
BuildRequires: xorg-x11-drv-dummy
%endif
%{!?with_java:Conflicts: vtk-java}
Requires: hdf5 = %{_hdf5_version}

# Bundled KWSys
# https://fedorahosted.org/fpc/ticket/555
# Components used are specified in Utilities/KWSys/CMakeLists.txt
Provides: bundled(kwsys-base64)
Provides: bundled(kwsys-commandlinearguments)
Provides: bundled(kwsys-directory)
Provides: bundled(kwsys-dynamicloader)
Provides: bundled(kwsys-encoding)
Provides: bundled(kwsys-fstream)
Provides: bundled(kwsys-fundamentaltype)
Provides: bundled(kwsys-glob)
Provides: bundled(kwsys-md5)
Provides: bundled(kwsys-process)
Provides: bundled(kwsys-regularexpression)
Provides: bundled(kwsys-system)
Provides: bundled(kwsys-systeminformation)
Provides: bundled(kwsys-systemtools)
# Other bundled libraries
Provides: bundled(diy2)
Provides: bundled(exodusII) = 2.0.0
Provides: bundled(ftgl) = 1.32
%if !%{with gl2ps}
Provides: bundled(gl2ps) = 1.4.0
%endif
Provides: bundled(libharu)
Provides: bundled(metaio)
Provides: bundled(pugixml) = 1.8
Provides: bundled(utf8cpp)
Provides: bundled(verdict) = 1.2.0
Provides: bundled(vpic)
Provides: bundled(xdmf2) = 2.1
Provides: bundled(xdmf3)

Obsoletes: %{name}-tcl < 8.2.0-1
Obsoletes: %{name}-qt-tcl < 8.2.0-1

%description
VTK is an open-source software system for image processing, 3D
graphics, volume rendering and visualization. VTK includes many
advanced algorithms (e.g., surface reconstruction, implicit modeling,
decimation) and rendering techniques (e.g., hardware-accelerated
volume rendering, LOD control).

NOTE: The version in this package has NOT been compiled with MPI support.
%if %{with mpich}
Install the %{name}-mpich package to get a version compiled with mpich.
%endif
%if %{with openmpi}
Install the %{name}-openmpi package to get a version compiled with openmpi.
%endif

%package devel
Summary: VTK header files for building C++ code
Requires: vtk%{?_isa} = %{version}-%{release}
Requires: python%{python3_pkgversion}-vtk%{?_isa} = %{version}-%{release}
Requires: python%{python3_pkgversion}-vtk-qt%{?_isa} = %{version}-%{release}
%{?with_OSMesa:Requires: mesa-libOSMesa-devel%{?_isa}}
Requires: cmake
%if %{with flexiblas}
Requires: flexiblas-devel%{?_isa}
%else
Requires: blas-devel%{?_isa}
Requires: lapack-devel%{?_isa}
%endif
Requires: double-conversion-devel%{?_isa}
# eigen3 is noarch
Requires: eigen3-devel
Requires: expat-devel%{?_isa}
Requires: freetype-devel%{?_isa}
%if %{with gl2ps}
Requires: gl2ps-devel%{?_isa}
%endif
Requires: glew-devel%{?_isa}
Requires: hdf5-devel%{?_isa}
Requires: libjpeg-devel%{?_isa}
Requires: lz4-devel%{?_isa}
Requires: libpng-devel%{?_isa}
Requires: libogg-devel%{?_isa}
Requires: libSM-devel%{?_isa}
Requires: libtheora-devel%{?_isa}
Requires: libtiff-devel%{?_isa}
Requires: libxml2-devel%{?_isa}
Requires: libpq-devel%{?_isa}
Requires: PEGTL-devel%{?_isa}
Requires: proj-devel%{?_isa}
Requires: pugixml-devel%{?_isa}
Requires: sqlite-devel%{?_isa}
Requires: libX11-devel%{?_isa}
Requires: libXext-devel%{?_isa}
Requires: libXt-devel%{?_isa}
Requires: mariadb-devel%{?_isa}
Requires: netcdf-cxx-devel%{?_isa}
%if %{with qt5}
Requires: cmake(Qt5)
Requires: cmake(Qt5UiPlugin)
Requires: cmake(Qt5X11Extras)
Requires: qt5-qtwebkit-devel%{?_isa}
%else
Requires: qt4-devel%{?_isa}
Requires: qtwebkit-devel%{?_isa}
%endif
Requires: jsoncpp-devel%{?_isa}
# bz #1183210 + #1183530
Requires: python%{python3_pkgversion}-devel

%description devel 
This provides the VTK header files required to compile C++ programs that
use VTK to do 3D visualization.

%package -n python%{python3_pkgversion}-vtk
Summary: Python 3 bindings for VTK
Requires: vtk%{?_isa} = %{version}-%{release}
%{?python_provide:%python_provide python%{python3_pkgversion}-vtk}
Provides: %{py3_dist vtk} = %{version}
Provides: python%{python3_version}dist(vtk) = %{version}

%description -n python%{python3_pkgversion}-vtk
Python 3 bindings for VTK.

%if %{with java}
%package java
Summary: Java bindings for VTK
Requires: vtk%{?_isa} = %{version}-%{release}

%description java
Java bindings for VTK.
%endif

%package qt
Summary: Qt bindings for VTK
Requires: vtk%{?_isa} = %{version}-%{release}

%description qt
Qt bindings for VTK.

%package -n python%{python3_pkgversion}-vtk-qt
Summary: Qt Python 3 bindings for VTK
Requires: vtk%{?_isa} = %{version}-%{release}
%{?python_provide:%python_provide python%{python3_pkgversion}-vtk-qt}

%description -n python%{python3_pkgversion}-vtk-qt
Qt Python 3 bindings for VTK.

%if %{with mpich}
%package mpich
Summary: The Visualization Toolkit - mpich version

Obsoletes: %{name}-mpich-tcl < 8.2.0-1
Obsoletes: %{name}-mpich-qt-tcl < 8.2.0-1

%description mpich
VTK is an open-source software system for image processing, 3D
graphics, volume rendering and visualization. VTK includes many
advanced algorithms (e.g., surface reconstruction, implicit modeling,
decimation) and rendering techniques (e.g., hardware-accelerated
volume rendering, LOD control).

NOTE: The version in this package has been compiled with mpich support.

%package mpich-devel
Summary: VTK header files for building C++ code with mpich
Requires: vtk-mpich%{?_isa} = %{version}-%{release}
#Requires: python2-vtk%{?_isa} = %{version}-%{release}
#Requires: python2-vtk-qt%{?_isa} = %{version}-%{release}
%{?with_OSMesa:Requires: mesa-libOSMesa-devel%{?_isa}}
Requires: cmake
Requires: mpich-devel
%if %{with flexiblas}
Requires: flexiblas-devel%{?_isa}
%else
Requires: blas-devel%{?_isa}
Requires: lapack-devel%{?_isa}
%endif
%if 0%{with gl2ps}
Requires: gl2ps-devel%{?_isa}
%endif
Requires: expat-devel%{?_isa}
Requires: freetype-devel%{?_isa}
Requires: hdf5-mpich-devel%{?_isa}
Requires: libjpeg-devel%{?_isa}
Requires: libpng-devel%{?_isa}
Requires: libogg-devel%{?_isa}
Requires: libtheora-devel%{?_isa}
Requires: libtiff-devel%{?_isa}
Requires: libxml2-devel%{?_isa}
Requires: libpq-devel%{?_isa}
Requires: mariadb-devel%{?_isa}
Requires: netcdf-cxx-devel%{?_isa}
Requires: netcdf-mpich-devel%{?_isa}
%if %{with qt5}
Requires: cmake(Qt5)
Requires: cmake(Qt5UiPlugin)
Requires: cmake(Qt5X11Extras)
Requires: qt5-qtwebkit-devel%{?_isa}
%else
Requires: qt4-devel%{?_isa}
Requires: qtwebkit-devel%{?_isa}
%endif
Requires: jsoncpp-devel%{?_isa}
# bz #1183210 + #1183530
Requires: python%{python3_pkgversion}-devel

%description mpich-devel 
This provides the VTK header files required to compile C++ programs that
use VTK to do 3D visualization.

NOTE: The version in this package has been compiled with mpich support.

%package -n python%{python3_pkgversion}-vtk-mpich
Summary: Python 3 bindings for VTK with mpich
Requires: vtk-mpich%{?_isa} = %{version}-%{release}

%description -n python%{python3_pkgversion}-vtk-mpich
python 3 bindings for VTK with mpich.

%if %{with java}
%package mpich-java
Summary: Java bindings for VTK with mpich
Requires: vtk-mpich%{?_isa} = %{version}-%{release}

%description mpich-java
Java bindings for VTK with mpich.
%endif

%package mpich-qt
Summary: Qt bindings for VTK with mpich
Requires: vtk-mpich%{?_isa} = %{version}-%{release}

%description mpich-qt
Qt bindings for VTK with mpich.

%package -n python%{python3_pkgversion}-vtk-mpich-qt
Summary: Qt Python 3 bindings for VTK with mpich
Requires: vtk-mpich%{?_isa} = %{version}-%{release}

%description -n python%{python3_pkgversion}-vtk-mpich-qt
Qt Python 3 bindings for VTK with mpich.
%endif

%if %{with openmpi}
%package openmpi
Summary: The Visualization Toolkit - openmpi version

Obsoletes: %{name}-openmpi-tcl < 8.2.0-1
Obsoletes: %{name}-openmpi-qt-tcl < 8.2.0-1

%description openmpi
VTK is an open-source software system for image processing, 3D
graphics, volume rendering and visualization. VTK includes many
advanced algorithms (e.g., surface reconstruction, implicit modeling,
decimation) and rendering techniques (e.g., hardware-accelerated
volume rendering, LOD control).

NOTE: The version in this package has been compiled with openmpi support.

%package openmpi-devel
Summary: VTK header files for building C++ code with openmpi
Requires: vtk-openmpi%{?_isa} = %{version}-%{release}
#Requires: python2-vtk%{?_isa} = %{version}-%{release}
#Requires: python2-vtk-qt%{?_isa} = %{version}-%{release}
%{?with_OSMesa:Requires: mesa-libOSMesa-devel%{?_isa}}
Requires: cmake
Requires: openmpi-devel
%if %{with flexiblas}
Requires: flexiblas-devel%{?_isa}
%else
Requires: blas-devel%{?_isa}
Requires: lapack-devel%{?_isa}
%endif
%if 0%{with gl2ps}
Requires: gl2ps-devel%{?_isa}
%endif
Requires: expat-devel%{?_isa}
Requires: freetype-devel%{?_isa}
Requires: hdf5-openmpi-devel%{?_isa}
Requires: libjpeg-devel%{?_isa}
Requires: libpng-devel%{?_isa}
Requires: libogg-devel%{?_isa}
Requires: libtheora-devel%{?_isa}
Requires: libtiff-devel%{?_isa}
Requires: libxml2-devel%{?_isa}
Requires: libpq-devel%{?_isa}
Requires: mariadb-devel%{?_isa}
Requires: netcdf-cxx-devel%{?_isa}
Requires: netcdf-openmpi-devel%{?_isa}
%if %{with qt5}
Requires: cmake(Qt5)
Requires: cmake(Qt5UiPlugin)
Requires: cmake(Qt5X11Extras)
Requires: qt5-qtwebkit-devel%{?_isa}
%else
Requires: qt4-devel%{?_isa}
Requires: qtwebkit-devel%{?_isa}
%endif
Requires: jsoncpp-devel%{?_isa}
# bz #1183210 + #1183530
Requires: python%{python3_pkgversion}-devel

%description openmpi-devel 
This provides the VTK header files required to compile C++ programs that
use VTK to do 3D visualization.

NOTE: The version in this package has been compiled with openmpi support.

%package -n python%{python3_pkgversion}-vtk-openmpi
Summary: Python 3 bindings for VTK with openmpi
Requires: vtk-openmpi%{?_isa} = %{version}-%{release}

%description -n python%{python3_pkgversion}-vtk-openmpi
Python 3 bindings for VTK with openmpi.

%if %{with java}
%package openmpi-java
Summary: Java bindings for VTK with openmpi
Requires: vtk-openmpi%{?_isa} = %{version}-%{release}
%endif

%description openmpi-java
Java bindings for VTK with openmpi.

%package openmpi-qt
Summary: Qt bindings for VTK with openmpi
Requires: vtk-openmpi%{?_isa} = %{version}-%{release}

%description openmpi-qt
Qt bindings for VTK with openmpi.

%package -n python%{python3_pkgversion}-vtk-openmpi-qt
Summary: Qt Python 3 bindings for VTK with openmpi
Requires: vtk-openmpi%{?_isa} = %{version}-%{release}

%description -n python%{python3_pkgversion}-vtk-openmpi-qt
Qt Python 3 bindings for VTK with openmpi.
%endif

%package data
Summary: VTK data files for tests/examples
BuildArch: noarch
Obsoletes: vtkdata < 6.1.0-3

%description data
VTK data files for tests and examples.

%package testing
Summary: Testing programs for VTK
Requires: vtk%{?_isa} = %{version}-%{release}, vtk-data = %{version}

%description testing
Testing programs for VTK

%package examples
Summary: Examples for VTK
Requires: vtk%{?_isa} = %{version}-%{release}, vtk-data = %{version}

%description examples
This package contains many well-commented examples showing how to use
VTK. Examples are available in the C++, Tcl, Python and Java
programming languages.


%prep
%setup -q -b 1 -n VTK-%{version}
%patch0 -p1 -b .py38
%patch1 -p1 -b .proj6
%patch2 -p1 -b .gcc10
%patch3 -p1 -b .qt5.15
%patch4 -p1 -b .freetype
# Remove included thirdparty sources just to be sure
# TODO - diy2 - not yet packaged
# TODO - exodusII - not yet packaged
# TODO - pugixml - https://gitlab.kitware.com/vtk/vtk/issues/17538
# TODO - utf8cpp(source) - http://www.vtk.org/Bug/view.php?id=15730
# TODO - verdict - not yet packaged
# TODO - VPIC - not yet packaged
# TODO - xdmf2 - not yet packaged
# TODO - xdmf3 - not yet packaged
for x in vtk{doubleconversion,eigen,expat,freetype,%{?_with_gl2ps:gl2ps,}glew,hdf5,jpeg,jsoncpp,kissfft,libproj,libxml2,lz4,lzma,mpi4py,netcdf,ogg,pegtl,png,sqlite,theora,tiff,zfp,zlib}
do
  rm -r ThirdParty/*/${x}
done

# Needed to find PEGTL
cp %SOURCE3 CMake/FindPEGTL.cmake

# Remove unused KWSys items
find Utilities/KWSys/vtksys/ -name \*.[ch]\* | grep -vE '^Utilities/KWSys/vtksys/([a-z].*|Configure|SharedForward|String\.hxx|Base64|CommandLineArguments|Directory|DynamicLoader|Encoding|FStream|FundamentalType|Glob|MD5|Process|RegularExpression|System|SystemInformation|SystemTools)(C|CXX|UNIX)?\.' | xargs rm

# Save an unbuilt copy of the Example's sources for %doc
mkdir vtk-examples
cp -a Examples vtk-examples
# Don't ship Win32 examples
rm -r vtk-examples/Examples/GUI/Win32
find vtk-examples -type f | xargs chmod -R a-x

%build
export CFLAGS="%{optflags} -D_UNICODE -DHAVE_UINTPTR_T"
export CXXFLAGS="%{optflags} -D_UNICODE -DHAVE_UINTPTR_T"
export CPPFLAGS=-DACCEPT_USE_OF_DEPRECATED_PROJ_API_H
%if %{with java}
export JAVA_HOME=/usr/lib/jvm/java
%ifarch %{arm} s390x
# getting "java.lang.OutOfMemoryError: Java heap space" during the build
export JAVA_TOOL_OPTIONS=-Xmx2048m
%endif
%endif

%global vtk_cmake_options \\\
 -DVTK_CUSTOM_LIBRARY_SUFFIX="" \\\
 -DVTK_INSTALL_ARCHIVE_DIR:PATH=%{_lib} \\\
 -DVTK_INSTALL_DATA_DIR=share/vtk \\\
 -DVTK_INSTALL_INCLUDE_DIR:PATH=include/vtk \\\
 -DVTK_INSTALL_LIBRARY_DIR:PATH=%{_lib} \\\
 -DVTK_INSTALL_PACKAGE_DIR:PATH=%{_lib}/cmake/vtk \\\
 -DVTK_PYTHON_VERSION=3 \\\
%if %{with qt5} \
 -DVTK_INSTALL_QT_DIR:PATH=%{_lib}/qt5/plugins/designer \\\
%else \
 -DVTK_INSTALL_QT_DIR:PATH=%{_lib}/qt4/plugins/designer \\\
%endif \
 -DTK_INTERNAL_PATH:PATH=/usr/include/tk-private/generic \\\
%if %{with OSMesa} \
 -DVTK_OPENGL_HAS_OSMESA:BOOL=ON \\\
%endif \
%if %{with java} \
 -DVTK_WRAP_JAVA:BOOL=ON \\\
 -DJAVA_INCLUDE_PATH:PATH=$JAVA_HOME/include \\\
 -DJAVA_INCLUDE_PATH2:PATH=$JAVA_HOME/include/linux \\\
 -DJAVA_AWT_INCLUDE_PATH:PATH=$JAVA_HOME/include \\\
%else \
 -DVTK_WRAP_JAVA:BOOL=OFF \\\
%endif \
 -DVTK_WRAP_PYTHON:BOOL=ON \\\
 -DVTK_Group_Imaging:BOOL=ON \\\
 -DVTK_Group_Qt:BOOL=ON \\\
 -DVTK_Group_Rendering:BOOL=ON \\\
 -DVTK_Group_StandAlone:BOOL=ON \\\
 -DVTK_Group_Tk:BOOL=ON \\\
 -DVTK_Group_Views:BOOL=ON \\\
 -DModule_vtkIOExportOpenGL2:BOOL=ON \\\
 -DModule_vtkIOMySQL:BOOL=ON \\\
 -DModule_vtkIOPostgreSQL:BOOL=ON \\\
 -DModule_vtkRenderingParallel:BOOL=ON \\\
 -DModule_vtkTestingCore:BOOL=ON \\\
 -DModule_vtkTestingRendering:BOOL=ON \\\
%if %{with qt5} \
 -DVTK_QT_VERSION:STRING="5" \\\
%endif \
 -DVTK_USE_OGGTHEORA_ENCODER=ON \\\
 -DVTK_USE_SYSTEM_LIBRARIES=ON \\\
 %{?vtk_use_system_gl2ps} \\\
 -DVTK_USE_SYSTEM_HDF5:BOOL=ON \\\
 -DVTK_USE_SYSTEM_LIBHARU=OFF \\\
 -DVTK_USE_SYSTEM_NETCDF:BOOL=ON
# Commented old flags in case we'd like to reactive some of them
# -DVTK_USE_DISPLAY:BOOL=OFF \ # This prevents building of graphics tests

%global _vpath_builddir build
%cmake \
 %{vtk_cmake_options} \
 %{?with_flexiblas:-DBLAS_LIBRARIES=-lflexiblas} \
 -DBUILD_DOCUMENTATION:BOOL=ON \
 -DBUILD_EXAMPLES:BOOL=ON \
 -DBUILD_TESTING:BOOL=ON
%cmake_build
%cmake_build --target DoxygenDoc vtkMyDoxygenDoc

%if %{with mpich}
%global _vpath_builddir build-mpich
%_mpich_load
export CC=mpicc
export CXX=mpic++
%cmake \
 %{vtk_cmake_options} \
 -DCMAKE_PREFIX_PATH:PATH=$MPI_HOME \
 -DCMAKE_INSTALL_PREFIX:PATH=$MPI_HOME \
 -DVTK_INSTALL_ARCHIVE_DIR:PATH=lib \
 -DVTK_INSTALL_LIBRARY_DIR:PATH=lib \
 -DVTK_INSTALL_PACKAGE_DIR:PATH=lib/cmake \
%if %{with qt5}
 -DVTK_INSTALL_QT_DIR:PATH=lib/qt5/plugins/designer \
%else
 -DVTK_INSTALL_QT_DIR:PATH=lib/qt4/plugins/designer \
%endif
 -DVTK_Group_MPI:BOOL=ON \
 -DModule_vtkRenderingParallel:BOOL=ON \
 -DVTK_USE_PARALLEL:BOOL=ON \
 -DVTK_USE_SYSTEM_DIY2:BOOL=OFF \
 -DVTK_USE_SYSTEM_MPI4PY:BOOL=ON
%cmake_build
%_mpich_unload
%endif

%if %{with openmpi}
%global _vpath_builddir build-openmpi
%_openmpi_load
export CC=mpicc
export CXX=mpic++
%cmake \
 %{vtk_cmake_options} \
 -DCMAKE_PREFIX_PATH:PATH=$MPI_HOME \
 -DCMAKE_INSTALL_PREFIX:PATH=$MPI_HOME \
 -DVTK_INSTALL_ARCHIVE_DIR:PATH=lib \
 -DVTK_INSTALL_LIBRARY_DIR:PATH=lib \
 -DVTK_INSTALL_PACKAGE_DIR:PATH=lib/cmake \
%if %{with qt5}
 -DVTK_INSTALL_QT_DIR:PATH=lib/qt5/plugins/designer \
%else
 -DVTK_INSTALL_QT_DIR:PATH=lib/qt4/plugins/designer \
%endif
 -DVTK_Group_MPI:BOOL=ON \
 -DModule_vtkRenderingParallel:BOOL=ON \
 -DVTK_USE_PARALLEL:BOOL=ON \
 -DVTK_USE_SYSTEM_DIY2:BOOL=OFF \
 -DVTK_USE_SYSTEM_MPI4PY:BOOL=ON
%cmake_build
%_openmpi_unload
%endif

# Remove executable bits from sources (some of which are generated)
find . -name \*.c -or -name \*.cxx -or -name \*.h -or -name \*.hxx -or \
       -name \*.gif | xargs chmod -x


%install
%global _vpath_builddir build
%cmake_install

pushd build
# Gather list of non-python/tcl libraries
ls %{buildroot}%{_libdir}/*.so.* \
  | grep -Ev '(Java|Qt|Python..D|TCL)' | sed -e's,^%{buildroot},,' > libs.list

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
find bin \( -name \*Tests -o -name Test\* -o -name VTKBenchMark \) \
         -printf '%f\n' > testing.list

# Install examples too
for filelist in examples.list testing.list; do
  for file in `cat $filelist`; do
    install -p bin/$file %{buildroot}%{_bindir}
  done
done

# Fix up filelist paths
for filelist in examples.list testing.list; do
  perl -pi -e's,^,%{_bindir}/,' $filelist
done

# Remove any remnants of rpaths on files we install
# Seems to be some kind of java path
for file in `cat examples.list testing.list`; do
  chrpath -d %{buildroot}$file
done
chrpath -d  %{buildroot}%{_libdir}/qt?/plugins/designer/libQVTKWidgetPlugin.so

# Main package contains utils and core libs
cat libs.list
popd

%if %{with mpich}
%_mpich_load
%global _vpath_builddir build-mpich
%cmake_install

# Gather list of non-python/tcl libraries
ls %{buildroot}%{_libdir}/mpich/lib/*.so.* \
  | grep -Ev '(Java|Qt|Python..D|TCL)' | sed -e's,^%{buildroot},,' > build-mpich/libs.list
%_mpich_unload
%endif

%if %{with openmpi}
%_openmpi_load
%global _vpath_builddir build-openmpi
%cmake_install

# Gather list of non-python/tcl libraries
ls %{buildroot}%{_libdir}/openmpi/lib/*.so.* \
  | grep -Ev '(Java|Qt|Python..D|TCL)' | sed -e's,^%{buildroot},,' > build-openmpi/libs.list
%_openmpi_unload
%endif

# Remove exec bit from non-scripts and %%doc
for file in `find %{buildroot} -type f -perm 0755 \
  | xargs -r file | grep ASCII | awk -F: '{print $1}'`; do
  head -1 $file | grep '^#!' > /dev/null && continue
  chmod 0644 $file
done
find Utilities/Upgrading -type f -print0 | xargs -0 chmod -x

# Setup Wrapping docs tree
mkdir -p _docs
cp -pr --parents Wrapping/*/README* _docs/ 

#Install data
mkdir -p %{buildroot}%{_datadir}/vtkdata
cp -alL build/ExternalData/* %{buildroot}%{_datadir}/vtkdata/

%check
cp %SOURCE2 .
%if %{with xdummy}
if [ -x /usr/libexec/Xorg ]; then
   Xorg=/usr/libexec/Xorg
else
   Xorg=/usr/libexec/Xorg.bin
fi
$Xorg -noreset +extension GLX +extension RANDR +extension RENDER -logfile ./xorg.log -config ./xorg.conf -configdir . :99 &
export DISPLAY=:99
%endif
%global _vpath_builddir build
export FLEXIBLAS=netlib
%ctest --verbose || :
%if %{with xdummy}
kill %1 || :
cat xorg.log
%endif


%files -f build/libs.list
%license Copyright.txt
%doc README.md _docs/Wrapping

%files devel
%doc Utilities/Upgrading
%{_bindir}/vtkWrapHierarchy
%{_includedir}/vtk
%{_libdir}/*.so
%{_libdir}/libvtkWrappingTools.a
%{_libdir}/cmake/vtk/
%{_docdir}/vtk-8.2/

%files -n python%{python3_pkgversion}-vtk
%{python3_sitearch}/*
%{_libdir}/*Python%{python3_version_nodots}D.so.*
%exclude %{_libdir}/*QtPython%{python3_version_nodots}D.so.*
%{_bindir}/vtkpython
%{_bindir}/vtkWrapPython
%{_bindir}/vtkWrapPythonInit

%if %{with java}
%files java
%{_libdir}/*Java.so.*
%{_libdir}/vtk.jar
%{_bindir}/vtkParseJava
%{_bindir}/vtkWrapJava
%endif

%files qt
%{_libdir}/lib*Qt*.so.*
%exclude %{_libdir}/*Python%{python3_version_nodots}D.so.*
%{_libdir}/qt?/plugins/designer/libQVTKWidgetPlugin.so

%files -n python%{python3_pkgversion}-vtk-qt
%{_libdir}/*QtPython%{python3_version_nodots}D.so.*

%if %{with mpich}
%files mpich -f build-mpich/libs.list
%license Copyright.txt
%doc README.md _docs/Wrapping

%files mpich-devel
%{_libdir}/mpich/bin/vtkWrapHierarchy
%{_libdir}/mpich/include/
%{_libdir}/mpich/lib/*.so
%{_libdir}/mpich/lib/libvtkWrappingTools.a
%{_libdir}/mpich/lib/cmake/
%{_libdir}/mpich/share/doc/vtk-8.2/

%files -n python%{python3_pkgversion}-vtk-mpich
%{_libdir}/mpich/lib/python%{python3_version}/
%{_libdir}/mpich/lib/*Python%{python3_version_nodots}D.so.*
%exclude %{_libdir}/mpich/lib/*QtPython%{python3_version_nodots}D.so.*
%{_libdir}/mpich/bin/pvtkpython
%{_libdir}/mpich/bin/vtkpython
%{_libdir}/mpich/bin/vtkWrapPython
%{_libdir}/mpich/bin/vtkWrapPythonInit

%if %{with java}
%files mpich-java
%{_libdir}/mpich/lib/*Java.so.*
%{_libdir}/mpich/lib/vtk.jar
%{_libdir}/mpich/bin/vtkParseJava
%{_libdir}/mpich/bin/vtkWrapJava
%endif

%files mpich-qt
%{_libdir}/mpich/lib/lib*Qt*.so.*
%exclude %{_libdir}/mpich/lib/*Python%{python3_version_nodots}D.so.*
%{_libdir}/mpich/lib/qt?/

%files -n python%{python3_pkgversion}-vtk-mpich-qt
%{_libdir}/mpich/lib/*QtPython%{python3_version_nodots}D.so.*
%endif

%if %{with openmpi}
%files openmpi -f build-openmpi/libs.list
%license Copyright.txt
%doc README.md _docs/Wrapping

%files openmpi-devel
%{_libdir}/openmpi/bin/vtkWrapHierarchy
%{_libdir}/openmpi/include/
%{_libdir}/openmpi/lib/*.so
%{_libdir}/openmpi/lib/libvtkWrappingTools.a
%{_libdir}/openmpi/lib/cmake/
%{_libdir}/openmpi/share/doc/vtk-8.2/


%files -n python%{python3_pkgversion}-vtk-openmpi
%{_libdir}/openmpi/lib/python%{python3_version}/
%{_libdir}/openmpi/lib/*Python%{python3_version_nodots}D.so.*
%exclude %{_libdir}/openmpi/lib/*QtPython%{python3_version_nodots}D.so.*
%{_libdir}/openmpi/bin/pvtkpython
%{_libdir}/openmpi/bin/vtkpython
%{_libdir}/openmpi/bin/vtkWrapPython
%{_libdir}/openmpi/bin/vtkWrapPythonInit

%if %{with java}
%files openmpi-java
%{_libdir}/openmpi/lib/*Java.so.*
%{_libdir}/openmpi/lib/vtk.jar
%{_libdir}/openmpi/bin/vtkParseJava
%{_libdir}/openmpi/bin/vtkWrapJava
%endif

%files openmpi-qt
%{_libdir}/openmpi/lib/lib*Qt*.so.*
%exclude %{_libdir}/openmpi/lib/*Python27D.so.*
%{_libdir}/openmpi/lib/qt?/

%files -n python%{python3_pkgversion}-vtk-openmpi-qt
%{_libdir}/openmpi/lib/*QtPython%{python3_version_nodots}D.so.*
%endif

%files data
%{_datadir}/vtkdata

%files testing -f build/testing.list

%files examples -f build/examples.list
%doc vtk-examples/Examples


%changelog
* Thu Nov  5 20:45:48 CET 2020 Sandro Mani <manisandro@gmail.com> - 8.2.0-25
- Rebuild (proj)

* Thu Sep 17 2020 Orion Poplawski <orion@nwra.com> - 8.2.0-24
- Add patch to fix build with Qt 5.15

* Thu Aug 27 2020 Iñaki Úcar <iucar@fedoraproject.org> - 8.2.0-23
- https://fedoraproject.org/wiki/Changes/FlexiBLAS_as_BLAS/LAPACK_manager

* Sun Aug  9 2020 Orion Poplawski <orion@nwra.com> - 8.2.0-22
- Fix ExternalData in vtk-data (bz#1783622)

* Tue Aug  4 2020 Orion Poplawski <orion@nwra.com> - 8.2.0-21
- Use new cmake macros

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 8.2.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 24 2020 Jeff Law <law@redhat.com> - 8.2.0-19
- Use __cmake_in_source_build

* Sat Jul 11 2020 Jiri Vanek <jvanek@redhat.com> - 8.2.0-18
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Thu Jun 25 2020 Orion Poplawski <orion@cora.nwra.com> - 8.2.0-17
- Rebuild for hdf5 1.10.6

* Sat Jun 20 2020 Orion Poplawski <orion@nwra.com> - 8.2.0-16
- Drop _python_bytecompile_extra, python2 conditionals

* Sat May 30 2020 Björn Esser <besser82@fedoraproject.org> - 8.2.0-15
- Rebuild (jsoncpp)

* Wed May 27 2020 Orion Poplawski <orion@nwra.com> - 8.2.0-14
- Add patch to fix building with GCC 10 (bz#1800240)

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 8.2.0-14
- Rebuilt for Python 3.9

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 8.2.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Nov 14 2019 Björn Esser <besser82@fedoraproject.org> - 8.2.0-12
- Rebuild (jsoncpp)

* Sat Nov  9 2019 Orion Poplawski <orion@nwra.com> - 8.2.0-11
- Drop BR on sip-devel (python2)

* Sun Sep 22 2019 Orion Poplawski <orion@nwra.com> - 8.2.0-10
- Rebuild for double-conversion 3.1.5

* Mon Sep 09 2019 Orion Poplawski <orion@nwra.com> - 8.2.0-9
- Rebuild for proj 6.2.0
- Add patch and flags for proj 6 support

* Tue Aug 20 2019 Orion Poplawski <orion@nwra.com> - 8.2.0-8
- Add upstream patch to support Python 3.8

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 8.2.0-7
- Rebuilt for Python 3.8

* Wed Jul 31 2019 Orion Poplawski <orion@nwra.com> - 8.2.0-6
- BR motif-devel instead of /usr/include/Xm (bugz#1731728)

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 8.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 03 2019 Björn Esser <besser82@fedoraproject.org> - 8.2.0-4
- Rebuild (jsoncpp)

* Thu Apr 18 2019 Orion Poplawski <orion@nwra.com> - 8.2.0-3
- Provide starndard python 3.Y dist name (bugz#1700307)

* Tue Apr 16 2019 Orion Poplawski <orion@nwra.com> - 8.2.0-2
- Provide standard python 3 dist name (bugz#1700307)

* Sat Mar 16 2019 Orion Poplawski <orion@nwra.com> - 8.2.0-1
- Update to 8.2.0
- TCL wrapping has been dropped upstream
- Build with system glew

* Fri Feb 15 2019 Orion Poplawski <orion@nwra.com> - 8.1.1-3
- Rebuild for openmpi 3.1.3

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 8.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Oct 26 2018 Orion Poplawski <orion@cora.nwra.com> - 8.1.1-1
- Update to 8.1.1 (bug #1460059)
- Use Qt 5 (bug #1319504)
- Use Python 3 for Fedora 30+ (bug #1549034)

* Thu Sep 06 2018 Pavel Raiskup <praiskup@redhat.com> - 7.1.1-13
- rebuild against libpq (rhbz#1618698, rhbz#1623764)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Mar 07 2018 Adam Williamson <awilliam@redhat.com> - 7.1.1-11
- Rebuild to fix GCC 8 mis-compilation
  See https://da.gd/YJVwk ("GCC 8 ABI change on x86_64")

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Dec 26 2017 Björn Esser <besser82@fedoraproject.org> - 7.1.1-9
- Rebuilt for jsoncpp.so.20

* Mon Dec 18 2017 Orion Poplawski <orion@nwra.com> - 7.1.1-8
- Enable mysql and postgresql support
- Use mariadb BR for F28+ (Bug #1494054)

* Fri Sep 01 2017 Björn Esser <besser82@fedoraproject.org> - 7.1.1-7
- Rebuilt for jsoncpp-1.8.3

* Sat Aug 12 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 7.1.1-6
- Python 2 binary packages renamed to python2-vtk and python2-vtk-qt
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Tue May 9 2017 Orion Poplawski <orion@cora.nwra.com> - 7.1.1-2
- Enable tests on s390x

* Mon May 8 2017 Orion Poplawski <orion@cora.nwra.com> - 7.1.1-1
- Update to 7.1.1

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 3 2017 Dan Horák <dan[at]danny.cz> - 7.1.0-5
- s390x needs increased Java heap size

* Thu Dec 29 2016 Orion Poplawski <orion@cora.nwra.com> - 7.1.0-4
- Drop setting java heap size

* Thu Dec 8 2016 Dan Horák <dan[at]danny.cz> - 7.1.0-3
- Enable openmpi on s390(x)
- Add missing conditions for mpich/openmpi subpackages

* Thu Dec 8 2016 Orion Poplawski <orion@cora.nwra.com> - 7.1.0-2
- Fix MPI library install location

* Mon Dec 5 2016 Orion Poplawski <orion@cora.nwra.com> - 7.1.0-1
- Update to 7.1.0
- Enable OSMesa
- Build MPI versions
- Use bundled glew

* Wed Nov 2 2016 Orion Poplawski <orion@cora.nwra.com> - 6.3.0-12
- Rebuild for R openblas changes

* Mon Oct 03 2016 Björn Esser <fedora@besser82.io> - 6.3.0-11
- Rebuilt for libjsoncpp.so.11

* Thu Jul 28 2016 Than Ngo <than@redhat.com> - 6.3.0-10
- %%check: make non-fatal as temporary workaround for build on s390x

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.3.0-9
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Jun 29 2016 Orion Poplawski <orion@cora.nwra.com> - 6.3.0-8
- Rebuild for hdf5 1.8.17

* Fri Mar 25 2016 Björn Esser <fedora@besser82.io> - 6.3.0-7
- Rebuilt for libjsoncpp.so.1

* Mon Feb 8 2016 Orion Poplawski <orion@cora.nwra.com> - 6.3.0-6
- Add patch for gcc 6 support

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 6.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 22 2016 Orion Poplawski <orion@cora.nwra.com> - 6.3.0-4
- Rebuild for netcdf 4.4.0

* Sat Jan 16 2016 Jonathan Wakely <jwakely@redhat.com> - 6.3.0-3
- Rebuilt for Boost 1.60

* Wed Oct 21 2015 Orion Poplawski <orion@cora.nwra.com> - 6.3.0-2
- Note bundled libraries

* Tue Sep 15 2015 Orion Poplawski <orion@cora.nwra.com> - 6.3.0-1
- Update to 6.3.0

* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 6.2.0-10
- Rebuilt for Boost 1.59

* Fri Aug 21 2015 Orion Poplawski <orion@cora.nwra.com> - 6.2.0-9
- Note bundled kwsys, remove unused kwsys files

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 6.2.0-7
- rebuild for Boost 1.58

* Tue Jul 7 2015 Orion Poplawski <orion@cora.nwra.com> - 6.2.0-6
- Drop glext patch, no longer needed

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 23 2015 Orion Poplawski <orion@cora.nwra.com> - 6.2.0-4
- Add requires netcdf-cxx-devel to vtk-devel (bug #1224512)

* Sun May 17 2015 Orion Poplawski <orion@cora.nwra.com> - 6.2.0-3
- Rebuild for hdf5 1.8.15

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 6.2.0-2
- Rebuilt for GCC 5 C++11 ABI change

* Wed Mar 18 2015 Orion Poplawski <orion@cora.nwra.com> - 6.2.0-1
- Update to 6.2.0
- Remove type, system, install, and netcdf patches applied upstream
- Integrate and replace vtkdata
- Build and run tests again
- Generate testing.list based on executable name

* Thu Mar 05 2015 Orion Poplawski <orion@cora.nwra.com> - 6.1.0-26
- Add needed vtk-*-devel requires to vtk-devel (bug #1199310)

* Wed Mar 04 2015 Orion Poplawski <orion@cora.nwra.com> - 6.1.0-25
- Rebuild for jsoncpp

* Wed Feb 04 2015 Petr Machata <pmachata@redhat.com> - 6.1.0-24
- Bump for rebuild.

* Tue Feb 3 2015 Orion Poplawski <orion@cora.nwra.com> - 6.1.0-23
- Add patch to fix tcl library loading

* Mon Jan 26 2015 Petr Machata <pmachata@redhat.com> - 6.1.0-22
- Rebuild for boost 1.57.0

* Mon Jan 19 2015 François Cami <fcami@fedoraproject.org> - 6.1.0-21
- Switch to non-explicit arch requires for now (bugs #1183210 #1183530)

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
