#include "plate_actor.h"

#include <cogl/cogl.h>
#include <string.h>

G_DEFINE_TYPE (ClutterPlate, clutter_plate, CLUTTER_TYPE_ACTOR);

enum
{
  PROP_0, 
  PROP_MATRIX
};

static CoglVertexP3T2 vertices[] =
{
  /* Front face */
  { /* pos = */ -1.0f, -1.0f,  1.0f, /* tex coords = */ 0.0f, 1.0f},
  { /* pos = */  1.0f, -1.0f,  1.0f, /* tex coords = */ 1.0f, 1.0f},
  { /* pos = */  1.0f,  1.0f,  1.0f, /* tex coords = */ 1.0f, 0.0f},
  { /* pos = */ -1.0f,  1.0f,  1.0f, /* tex coords = */ 0.0f, 0.0f},
  { /* pos = */ -1.0f, -1.0f,  1.0f, /* tex coords = */ 0.0f, 1.0f},

  /* Back face */
  { /* pos = */ -1.0f, -1.0f, -1.0f, /* tex coords = */ 1.0f, 0.0f},
  { /* pos = */ -1.0f,  1.0f, -1.0f, /* tex coords = */ 1.0f, 1.0f},
  { /* pos = */  1.0f,  1.0f, -1.0f, /* tex coords = */ 0.0f, 1.0f},
  { /* pos = */  1.0f, -1.0f, -1.0f, /* tex coords = */ 0.0f, 0.0f},
  { /* pos = */ -1.0f, -1.0f, -1.0f, /* tex coords = */ 1.0f, 0.0f},

  /* Top face */
  { /* pos = */ -1.0f,  1.0f, -1.0f, /* tex coords = */ 0.0f, 1.0f},
  { /* pos = */ -1.0f,  1.0f,  1.0f, /* tex coords = */ 0.0f, 0.0f},
  { /* pos = */  1.0f,  1.0f,  1.0f, /* tex coords = */ 1.0f, 0.0f},
  { /* pos = */  1.0f,  1.0f, -1.0f, /* tex coords = */ 1.0f, 1.0f},
  { /* pos = */ -1.0f,  1.0f, -1.0f, /* tex coords = */ 0.0f, 1.0f},

  /* Bottom face */
  { /* pos = */ -1.0f, -1.0f, -1.0f, /* tex coords = */ 1.0f, 1.0f},
  { /* pos = */  1.0f, -1.0f, -1.0f, /* tex coords = */ 0.0f, 1.0f},
  { /* pos = */  1.0f, -1.0f,  1.0f, /* tex coords = */ 0.0f, 0.0f},
  { /* pos = */ -1.0f, -1.0f,  1.0f, /* tex coords = */ 1.0f, 0.0f},
  { /* pos = */ -1.0f, -1.0f, -1.0f, /* tex coords = */ 1.0f, 1.0f},

  /* Bottom grid */
  { /* pos = */  -1.0f, -1.0f, -0.5f, /* tex coords = */ 0.0f, 1.0f},
  { /* pos = */   1.0f, -1.0f, -0.5f, /* tex coords = */ 0.0f, 1.0f},
  { /* pos = */  -1.0f, -1.0f,  0.0f, /* tex coords = */ 0.0f, 1.0f},
  { /* pos = */   1.0f, -1.0f,  0.0f, /* tex coords = */ 0.0f, 1.0f},
  { /* pos = */  -1.0f, -1.0f,  0.5f, /* tex coords = */ 0.0f, 1.0f},
  { /* pos = */   1.0f, -1.0f,  0.5f, /* tex coords = */ 0.0f, 1.0f},

  { /* pos = */   0.5f, -1.0f, -1.0f, /* tex coords = */ 0.0f, 1.0f},
  { /* pos = */   0.5f, -1.0f,  1.0f, /* tex coords = */ 0.0f, 0.0f},
  { /* pos = */   0.0f, -1.0f, -1.0f, /* tex coords = */ 0.0f, 1.0f},
  { /* pos = */   0.0f, -1.0f,  1.0f, /* tex coords = */ 0.0f, 0.0f},
  { /* pos = */  -0.5f, -1.0f, -1.0f, /* tex coords = */ 0.0f, 1.0f},
  { /* pos = */  -0.5f, -1.0f,  1.0f, /* tex coords = */ 0.0f, 0.0f},

  /* Right face */
  { /* pos = */ 1.0f, -1.0f, -1.0f, /* tex coords = */ 1.0f, 0.0f},
  { /* pos = */ 1.0f,  1.0f, -1.0f, /* tex coords = */ 1.0f, 1.0f},
  { /* pos = */ 1.0f,  1.0f,  1.0f, /* tex coords = */ 0.0f, 1.0f},
  { /* pos = */ 1.0f, -1.0f,  1.0f, /* tex coords = */ 0.0f, 0.0f},
  { /* pos = */ 1.0f, -1.0f, -1.0f, /* tex coords = */ 1.0f, 0.0f},

  /* Left face */
  { /* pos = */ -1.0f, -1.0f, -1.0f, /* tex coords = */ 0.0f, 0.0f},
  { /* pos = */ -1.0f, -1.0f,  1.0f, /* tex coords = */ 1.0f, 0.0f},
  { /* pos = */ -1.0f,  1.0f,  1.0f, /* tex coords = */ 1.0f, 1.0f},
  { /* pos = */ -1.0f,  1.0f, -1.0f, /* tex coords = */ 0.0f, 1.0f},
  { /* pos = */ -1.0f, -1.0f, -1.0f, /* tex coords = */ 0.0f, 0.0f}
};


