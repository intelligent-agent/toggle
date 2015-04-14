#include "toggle-box.h"

#include <cogl/cogl.h>
#include <string.h>

/**
* SECTION: toggle-box
* @short_description: A 3d stage.
*
* The #ToggleBox is a class to display a 3D stage.
*/
G_DEFINE_TYPE (ToggleBox, toggle_box, CLUTTER_TYPE_ACTOR);

#define TOGGLE_BOX_GET_PRIVATE(obj) (G_TYPE_INSTANCE_GET_PRIVATE ((obj), TOGGLE_TYPE_BOX, ToggleBoxPrivate))

struct _ToggleBoxPrivate{
    CoglPipeline    *pipeline;
    CoglFramebuffer *fb;
    CoglPrimitive   *prim;    
    CoglTexture     *texture;
    ClutterColor    *color;
};


gboolean
toggle_button_press (ClutterActor *origin,
                 ClutterEvent *event,
                 ClutterActor *rect){

    float x, y;    
    clutter_event_get_coords(event, &x, &y);
    fprintf(stderr, "Box pressed @ (%f, %f)\n", x, y);
    clutter_event_set_coords(event, y, x);
    return CLUTTER_EVENT_PROPAGATE;
}

static void
toggle_box_finalize (GObject *object){
  G_OBJECT_CLASS (toggle_box_parent_class)->finalize (object);
}

static void
toggle_box_dispose (GObject *object){
  G_OBJECT_CLASS (toggle_box_parent_class)->dispose (object);
}

static void
toggle_box_class_init (ToggleBoxClass *klass){
    GObjectClass      *gobject_class = G_OBJECT_CLASS (klass);
    ClutterActorClass *actor_class = CLUTTER_ACTOR_CLASS (klass);

    actor_class->button_press_event = toggle_button_press;

    gobject_class->finalize     = toggle_box_finalize;
    gobject_class->dispose      = toggle_box_dispose;

  //g_type_class_add_private (gobject_class, sizeof (ToggleBoxPrivate));
}

static void
toggle_box_init (ToggleBox *self){

    g_signal_connect_swapped (self, "paint",
                            G_CALLBACK (cogl_set_depth_test_enabled),
                            GINT_TO_POINTER (TRUE));
    g_signal_connect_data (self, "paint",
                         G_CALLBACK (cogl_set_depth_test_enabled),
                         GINT_TO_POINTER (FALSE), NULL,
                         G_CONNECT_AFTER | G_CONNECT_SWAPPED);
}

/**
* clutter_box_new:
*
* Allocates a new #ToggleBox.
*
* Return value: a new #ToggleBox.
*/
ClutterActor*
toggle_box_new (){
    return g_object_new (TOGGLE_TYPE_BOX, NULL);
}



