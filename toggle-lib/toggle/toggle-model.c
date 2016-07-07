#include "toggle-model.h"


/**
 * SECTION:toggle-model
 * @short_description: Model used in Toggle
 *
 * A #ToggleModel is a subclass of #MashModel
 * Yep!
 */
G_DEFINE_TYPE (ToggleModel, toggle_model, MASH_TYPE_MODEL);

/* macro for accessing the object's private structure */
#define TOGGLE_MODEL_GET_PRIVATE(obj) (G_TYPE_INSTANCE_GET_PRIVATE ((obj), TOGGLE_TYPE_MODEL, ToggleModelPrivate))

struct _ToggleModelPrivate{
    CoglPipeline *pipeline;
    CoglColor *color;
};


static void
toggle_model_class_init (ToggleModelClass *klass){
  ClutterActorClass *actor_class = CLUTTER_ACTOR_CLASS (klass);
  GObjectClass *gobject_class = G_OBJECT_CLASS (klass);
  GParamSpec *pspec;

  g_type_class_add_private (klass, sizeof (ToggleModelPrivate));
}

static void
toggle_model_init (ToggleModel *self){
    ToggleModelPrivate *priv;
    priv = self->priv = TOGGLE_MODEL_GET_PRIVATE (self);

    priv->pipeline = (CoglPipeline*) mash_model_get_material (MASH_MODEL (&self->parent));
    cogl_pipeline_set_layer_combine (priv->pipeline, 0, "RGBA = MODULATE(CONSTANT, PRIMARY)", NULL);
}


/**
 * toggle_model_new:
 *
 * Creates a new #ToggleModel instance
 *
 * Returns: a new #ToggleModel
 */
ClutterActor *
toggle_model_new (void){
    return g_object_new (TOGGLE_TYPE_MODEL, NULL);
}


/**
* toggle_model_new_from_file:
* @flags: Flags for loading the data.
* @filename: The name of a PLY file to load.
* @error: Return location for a #GError or %NULL.
*
* This is a convenience function that creates a new #MashData
* and immediately loads the data in @filename. If the load succeeds a
* new #MashModel will be created for the data. The model has a
* default white material so that if vertices of the model have any
* color attributes they will be used directly. The material does not
* have textures by default so if you want the model to be textured
* you will need to modify the material.
*
* Return value: a new #ToggleModel or %NULL if the load failed.
*/
ClutterActor *
toggle_model_new_from_file (MashDataFlags flags, const gchar *filename, GError **error){
    MashData *data = mash_data_new ();
    ClutterActor *model = NULL;
    if (mash_data_load (data, flags, filename, error)){
        model = toggle_model_new ();
        mash_model_set_data (MASH_MODEL (model), data);
    }
    g_object_unref (data);
    return model;
}


/**
* toggle_model_load_from_file:
* @self: A #ToggleModel instance
* @flags: Flags for loading the data.
* @filename: The name of a PLY file to load.
* @error: Return location for a #GError or %NULL.
*
*/
void
toggle_model_load_from_file(ToggleModel *self, MashDataFlags flags, const gchar *filename, GError **error){
    ToggleModelPrivate *priv;
    g_return_if_fail (TOGGLE_IS_MODEL (self));

    priv = self->priv;

    MashData *data = mash_data_new ();
    if (mash_data_load (data, flags, filename, error)){
        mash_model_set_data (MASH_MODEL (&self->parent), data);
    }
    g_object_unref (data);
}

/**
 * toggle_model_set_color:
 * @self: a #ToggleModel
 * @color: the #ClutterColor to use as the color for the button text
 *
 * Set the color of the text on the button
 */
void
toggle_model_set_color (ToggleModel *self, const ClutterColor *color){
    ToggleModelPrivate *priv;

    g_return_if_fail (TOGGLE_IS_MODEL (self));

    priv = self->priv = TOGGLE_MODEL_GET_PRIVATE (self);

    priv->pipeline = (CoglPipeline*) mash_model_get_material (MASH_MODEL (&self->parent));
	priv->color     = cogl_color_new();
    cogl_color_init_from_4ub(priv->color, color->red, color->green, color->blue, color->alpha);

    cogl_pipeline_set_cull_face_mode (priv->pipeline, 1);
	cogl_pipeline_set_layer_combine_constant (priv->pipeline, 0, priv->color);
    cogl_pipeline_set_layer_combine (priv->pipeline, 0, "RGBA = MODULATE (CONSTANT, PRIMARY)", NULL);
}


/**
 * toggle_model_set_culling:
 * @self: a #ToggleModel
 * @culling: the culling type
 *
 * Set the culling type for the model
 */
void
toggle_model_set_culling (ToggleModel *self, int culling){
    ToggleModelPrivate *priv;
    g_return_if_fail (TOGGLE_IS_MODEL (self));
    priv = self->priv = TOGGLE_MODEL_GET_PRIVATE (self);

    cogl_pipeline_set_cull_face_mode (priv->pipeline, culling);
    cogl_pipeline_set_layer_combine_constant (priv->pipeline, 0, priv->color);
    cogl_pipeline_set_layer_combine (priv->pipeline, 0, "RGBA = MODULATE (CONSTANT, PRIMARY)", NULL);
}



/**
 * toggle_model_set_specular:
 * @self: a #ToggleModel
 * @color: the #ClutterColor to use as the color for the button text
 *
 * Set the color of the text on the button
 */
void
toggle_model_set_specular (ToggleModel *self, const ClutterColor *color){
    ToggleModelPrivate *priv;

    g_return_if_fail (TOGGLE_IS_MODEL (self));

    priv = self->priv = TOGGLE_MODEL_GET_PRIVATE (self);

    priv->pipeline = (CoglPipeline*) mash_model_get_material (MASH_MODEL (&self->parent));
	CoglColor* color1   = cogl_color_new();
    cogl_color_init_from_4ub(color1, color->red, color->green, color->blue, color->alpha);

    cogl_pipeline_set_specular(priv->pipeline, color1);
}

/**
 * toggle_model_get_model_depth:
 * @self: a #ToggleModel
 *
 * Return value: the depth of the actor, in pixels
 */
gfloat
toggle_model_get_model_depth (ToggleModel *self){
    ToggleModelPrivate *priv;

    g_return_if_fail (TOGGLE_IS_MODEL (self));

    priv = self->priv = TOGGLE_MODEL_GET_PRIVATE (self);

    return mash_model_get_model_depth(self);
}
