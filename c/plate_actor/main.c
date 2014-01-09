#include <clutter/clutter.h>
#include "plate_actor.h"
#include <stdlib.h>

ClutterActor *actor;
gdouble rotation = 0;

void on_timeline_new_frame(ClutterTimeline *timeline, gint frame_num, gpointer data) {
        rotation += 0.3;
        //clutter_actor_set_rotation_angle(actor, CLUTTER_X_AXIS, rotation * 5);
}

int main(int argc, char *argv[]){
    int ret; 
    ClutterColor stage_color = { 0xFF, 0xFf, 0xFF, 0xFF };

    ret = clutter_init (&argc, &argv);

    /* Get the stage and set its size and color: */
    ClutterActor *stage = clutter_stage_new ();
    clutter_actor_set_size (stage, 200, 200);
    clutter_actor_set_background_color (stage, &stage_color);

    /* Show the stage: */
    clutter_actor_show (stage);

    /* Add our custom actor to the stage: */
    actor = clutter_plate_new();
    clutter_actor_set_size (actor, 100, 100);
    clutter_actor_set_position (actor, 240, 400);
    clutter_actor_add_child (stage, actor);
    clutter_actor_show (actor);

    ClutterTimeline *timeline = clutter_timeline_new(60);
    g_signal_connect(timeline, "new-frame", G_CALLBACK(on_timeline_new_frame), NULL);
    clutter_timeline_set_repeat_count(timeline, -1);
    clutter_timeline_start(timeline);

    /* Start the main loop, so we can respond to events: */
    clutter_main ();

    return EXIT_SUCCESS;

}
