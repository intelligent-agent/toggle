#include <clutter/clutter.h>
#include <mx/mx.h>
#include <mash/mash.h>
#include <stdlib.h>
#include "plate-actor.h"

ClutterActor *model, *plate, *volume_stage, *volume_viewport;
ClutterMatrix mat;
float rotation;
gboolean touching = FALSE;
gfloat port_x, port_y;
gfloat start_x, start_y;
gfloat current_x, current_y;
gfloat delta_x, delta_y;

void
on_enter_volume_viewport(ClutterActor *actor,
               ClutterEvent *event){
    touching = TRUE;
    clutter_event_get_coords(event, &start_x, &start_y);
}
void
on_leave_stage(ClutterActor *actor,
               ClutterEvent *event){
    if(touching){
        touching = FALSE;
    }
}
void
on_motion_event(ClutterActor *actor,
                ClutterEvent *event){
    clutter_event_get_coords(event, &port_x, &port_y);
    if(touching){
        delta_x = (port_x-start_x);
        delta_y = (port_y-start_y);
        clutter_actor_set_rotation_angle(volume_stage, CLUTTER_X_AXIS, current_x+delta_x/10.0 );
        clutter_actor_set_rotation_angle(volume_stage, CLUTTER_Y_AXIS, current_y+delta_y/10.0 );
        current_x = delta_x;
        current_y = delta_y;
    }
}

void
on_motion_viewport(ClutterActor *actor, 
                ClutterEvent *event){
    fprintf(stderr, "motion-viewport\n");
}


// Main
int main(int argc, char *argv[]) {
    int ret;
	GError* err = NULL;
	ClutterActor *stage;
	ClutterActor *box;
	MashLightSet *light_set;
	ClutterActor *light_point, *light_directional, *light_spot;
	MxStyle *style;

    ret = clutter_init(&argc, &argv);

    // Make a transformation matrix and apply it to the plate
    cogl_matrix_init_identity(&mat);    
    cogl_matrix_translate(&mat,  200, 200, 0);
    cogl_matrix_scale (&mat, 100, 100, 100);
    cogl_matrix_rotate(&mat, 180, 0, 0, 1);

    // Dummy call to make sure it gets loaded
    clutter_plate_new();

	const gchar *paths[] = { "/etc/toggle/", "/etc/toggle/style/" };

	style = mx_style_get_default ();
	if (!mx_style_load_from_file (style, "/etc/toggle/style/style.css", &err)){
      		g_warning ("Error setting style: %s", err->message);
      		g_clear_error (&err);
    }

    // Load the scene using clutterscript
	ClutterScript *ui = clutter_script_new();
	clutter_script_add_search_paths (ui, paths, 1);
	clutter_script_load_from_file(ui, "/etc/toggle/ui.json", &err);

    clutter_script_get_objects (ui,"stage", &stage, NULL);
    clutter_script_connect_signals (ui, ui);
    clutter_actor_show(stage);

    clutter_script_get_objects(ui, "volume-viewport", &volume_viewport, NULL);
    clutter_script_get_objects(ui, "volume-stage", &volume_stage, NULL);
    clutter_script_get_objects(ui, "plate", &plate, NULL);

	if (err != NULL){
		g_critical ("Error loading ClutterScript file %s\n%s", "ui.json", err->message);
      		g_error_free (err);
      		exit (EXIT_FAILURE);
    }

	if ((model = mash_model_new_from_file (MASH_DATA_NONE, 
                "/usr/share/models/treefrog.ply", &err)) == NULL){
      		g_warning ("Failed to load model: %s\n", err->message);
      		g_clear_error (&err);
    }

	// Set up the light
	light_set = mash_light_set_new ();
	light_point = mash_point_light_new();
	light_directional = mash_directional_light_new();
	light_spot = mash_spot_light_new();

	ClutterColor ambient  = { 128, 128, 128, 128 };
	ClutterColor diffuse  = { 128, 128, 128, 128 };
	ClutterColor specular = { 128, 128, 128, 128 };

    mash_light_set_add_light (light_set, MASH_LIGHT (light_point));
    mash_light_set_add_light (light_set, MASH_LIGHT (light_directional));
	mash_light_set_add_light (light_set, MASH_LIGHT (light_spot));
 	mash_model_set_light_set (MASH_MODEL (model), light_set);
	g_object_unref (light_set);

	// Add the model the lights to the volume viewport
	clutter_actor_add_child(volume_viewport, light_point);
	clutter_actor_add_child(volume_viewport, light_directional);
	clutter_actor_add_child(volume_viewport, light_spot);

	// Make a new material for the model
	CoglMaterial *material = (CoglMaterial *) cogl_material_new();
	CoglColor *model_color = cogl_color_new();
	cogl_color_init_from_4f(model_color, 0.0, 1.0, 0.0, 1.0);

	cogl_material_set_layer_combine_constant (material, 0, model_color);
	cogl_material_set_layer_combine (material, 0, "RGBA = MODULATE(CONSTANT, PRIMARY)", NULL);
	cogl_material_set_shininess(material, 128.0);
	//cogl_material_set_diffuse(material, 0.5, 0.5, 0.5, 0.5);
	mash_model_set_material (MASH_MODEL (model), material);

	// Position and size the model
	//clutter_actor_set_pivot_point (model, 0.5, 0.5);
	//clutter_actor_set_position(model, clutter_actor_get_width(plate)/2.0, clutter_actor_get_height(plate)/2.0);
	//clutter_actor_set_rotation_angle(model, CLUTTER_X_AXIS, 180.0);
    clutter_actor_add_child(volume_stage, model);
   
    clutter_actor_set_pivot_point (volume_stage, 0.5, 0.5);

    //g_signal_connect (stage, "touch-event", G_CALLBACK (on_touch_event), NULL);
    //g_signal_connect (stage, "event", G_CALLBACK (on_event), NULL);
    g_signal_connect (stage, "motion-event", G_CALLBACK (on_motion_event), NULL);
    g_signal_connect (volume_viewport, "motion-event", G_CALLBACK (on_motion_viewport), NULL);
    g_signal_connect (stage, "enter-event", G_CALLBACK (on_enter_volume_viewport), NULL);
    g_signal_connect (stage, "leave-event", G_CALLBACK (on_leave_stage), NULL);
    

	/* Rotate the display/stage */
    clutter_script_get_objects(ui, "box", &box, NULL);
    clutter_actor_set_rotation_angle (box, CLUTTER_Z_AXIS, -90.0f);
    clutter_actor_set_position(box, 0, 800);

    clutter_main();

    return EXIT_SUCCESS;
}
