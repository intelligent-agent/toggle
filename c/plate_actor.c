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
    // Make a new blank texture
    //priv->texture = cogl_texture_new_with_size (width, height,
    //                                             COGL_TEXTURE_NONE,
    //                                             COGL_PIXEL_FORMAT_RGB_888);

    // Init the Offscreen buffer from the texture
    //offscreen = cogl_offscreen_new_with_texture (priv->texture);
    //priv->fb = COGL_FRAMEBUFFER (offscreen);
    
    //cogl_framebuffer_set_viewport (priv->fb,
    //                             0, 0,
    //                             width,
    //                             height);

    //fovy = 60; /* y-axis field of view */
    //aspect = width/height;
    //z_near = 0.1; /* distance to near clipping plane */
    //z_2d = 1000; /* position to 2d plane */
    //z_far = 2000; /* distance to far clipping plane */

    /*
    cogl_framebuffer_perspective (priv->fb, fovy, aspect, z_near, z_far);

    cogl_matrix_init_identity (&view);
    cogl_matrix_view_2d_in_perspective (&view, fovy, aspect, z_near, z_2d,
                                      width,
                                      height);
    */
    //cogl_framebuffer_set_modelview_matrix (priv->fb, &view);

    //cogl_matrix_init_identity (&priv->matrix); 
    //cogl_matrix_translate(&priv->matrix,  width/2, height/2, 0);
    //cogl_matrix_scale (&priv->matrix, 100, 100, 100);
    //cogl_matrix_rotate(&priv->matrix, 45, 0, 1, 0);
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


/**
 * clutter_plate_get_matrix:
 * @plate: a #ClutterPlate
 * @matrix: return location for a #ClutterMatrix
 *
 * Retrieves the matrix of @plate.
 */
void 
clutter_plate_get_matrix (ClutterPlate *plate, 
                          const ClutterMatrix *matrix){
    ClutterPlatePrivate *priv;

    g_return_if_fail (CLUTTER_IS_PLATE (plate));
    g_return_if_fail (matrix != NULL);

    priv = plate->priv;

    memcpy((void *)matrix, &priv->matrix, sizeof(CoglMatrix));
}

/**
 * clutter_plate_set_matrix:
 * @plate: a #ClutterPlate
 * @matrix: a #CoglMatrix
 *
 * Sets the matrix of @plate.
 */
void
clutter_plate_set_matrix (ClutterPlate   *plate,
			     const ClutterMatrix *matrix){
    ClutterPlatePrivate *priv;

    g_return_if_fail (CLUTTER_IS_PLATE (plate));
    g_return_if_fail (matrix != NULL);

    g_object_ref (plate);

    priv = plate->priv;

    memcpy(&priv->matrix, matrix, sizeof(CoglMatrix));

    if (CLUTTER_ACTOR_IS_VISIBLE (CLUTTER_ACTOR (plate)))
        clutter_actor_queue_redraw (CLUTTER_ACTOR (plate));

    g_object_notify (G_OBJECT (plate), "matrix");
    g_object_unref (plate);
}
