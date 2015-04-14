lib_LTLIBRARIES = libtoggle-@TOGGLE_API_VERSION@.la

INCLUDES = \
	-I$(top_srcdir)

AM_CPPFLAGS = \
	-DTOGGLE_COMPILATION=1 \
	@CLUTTER_CFLAGS@ \
	@MASH_CFLAGS@

source_h = \
	$(srcdir)/toggle-box.h \
	$(srcdir)/toggle-model.h

libtoggle_@TOGGLE_API_VERSION@_la_SOURCES = \
	$(source_h) \
	$(srcdir)/toggle-box.c \
	$(srcdir)/toggle-model.c

nodist_libtoggle_@TOGGLE_API_VERSION@_la_SOURCES =


toggledir = $(includedir)/toggle-@TOGGLE_API_VERSION@/toggle

toggle_HEADERS = 

nodist_toggle_HEADERS = 

libtoggle_@TOGGLE_API_VERSION@_la_LDFLAGS = \
	-version-info "@TOGGLE_LT_CURRENT@:@TOGGLE_LT_REVISION@:@TOGGLE_LT_AGE@"

libtoggle_@TOGGLE_API_VERSION@_la_LIBADD = \
	@CLUTTER_LIBS@ \
	@MASH_LIBS@

CLEANFILES =

BUILT_GIRSOURCES =

if HAVE_INTROSPECTION

Toggle-@TOGGLE_API_VERSION@.gir: $(INTROSPECTION_SCANNER) libtoggle-@TOGGLE_API_VERSION@.la
	$(QUIET_GEN)$(INTROSPECTION_SCANNER) -v \
		--namespace Toggle \
		--nsversion=@TOGGLE_API_VERSION@ \
		$(INCLUDES) \
		-L`pwd`/.libs\
		$(AM_CPPFLAGS) \
		$(json_gir_include_path) \
		--c-include='toggle/toggle.h' \
		--include=Clutter-1.0 \
		--output $@ \
		--library=toggle-@TOGGLE_API_VERSION@ \
		$(libtoggle_@TOGGLE_API_VERSION@_la_SOURCES)

BUILT_GIRSOURCES += Toggle-@TOGGLE_API_VERSION@.gir

# INTROSPECTION_GIRDIR/INTROSPECTION_TYPELIBDIR aren't the right place to
# install anything - we need to install inside our prefix.
girdir = $(datadir)/gir-1.0
gir_DATA = $(BUILT_GIRSOURCES)

typelibsdir = $(libdir)/girepository-1.0/

typelibs_DATA = $(BUILT_GIRSOURCES:.gir=.typelib)

.gir.typelib : %.typelib: $(INTROSPECTION_COMPILER)
	$(QUIET_GEN) \
	LD_LIBRARY_PATH=.libs$${LD_LIBRARY_PATH:+:$$LD_LIBRARY_PATH} \
	$(INTROSPECTION_COMPILER) \
		--includedir=$(srcdir) \
		--includedir=. \
		$(INTROSPECTION_COMPILER_OPTS) $< -o $(@F)

CLEANFILES += $(BUILT_GIRSOURCES) $(typelibs_DATA)

endif # HAVE_INTROSPECTION

# These need to be defined before we can include the glib Makefiles
# below
DISTCLEANFILES =
BUILT_SOURCES =
EXTRA_DIST =


