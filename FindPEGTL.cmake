# - Try to find PEGTL lib
#
# This module supports requiring a minimum version, e.g. you can do
#   find_package(PEGTL 3.1.2)
# to require version 3.1.2 or newer of PEGTL.
#
# Once done this will define
#
#  PEGTL_FOUND - system has eigen lib with correct version
#  PEGTL_INCLUDE_DIR - the eigen include directory
#  PEGTL_VERSION - eigen version

# Copyright (c) 2006, 2007 Montel Laurent, <montel@kde.org>
# Copyright (c) 2008, 2009 Gael Guennebaud, <g.gael@free.fr>
# Copyright (c) 2009 Benoit Jacob <jacob.benoit.1@gmail.com>
# Redistribution and use is allowed according to the terms of the 2-clause BSD license.

if(NOT PEGTL_FIND_VERSION)
  if(NOT PEGTL_FIND_VERSION_MAJOR)
    set(PEGTL_FIND_VERSION_MAJOR 2)
  endif()
  if(NOT PEGTL_FIND_VERSION_MINOR)
    set(PEGTL_FIND_VERSION_MINOR 4)
  endif()
  if(NOT PEGTL_FIND_VERSION_PATCH)
    set(PEGTL_FIND_VERSION_PATCH 0)
  endif()

  set(PEGTL_FIND_VERSION "${PEGTL_FIND_VERSION_MAJOR}.${PEGTL_FIND_VERSION_MINOR}.${PEGTL_FIND_VERSION_PATCH}")
endif()

macro(_pegtl_check_version)
  file(READ "${PEGTL_INCLUDE_DIR}/tao/pegtl/version.hpp" _pegtl_version_header)
  string(REGEX MATCH "define[ \t]+TAO_PEGTL_VERSION[ \t]+\"([0-9.]+)\"" _pegtl_version_match "${_pegtl_version_header}")
  set(PEGTL_VERSION ${CMAKE_MATCH_1})
  if(${PEGTL_VERSION} VERSION_LESS ${PEGTL_FIND_VERSION})
    set(PEGTL_VERSION_OK FALSE)
  else()
    set(PEGTL_VERSION_OK TRUE)
  endif()

  if(NOT PEGTL_VERSION_OK)
    message(STATUS "PEGTL version ${PEGTL_VERSION} found in ${PEGTL_INCLUDE_DIR}, "
                   "but at least version ${PEGTL_FIND_VERSION} is required")
  endif()
endmacro()

if (PEGTL_INCLUDE_DIR)
  # in cache already
  _pegtl_check_version()
  set(PEGTL_FOUND ${PEGTL_VERSION_OK})
else ()
  find_path(PEGTL_INCLUDE_DIR NAMES tao
      PATHS
      ${CMAKE_INSTALL_PREFIX}/include
    )

  if(PEGTL_INCLUDE_DIR)
    _pegtl_check_version()
  endif()

  include(FindPackageHandleStandardArgs)
  find_package_handle_standard_args(PEGTL DEFAULT_MSG PEGTL_INCLUDE_DIR PEGTL_VERSION_OK)

  mark_as_advanced(PEGTL_INCLUDE_DIR)
endif()
