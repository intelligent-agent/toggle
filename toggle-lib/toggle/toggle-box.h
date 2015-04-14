#ifndef _TOGGLE_BOX_H
#define _TOGGLE_BOX_H

#include <glib-object.h>
#include <clutter/clutter.h>

G_BEGIN_DECLS

GType toggle_box_get_type (void);

#define TOGGLE_TYPE_BOX toggle_box_get_type()

#define TOGGLE_BOX(obj) \
  (G_TYPE_CHECK_INSTANCE_CAST ((obj), \
  TOGGLE_TYPE_BOX, ToggleBox))

#define TOGGLE_BOX_CLASS(klass) \
  (G_TYPE_CHECK_CLASS_CAST ((klass), \
  TOGGLE_TYPE_BOX, ToggleBoxClass))

#define TOGGLE_IS_BOX(obj) \
  (G_TYPE_CHECK_INSTANCE_TYPE ((obj), \
  TOGGLE_TYPE_BOX))

#define TOGGLE_IS_BOX_CLASS(klass) \
  (G_TYPE_CHECK_CLASS_TYPE ((klass), \
  TOGGLE_TYPE_BOX))

#define TOGGLE_BOX_GET_CLASS(obj) \
  (G_TYPE_INSTANCE_GET_CLASS ((obj), \
  TOGGLE_TYPE_BOX, ToggleBoxClass))

typedef struct _ToggleBox        ToggleBox;
typedef struct _ToggleBoxClass   ToggleBoxClass;
typedef struct _ToggleBoxPrivate ToggleBoxPrivate;

struct _ToggleBox
{
  ClutterActor           parent;

  /*< private >*/
  ToggleBoxPrivate *priv;
};

struct _ToggleBoxClass
{
  ClutterActorClass parent_class;
};

ClutterActor *toggle_box_new ();

G_END_DECLS

#endif

