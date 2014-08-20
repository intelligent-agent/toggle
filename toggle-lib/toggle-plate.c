#include "toggle-plate.h"

#include <cogl/cogl.h>
#include <string.h>

/**
* SECTION: toggle-plate
* @short_description: A 3d stage.
*
* The #TogglePlate is a class to display a 3D stage.
*/
G_DEFINE_TYPE (TogglePlate, toggle_plate, CLUTTER_TYPE_ACTOR);

#define TOGGLE_PLATE_GET_PRIVATE(obj) (G_TYPE_INSTANCE_GET_PRIVATE ((obj), TOGGLE_TYPE_PLATE, TogglePlatePrivate))

struct _TogglePlatePrivate{
    CoglPipeline    *pipeline;
    CoglFramebuffer *fb;
    CoglPrimitive   *prim;    
    CoglTexture     *texture;
    ClutterColor    *color;

    CoglMatrix matrix;
    int width; 
    int height; 

};

enum
{
  PROP_0, 
  PROP_MATRIX, 
  N_PROPERTIES
};

static GParamSpec *obj_properties[N_PROPERTIES] = { NULL, };

static CoglVertexP3T2 vertices[] =
{
  /* Front face */
  { /* pos = */  0.0f,  0.0f,  1.0f, /* tex coords = */ 0.0f, 1.0f},
  { /* pos = */  1.0f,  0.0f,  1.0f, /* tex coords = */ 1.0f, 1.0f},
  { /* pos = */  1.0f,  1.0f,  1.0f, /* tex coords = */ 1.0f, 0.0f},
  { /* pos = */  0.0f,  1.0f,  1.0f, /* tex coords = */ 0.0f, 0.0f},
  { /* pos = */  0.0f,  0.0f,  1.0f, /* tex coords = */ 0.0f, 1.0f},

  /* Back face */
  { /* pos = */  0.0f,  0.0f,  0.0f, /* tex coords = */ 1.0f, 0.0f},
  { /* pos = */  0.0f,  1.0f,  0.0f, /* tex coords = */ 1.0f, 1.0f},
  { /* pos = */  1.0f,  1.0f,  0.0f, /* tex coords = */ 0.0f, 1.0f},
  { /* pos = */  1.0f,  0.0f,  0.0f, /* tex coords = */ 0.0f, 0.0f},
  { /* pos = */  0.0f,  0.0f,  0.0f, /* tex coords = */ 1.0f, 0.0f},

  /* Top face */
  { /* pos = */  0.0f,  1.0f,  0.0f, /* tex coords = */ 0.0f, 1.0f},
  { /* pos = */  0.0f,  1.0f,  1.0f, /* tex coords = */ 0.0f, 0.0f},
  { /* pos = */  1.0f,  1.0f,  1.0f, /* tex coords = */ 1.0f, 0.0f},
  { /* pos = */  1.0f,  1.0f,  0.0f, /* tex coords = */ 1.0f, 1.0f},
  { /* pos = */  0.0f,  1.0f,  0.0f, /* tex coords = */ 0.0f, 1.0f},

  /* Bottom face */
  { /* pos = */  0.0f,  0.0f,  0.0f, /* tex coords = */ 1.0f, 1.0f},
  { /* pos = */  1.0f,  0.0f,  0.0f, /* tex coords = */ 0.0f, 1.0f},
  { /* pos = */  1.0f,  0.0f,  1.0f, /* tex coords = */ 0.0f, 0.0f},
  { /* pos = */  0.0f,  0.0f,  1.0f, /* tex coords = */ 1.0f, 0.0f},
  { /* pos = */  0.0f,  0.0f,  0.0f, /* tex coords = */ 1.0f, 1.0f},

  /* Bottom grid */
  { /* pos = */   0.0f,  0.0f, 0.25f, /* tex coords = */ 0.0f, 1.0f},
  { /* pos = */   1.0f,  0.0f, 0.25f, /* tex coords = */ 0.0f, 1.0f},
  { /* pos = */   0.0f,  0.0f,  0.0f, /* tex coords = */ 0.0f, 1.0f},
  { /* pos = */   1.0f,  0.0f,  0.0f, /* tex coords = */ 0.0f, 1.0f},
  { /* pos = */   0.0f,  0.0f,  0.75f, /* tex coords = */ 0.0f, 1.0f},
  { /* pos = */   1.0f,  0.0f,  0.75f, /* tex coords = */ 0.0f, 1.0f},

  { /* pos = */   0.75f,  0.0f,  0.0f, /* tex coords = */ 0.0f, 1.0f},
  { /* pos = */   0.75f,  0.0f,  1.0f, /* tex coords = */ 0.0f, 0.0f},
  { /* pos = */   0.0f,  0.0f,  0.0f, /* tex coords = */ 0.0f, 1.0f},
  { /* pos = */   0.0f,  0.0f,  1.0f, /* tex coords = */ 0.0f, 0.0f},
  { /* pos = */  0.25f,  0.0f,  0.0f, /* tex coords = */ 0.0f, 1.0f},
  { /* pos = */  0.25f,  0.0f,  1.0f, /* tex coords = */ 0.0f, 0.0f},

  /* Right face */
  { /* pos = */ 1.0f,  0.0f,  0.0f, /* tex coords = */ 1.0f, 0.0f},
  { /* pos = */ 1.0f,  1.0f,  0.0f, /* tex coords = */ 1.0f, 1.0f},
  { /* pos = */ 1.0f,  1.0f,  1.0f, /* tex coords = */ 0.0f, 1.0f},
  { /* pos = */ 1.0f,  0.0f,  1.0f, /* tex coords = */ 0.0f, 0.0f},
  { /* pos = */ 1.0f,  0.0f,  0.0f, /* tex coords = */ 1.0f, 0.0f},

  /* Left face */
  { /* pos = */  0.0f,  0.0f,  0.0f, /* tex coords = */ 0.0f, 0.0f},
  { /* pos = */  0.0f,  0.0f,  1.0f, /* tex coords = */ 1.0f, 0.0f},
  { /* pos = */  0.0f,  1.0f,  1.0f, /* tex coords = */ 1.0f, 1.0f},
  { /* pos = */  0.0f,  1.0f,  0.0f, /* tex coords = */ 0.0f, 1.0f},
  { /* pos = */  0.0f,  0.0f,  0.0f, /* tex coords = */ 0.0f, 0.0f}
};

