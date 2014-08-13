#ifndef _TOGGLE_PLATE_H
#define _TOGGLE_PLATE_H

#include <glib-object.h>
#include <clutter/clutter.h>

G_BEGIN_DECLS

#define TOGGLE_TYPE_PLATE toggle_plate_get_type()

#define TOGGLE_PLATE(obj) \
  (G_TYPE_CHECK_INSTANCE_CAST ((obj), \
  TOGGLE_TYPE_PLATE, TogglePlate))

#define TOGGLE_PLATE_CLASS(klass) \
  (G_TYPE_CHECK_CLASS_CAST ((klass), \
  TOGGLE_TYPE_PLATE, TogglePlateClass))

#define TOGGLE_IS_PLATE(obj) \
  (G_TYPE_CHECK_INSTANCE_TYPE ((obj), \
  TOGGLE_TYPE_PLATE))

#define TOGGLE_IS_PLATE_CLASS(klass) \
  (G_TYPE_CHECK_CLASS_TYPE ((klass), \
  TOGGLE_TYPE_PLATE))

#define TOGGLE_PLATE_GET_CLASS(obj) \
  (G_TYPE_INSTANCE_GET_CLASS ((obj), \
  TOGGLE_TYPE_PLATE, TogglePlateClass))

typedef struct _TogglePlate        TogglePlate;
typedef struct _TogglePlateClass   TogglePlateClass;
typedef struct _TogglePlatePrivate TogglePlatePrivate;

struct _TogglePlate
{
  ClutterActor           parent;

  /*< private >*/
  TogglePlatePrivate *priv;
};

struct _TogglePlateClass
{
  ClutterActorClass parent_class;
};

GType toggle_plate_get_type (void) G_GNUC_CONST;
ClutterActor *toggle_plate_new ();

G_END_DECLS

#endif