#define CLUTTER_PLATE_GET_PRIVATE(obj) \
(G_TYPE_INSTANCE_GET_PRIVATE ((obj), CLUTTER_TYPE_PLATE, ClutterPlatePrivate))

struct _ClutterPlatePrivate{
    CoglPipeline    *pipeline;
    CoglFramebuffer *fb;
    CoglPrimitive   *prim;    
    CoglTexture     *texture;

    CoglMatrix matrix;
    int width; 
    int height; 

};

static void
my_actor_paint_node (ClutterActor     *actor,
                     ClutterPaintNode *root){
    ClutterPaintNode    *node;
    ClutterActorBox     box;
    ClutterPlate        *plate;
    ClutterPlatePrivate *priv;
    CoglMatrix                  transform;

    CoglFramebuffer     *screen; 
    screen = cogl_get_draw_framebuffer ();
    
    plate = CLUTTER_PLATE(actor);
    priv = plate->priv;

    node = clutter_color_node_new(CLUTTER_COLOR_White);

    clutter_paint_node_add_primitive(node, priv->prim);

    /* add the node, and transfer ownership */
    clutter_paint_node_add_child (root, node);
    clutter_paint_node_unref (node);
}

static void
clutter_plate_set_property (GObject      *object,
				guint         prop_id,
				const GValue *value,
				GParamSpec   *pspec)
{
  ClutterPlate *plate = CLUTTER_PLATE(object);

  switch (prop_id)
    {
    case PROP_MATRIX:
      clutter_plate_set_matrix (plate, g_value_get_boxed (value));
      break;
    default:
      G_OBJECT_WARN_INVALID_PROPERTY_ID (object, prop_id, pspec);
      break;
  }
}

static void
clutter_plate_get_property (GObject    *object,
				guint       prop_id,
				GValue     *value,
				GParamSpec *pspec)
{
  ClutterPlate *plate = CLUTTER_PLATE(object);
  ClutterMatrix     matrix;

  switch (prop_id)
    {
    case PROP_MATRIX:
      clutter_plate_get_matrix (plate, &matrix);
      g_value_set_boxed (value, &matrix);
      break;
    default:
      G_OBJECT_WARN_INVALID_PROPERTY_ID (object, prop_id, pspec);
      break;
    }
}


static void
clutter_plate_finalize (GObject *object)
{
  G_OBJECT_CLASS (clutter_plate_parent_class)->finalize (object);
}

static void
clutter_plate_dispose (GObject *object)
{
  G_OBJECT_CLASS (clutter_plate_parent_class)->dispose (object);
}


static void
clutter_plate_class_init (ClutterPlateClass *klass)
{
  GObjectClass        *gobject_class = G_OBJECT_CLASS (klass);
  ClutterActorClass *actor_class = CLUTTER_ACTOR_CLASS (klass);

  /* Provide implementations for ClutterActor vfuncs: */
  actor_class->paint_node = my_actor_paint_node;

  gobject_class->finalize     = clutter_plate_finalize;
  gobject_class->dispose      = clutter_plate_dispose;
  gobject_class->set_property = clutter_plate_set_property;
  gobject_class->get_property = clutter_plate_get_property;

  /**
   * ClutterPlate:cogl-matrix:
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

  g_type_class_add_private (gobject_class, sizeof (ClutterPlatePrivate));
}

static void
clutter_plate_init (ClutterPlate *self){
    ClutterPlatePrivate *priv;
    ClutterBackend      *be         = clutter_get_default_backend ();
    CoglContext         *ctx        = (CoglContext*) clutter_backend_get_cogl_context (be);
    CoglOffscreen       *offscreen;
    CoglMatrix          view;
    int width, height;
    float fovy, aspect, z_near, z_2d, z_far;


    self->priv       = priv = CLUTTER_PLATE_GET_PRIVATE (self);
    priv->pipeline   = cogl_pipeline_new(ctx);

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
 * Creates a new #ClutterActor with a rectangular shape.
 *
 * Return value: a new #ClutterActor
 */
ClutterActor*
clutter_plate_new (void){
  return g_object_new (CLUTTER_TYPE_PLATE, NULL);
}

