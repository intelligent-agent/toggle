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
    CoglMaterial *material;
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

  	// Make a new material for the model
	priv->material  = (CoglMaterial *) cogl_material_new();
	priv->color     = cogl_color_new();
	cogl_color_init_from_4f(priv->color, 0.0, 1.0, 0.0, 1.0);

	cogl_material_set_layer_combine_constant (priv->material, 0, priv->color);
	cogl_material_set_layer_combine (priv->material, 0, "RGBA = MODULATE(CONSTANT, PRIMARY)", NULL);
	cogl_material_set_shininess(priv->material, 128.0);
	mash_model_set_material (MASH_MODEL(&self->parent), priv->material);
    fprintf(stderr, "Material set!\n");
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
    fprintf(stderr, "New model\n");
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
    fprintf(stderr, "new from file!\n");
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
    fprintf(stderr, "load from file!\n");
}

