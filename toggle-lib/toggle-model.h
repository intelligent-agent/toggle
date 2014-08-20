/* Subclass for MashModel. This is really just to 
circumvent the limitations of Cogl introspection, 
so we make the model like we want in C and instrospect that! */
#ifndef __TOGGLE_MODEL_H__
#define __TOGGLE_MODEL_H__

#include <clutter/clutter.h>
#include <mash/mash.h>

GType toggle_model_get_type (void);

/* GObject type macros */
#define TOGGLE_TYPE_MODEL            toggle_model_get_type ()
#define TOGGLE_MODEL(obj)            (G_TYPE_CHECK_INSTANCE_CAST ((obj), TOGGLE_TYPE_MODEL, ToggleModel))
#define TOGGLE_IS_MODEL(obj)         (G_TYPE_CHECK_INSTANCE_TYPE ((obj), TOGGLE_TYPE_MODEL))
#define TOGGLE_MODEL_CLASS(klass)    (G_TYPE_CHECK_CLASS_CAST ((klass), TOGGLE_TYPE_MODEL, ToggleModelClass))
#define TOGGLE_IS_MODEL_CLASS(klass) (G_TYPE_CHECK_CLASS_TYPE ((klass), TOGGLE_TYPE_MODEL))
#define TOGGLE_MODEL_GET_CLASS(obj)  (G_TYPE_INSTANCE_GET_CLASS ((obj), TOGGLE_TYPE_MODEL, ToggleModelClass))

typedef struct _ToggleModelPrivate ToggleModelPrivate;
typedef struct _ToggleModel        ToggleModel;
typedef struct _ToggleModelClass   ToggleModelClass;

/* object structure */
struct _ToggleModel{
    MashModel parent;
  
    /* Private */
    ToggleModelPrivate *priv;
};

/* class structure */
struct _ToggleModelClass{
    MashModelClass parent;
};

/* public API */
ClutterActor *toggle_model_new (void);

ClutterActor *toggle_model_new_from_file (MashDataFlags flags, const gchar *filename, GError **error);
void toggle_model_load_from_file(ToggleModel *self, MashDataFlags flags, const gchar *filename, GError **error);
void toggle_model_set_color (ToggleModel *self, const ClutterColor *color);
#endif /* __TOGGLE_MODEL_H__ */
