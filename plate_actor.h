#ifndef _CLUTTER_PLATE_ACTOR_H
#define _CLUTTER_PLATE_ACTOR_H

#include <glib-object.h>
#include <clutter/clutter.h>

G_BEGIN_DECLS

#define CLUTTER_TYPE_PLATE clutter_plate_get_type()

#define CLUTTER_PLATE(obj) \
  (G_TYPE_CHECK_INSTANCE_CAST ((obj), \
  CLUTTER_TYPE_PLATE, ClutterPlate))

#define CLUTTER_PLATE_CLASS(klass) \
  (G_TYPE_CHECK_CLASS_CAST ((klass), \
  CLUTTER_TYPE_PLATE, ClutterPlateClass))

#define CLUTTER_IS_PLATE(obj) \
  (G_TYPE_CHECK_INSTANCE_TYPE ((obj), \
  CLUTTER_TYPE_PLATE))

#define CLUTTER_IS_PLATE_CLASS(klass) \
  (G_TYPE_CHECK_CLASS_TYPE ((klass), \
  CLUTTER_TYPE_PLATE))

#define CLUTTER_PLATE_GET_CLASS(obj) \
  (G_TYPE_INSTANCE_GET_CLASS ((obj), \
  CLUTTER_TYPE_PLATE, ClutterPlateClass))

typedef struct _ClutterPlate        ClutterPlate;
typedef struct _ClutterPlateClass   ClutterPlateClass;
typedef struct _ClutterPlatePrivate ClutterPlatePrivate;

struct _ClutterPlate
{
  ClutterActor           parent;

  /*< private >*/
  ClutterPlatePrivate *priv;
}; 

struct _ClutterPlateClass 
{
  ClutterActorClass parent_class;
};

GType clutter_plate_get_type (void) G_GNUC_CONST;
ClutterActor *clutter_plate_new (void);

G_END_DECLS

#endif
