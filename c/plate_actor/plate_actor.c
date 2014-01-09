#include "plate_actor.h"

#include <cogl/cogl.h>

G_DEFINE_TYPE (ClutterPlate, clutter_plate, CLUTTER_TYPE_ACTOR);

enum
{
  PROP_0
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

    int width; 
    int height; 
};

static void
do_plate_paint (ClutterActor *self){
    ClutterPlate        *plate;
    ClutterPlatePrivate *priv;
    CoglColor           *color = cogl_color_new();
    gfloat texcoords[4] = { 0, 0, 1, 1 };
    CoglHandle material;

    plate = CLUTTER_PLATE(self);
    priv = plate->priv;

    /* Paint the plate with the actor's color: */
    cogl_color_init_from_4f(color, 1.0f, 1.0f, 1.0f, 1.0f);

    // Clear the framebuffer
    cogl_framebuffer_clear4f (priv->fb,
        COGL_BUFFER_BIT_COLOR|COGL_BUFFER_BIT_DEPTH,
        0, 0, 0, 1);

    // Paint the primitive in the offscreen framebuffer
    cogl_framebuffer_push_matrix (priv->fb);
    cogl_pipeline_set_color (priv->pipeline, color);
    cogl_framebuffer_scale (priv->fb, 75, 75, 75);
    cogl_primitive_draw (priv->prim, priv->fb, priv->pipeline);
    cogl_framebuffer_pop_matrix (priv->fb);    

    // Draw the frambuffer as the actor. 
    material = cogl_material_new ();
    cogl_material_set_color4ub (material, 0x88, 0x88, 0x88, 0x88);
    cogl_material_set_layer (material, 0, priv->texture);
    cogl_set_source (material);
    cogl_rectangle_with_texture_coords (0, 0,
                                        priv->width, priv->height,
                                        texcoords[0],
                                        texcoords[1],
                                        texcoords[2],
                                        texcoords[3]);
}

static void
clutter_plate_paint (ClutterActor *self){
  do_plate_paint (self);
}

static void
clutter_plate_pick (ClutterActor *self, const ClutterColor *color){
  do_plate_paint (self);
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
  actor_class->paint = clutter_plate_paint;
  actor_class->pick = clutter_plate_pick;

  gobject_class->finalize     = clutter_plate_finalize;
  gobject_class->dispose      = clutter_plate_dispose;

  g_type_class_add_private (gobject_class, sizeof (ClutterPlatePrivate));
}

static void
clutter_plate_init (ClutterPlate *self){
    ClutterPlatePrivate *priv;
    ClutterBackend      *be         = clutter_get_default_backend ();
    CoglContext         *ctx        = clutter_backend_get_cogl_context (be);
    CoglOffscreen       *offscreen;
    CoglMatrix          view;
    int width, height;
    float fovy, aspect, z_near, z_2d, z_far;


    self->priv       = priv = CLUTTER_PLATE_GET_PRIVATE (self);
    //priv->fb         = cogl_get_draw_framebuffer ();
    priv->pipeline   = cogl_pipeline_new(ctx);

    priv->width = width = 400;
    priv->height = height = 400;

    // Initialize the plate primitive 
    priv->prim = cogl_primitive_new_p3t2 (ctx, COGL_VERTICES_MODE_LINES,
                                       G_N_ELEMENTS (vertices),
                                       vertices);

    
    // Make a new blank texture
    priv->texture = cogl_texture_new_with_size (width, height,
                                                 COGL_TEXTURE_NONE,
                                                 COGL_PIXEL_FORMAT_RGB_888);

    // Init the Offscreen buffer from the texture
    offscreen = cogl_offscreen_new_with_texture (priv->texture);
    priv->fb = COGL_FRAMEBUFFER (offscreen);
    
    cogl_framebuffer_set_viewport (priv->fb,
                                 0, 0,
                                 width,
                                 height);

    fovy = 60; /* y-axis field of view */
    aspect = width/height;
    z_near = 0.1; /* distance to near clipping plane */
    z_2d = 1000; /* position to 2d plane */
    z_far = 2000; /* distance to far clipping plane */

    cogl_framebuffer_perspective (priv->fb, fovy, aspect, z_near, z_far);

    cogl_matrix_init_identity (&view);
    cogl_matrix_view_2d_in_perspective (&view, fovy, aspect, z_near, z_2d,
                                      width,
                                      height);

    cogl_framebuffer_set_modelview_matrix (priv->fb, &view);
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

