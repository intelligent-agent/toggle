#include <clutter/clutter.h>
#include <mx/mx.h>
#include <mash/mash.h>
#include <stdlib.h>

ClutterActor *model;
gdouble rotation = 0;

void on_timeline_new_frame(ClutterTimeline *timeline, gint frame_num, gpointer data) {
        rotation += 0.3;

        clutter_actor_set_rotation_angle(model, CLUTTER_Y_AXIS, rotation * 5);
}

int main(int argc, char *argv[]) {
        int ret;
	GError* err = NULL;
	ClutterActor *stage, *plate, *rect;
	ClutterActor *box;
	MashLightSet *light_set;
	ClutterActor *light_point, *light_directional;

        ret = clutter_init(&argc, &argv);

	gchar *filename = "ui.json";
	const gchar *paths[] = { "/usr/src/toggle/etc" };

	ClutterScript *ui = clutter_script_new();
	clutter_script_add_search_paths (ui, paths, 1);
	clutter_script_load_from_file(ui, "../etc/ui.json", &err);

        clutter_script_get_objects (ui,"stage", &stage, NULL);
        clutter_script_connect_signals (ui, ui);
        clutter_actor_show(stage);

        clutter_script_get_objects(ui, "3d-stage", &plate, NULL);

	if (err != NULL){
		g_critical ("Error loading ClutterScript file %s\n%s", filename, err->message);
      		g_error_free (err);
      		exit (EXIT_FAILURE);
    	}

        ClutterColor actor_color = { 0x00, 0xCC, 0x00, 0xFF };

	if ((model = mash_model_new_from_file (MASH_DATA_NONE, "../models/suzanne.ply", &err))
	== NULL){
      		g_warning ("Failed to load model: %s\n", err->message);
      		g_clear_error (&err);
    	}

	// Set up the light
	light_set = mash_light_set_new ();
	light_point = mash_point_light_new();
	light_directional = mash_directional_light_new();

	ClutterColor ambient  = { 128, 128, 128, 128 };
	ClutterColor diffuse  = { 128, 128, 128, 128 };
	ClutterColor specular = { 128, 128, 128, 128 };

	//mash_light_set_ambient(MASH_LIGHT(light_point), &ambient);
	//mash_light_set_diffuse(MASH_LIGHT(light_point), &diffuse);
	//mash_light_set_specular(MASH_LIGHT(light_point), &specular);

	//mash_point_light_set_constant_attenuation(MASH_LIGHT(light_point), 0.5);
	//mash_point_light_set_linear_attenuation(MASH_LIGHT(light_point), 0.5);

        mash_light_set_add_light (light_set, MASH_LIGHT (light_point));
        mash_light_set_add_light (light_set, MASH_LIGHT (light_directional));
 	mash_model_set_light_set (MASH_MODEL (model), light_set);
	g_object_unref (light_set);

	// Add the model and the light
	clutter_actor_add_child(plate, light_point);
	//clutter_actor_set_z_position(light1, -100);
	clutter_actor_set_position(light_point, clutter_actor_get_width(plate)/2.0, clutter_actor_get_height(plate)/2.0);
	clutter_actor_add_child(plate, model);

	// Make a new material for the model
	CoglMaterial *material = cogl_material_new();
	CoglColor* model_color = cogl_color_new();
	cogl_color_init_from_4f(model_color, 0.0, 1.0, 0.0, 0.5);
	cogl_material_set_layer_combine_constant (material, 0, model_color);
        cogl_material_set_layer_combine (material, 0, "RGBA = REPLACE(CONSTANT)", NULL);
	cogl_material_set_shininess(material, 128.0);
	cogl_material_set_diffuse(material, 0.5, 0.5, 0.5, 0.5);
	mash_model_set_material (MASH_MODEL (model), material);

	// Position and size the model
	clutter_actor_set_pivot_point (model, 0.5, 0.5);
	clutter_actor_set_position(model, clutter_actor_get_width(plate)/2.0, clutter_actor_get_height(plate)/2.0);
	clutter_actor_set_scale (model, 100.0, 100.0);

	// Make the model spin
        ClutterTimeline *timeline = clutter_timeline_new(60);
        g_signal_connect(timeline, "new-frame", G_CALLBACK(on_timeline_new_frame), NULL);
        clutter_timeline_set_repeat_count(timeline, -1);
        clutter_timeline_start(timeline);

	/* Rotate the stage */
        clutter_script_get_objects(ui, "box", &box, NULL);
        clutter_actor_set_rotation_angle (box, CLUTTER_Z_AXIS, -90.0f);
        clutter_actor_set_position(box, 0, 800);

        clutter_main();

        return EXIT_SUCCESS;
}
