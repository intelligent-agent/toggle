#include <clutter/clutter.h>
#include <stdlib.h>

ClutterActor *rect;
gdouble rotation = 0;

void on_timeline_new_frame(ClutterTimeline *timeline, gint frame_num, gpointer data) {
        rotation += 0.3;

        clutter_actor_set_rotation(rect, CLUTTER_Z_AXIS, rotation * 5, 0, 0, 0);
}

int main(int argc, char *argv[]) {
        int ret; 
	ret = clutter_init(&argc, &argv);

        ClutterColor stage_color = { 0xFF, 0xFF, 0xFF, 0xFF };
	ClutterColor actor_color = { 0x00, 0xCC, 0x00, 0xFF };

        ClutterActor *stage = clutter_stage_new();
        //clutter_actor_set_size(stage, 800, 480);
        clutter_actor_set_background_color(stage, &stage_color);

	/* Add a rectangle to the stage: */
	rect = clutter_actor_new();
	clutter_actor_set_background_color (rect, &actor_color);	
	clutter_actor_set_size (rect, 100, 50);
	clutter_actor_set_position (rect, 240, 400);
	clutter_actor_add_child (stage, rect);
	clutter_actor_show (rect);

	ClutterTimeline *timeline = clutter_timeline_new(60);
	g_signal_connect(timeline, "new-frame", G_CALLBACK(on_timeline_new_frame), NULL);
	clutter_timeline_set_loop(timeline, TRUE); 
	clutter_timeline_start(timeline);

        clutter_actor_show(stage);

        clutter_main();

        return EXIT_SUCCESS;
}
