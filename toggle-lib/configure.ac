dnl The version system for Mash has a major, minor and micro version
dnl number. The ABI and API is stable only between micro version
dnl numbers (although this will likely change if Mash ever makes a
dnl 1.0.0 release). The micro is odd numbered between releases. Only
dnl on the commit that contains a release should it be an even number.

m4_define([toggle_major_version], [0])
m4_define([toggle_minor_version], [4])
m4_define([toggle_micro_version], [0])
m4_define([toggle_version],
          [toggle_major_version.toggle_minor_version.toggle_micro_version])

dnl The major and minor currently number define the API version so
dnl these become part of the library name.

m4_define([toggle_api_version], [toggle_major_version.toggle_minor_version])

dnl The interface version is managed manually, separately from the
dnl public package version number. The numbers here are modified
dnl according to the guidelines set out in the libtool manual. This is
dnl different from the semi-automatic usage implemented in Gtk and
dnl Clutter. I did this because I was convinced by the reasoning in
dnl the UProf configure script. The 'current' age here will
dnl effectively always be zero because whenever Mash breaks API it
dnl will change the library name so it's effectively a completely
dnl different library.

m4_define([toggle_lt_current], 0)
m4_define([toggle_lt_revision], 0)
m4_define([toggle_lt_age], 0)

AC_INIT([toggle], [toggle_version])

dnl AC_CONFIG_SRCDIR([toggle.h])
AC_CONFIG_HEADER([config.h])
AC_CONFIG_MACRO_DIR([m4])

AM_INIT_AUTOMAKE([1.9])

m4_ifdef([AM_SILENT_RULES], [AM_SILENT_RULES([yes])])

AC_PROG_LIBTOOL

dnl Version number variables for the Makefiles
TOGGLE_MAJOR_VERSION=toggle_major_version
TOGGLE_MINOR_VERSION=toggle_minor_version
TOGGLE_MICRO_VERSION=toggle_micro_version
TOGGLE_VERSION=toggle_version
TOGGLE_API_VERSION=toggle_api_version
AC_SUBST(TOGGLE_MAJOR_VERSION)
AC_SUBST(TOGGLE_MINOR_VERSION)
AC_SUBST(TOGGLE_MICRO_VERSION)
AC_SUBST(TOGGLE_VERSION)
AC_SUBST(TOGGLE_API_VERSION)

TOGGLE_LT_CURRENT=toggle_lt_current
TOGGLE_LT_REVISION=toggle_lt_revision
TOGGLE_LT_AGE=toggle_lt_age
AC_SUBST(TOGGLE_LT_CURRENT)
AC_SUBST(TOGGLE_LT_REVISION)
AC_SUBST(TOGGLE_LT_AGE)

dnl Check if we need to link to -lm
AC_SEARCH_LIBS([atan2f], [m], [have_atan2f=yes], [have_atan2f=no])
AS_IF([test "x$have_atan2f" = "xno"],
      AC_MSG_ERROR([Could not find math library]))

PKG_PROG_PKG_CONFIG

PKG_CHECK_MODULES(GLIB, [glib-2.0 >= 2.16 gobject-2.0 >= 2.16])
PKG_CHECK_MODULES(CLUTTER, [clutter-1.0 >= 1.5.10])
PKG_CHECK_MODULES(MX, [mx-1.0 >= 1.1.0])
PKG_CHECK_MODULES(MASH, [mash-0.2 >= 0.2.1])

AC_SUBST([MASH_CFLAGS])
AC_SUBST([MASH_LIBS])

GOBJECT_INTROSPECTION_CHECK([0.6.1])

AC_PATH_PROG([GLIB_MKENUMS], [glib-mkenums])

AC_CONFIG_FILES([
        Makefile
        toggle/Makefile
        toggle-$TOGGLE_API_VERSION.pc:toggle.pc.in
])

AC_OUTPUT