static void
my_actor_paint_node (ClutterActor     *actor,
                     ClutterPaintNode *root){
    ClutterPaintNode    *node;
    ClutterActorBox     box;
    TogglePlate        *plate;
    TogglePlatePrivate *priv;
    CoglMatrix          transform;

    CoglFramebuffer     *screen; 
    screen = (CoglFramebuffer *) cogl_get_draw_framebuffer ();
    
    plate = TOGGLE_PLATE(actor);
    priv = plate->priv;

    node = clutter_color_node_new(priv->color);
    clutter_paint_node_add_primitive(node, priv->prim);

    /* add the node, and transfer ownership */
    clutter_paint_node_add_child (root, node);
    clutter_paint_node_unref (node);
}


static void
toggle_plate_finalize (GObject *object)
{
  G_OBJECT_CLASS (toggle_plate_parent_class)->finalize (object);
}

static void
toggle_plate_dispose (GObject *object)
{
  G_OBJECT_CLASS (toggle_plate_parent_class)->dispose (object);
}


/* enables objects to be uniformly treated as GObjects;
 * also exposes properties so they become scriptable, e.g.
 * through ClutterScript
 */
static void
toggle_plate_set_property (GObject      *gobject,
                        guint         prop_id,
                        const GValue *value,
                        GParamSpec   *pspec)
{
  TogglePlate *plate = TOGGLE_PLATE (gobject);

  switch (prop_id)
    {
    case PROP_MATRIX:
      //TODO
      break;

    default:
      G_OBJECT_WARN_INVALID_PROPERTY_ID (gobject, prop_id, pspec);
      break;
    }
}

/* enables objects to be uniformly treated as GObjects */
static void
toggle_plate_get_property (GObject    *gobject,
                        guint       prop_id,
                        GValue     *value,
                        GParamSpec *pspec)
{
  TogglePlatePrivate *priv = TOGGLE_PLATE (gobject)->priv;

  switch (prop_id)
    {
    case PROP_MATRIX:
     //TODO
      break;

    default:
      G_OBJECT_WARN_INVALID_PROPERTY_ID (gobject, prop_id, pspec);
      break;
    }
}


static void
toggle_plate_class_init (TogglePlateClass *klass)
{
  GObjectClass      *gobject_class = G_OBJECT_CLASS (klass);
  ClutterActorClass *actor_class = CLUTTER_ACTOR_CLASS (klass);

  /* Provide implementations for ClutterActor vfuncs: */
  actor_class->paint_node = my_actor_paint_node;

  gobject_class->finalize     = toggle_plate_finalize;
  gobject_class->dispose      = toggle_plate_dispose;
  gobject_class->set_property = toggle_plate_set_property;
  gobject_class->get_property = toggle_plate_get_property;

  /*
   * TogglePlate:cogl-matrix:
   *
   * The CoglMatrix of the plate.
   */
  g_object_class_install_property (gobject_class,
                                   PROP_MATRIX,
                                   g_param_spec_boxed ("matrix",
                                                       "Matrix",
                                                       "The CoglMatrix of the plate",
                                                       CLUTTER_TYPE_MATRIX,
                                                       G_PARAM_READABLE | G_PARAM_WRITABLE));

  g_type_class_add_private (gobject_class, sizeof (TogglePlatePrivate));
}

static void
toggle_plate_init (TogglePlate *self){
    TogglePlatePrivate *priv;
    ClutterBackend      *be         = clutter_get_default_backend ();
    CoglContext         *ctx        = (CoglContext*) clutter_backend_get_cogl_context (be);
    CoglOffscreen       *offscreen;
    CoglMatrix          view;
    int width, height;
    float fovy, aspect, z_near, z_2d, z_far;


    self->priv       = priv = TOGGLE_PLATE_GET_PRIVATE (self);
    priv->pipeline   = cogl_pipeline_new(ctx);

    self->priv->color = CLUTTER_COLOR_Red;

    priv->width = width = 400;
    priv->height = height = 400;

    // Initialize the plate primitive 
    priv->prim = cogl_primitive_new_p3t2 (ctx, COGL_VERTICES_MODE_LINES,
                                       G_N_ELEMENTS (vertices),
                                       vertices);
}

/**
* clutter_plate_new:
*
* Allocates a new #TogglePlate.
*
* Return value: a new #TogglePlate.
*/
ClutterActor*
toggle_plate_new (){
    return g_object_new (TOGGLE_TYPE_PLATE, NULL);
}

/**
 * toggle_plate_set_color:
 * @self: a #TogglePlate
 * @color: the #ClutterColor to use as the color for the button text
 *
 * Set the color of the text on the button
 */
void
toggle_plate_set_color (TogglePlate *self, const ClutterColor *color){
    g_return_if_fail (TOGGLE_IS_PLATE (self));
    self->priv->color = color;
}


