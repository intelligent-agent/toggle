#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <cairo.h>
#include <clutter/clutter.h>
#include <glib.h>

gboolean pressed = FALSE;

GPtrArray *points;
ClutterContent *canvas;

typedef struct {
  float x; 
  float y;
} point;


void funcname (gpointer data, gpointer user_data){
  fprintf(stderr, "func\n");
}


static gboolean
draw_content (ClutterCanvas *canvas,
              cairo_t       *cr,
              int            surface_width,
              int            surface_height)
{
  /* rounded rectangle taken from:
   *
   *   http://cairographics.org/samples/rounded_rectangle/
   *
   * we leave 1 pixel around the edges to avoid jagged edges
   * when rotating the actor
   */
  //cairo_save (cr);
  cairo_set_operator (cr, CAIRO_OPERATOR_CLEAR);
  cairo_paint (cr);
  //cairo_restore (cr);

  cairo_set_line_width(cr, 1);  
  cairo_set_operator(cr, CAIRO_OPERATOR_OVER);
  cairo_set_source_rgb (cr, 0, 0, 0);
  cairo_new_sub_path (cr);
  for(int i=0; i<points->len; i++){
    point *p = (point*) g_ptr_array_index (points, i);  
    if(i==0){
      cairo_move_to(cr, p->x, p->y);
    }
    else{
      cairo_line_to(cr, p->x, p->y);
    }
    //fprintf(stderr, "pointer at stage x %.0f, y %.0f;, %p\n", p->x, p->y, p);
  }
  //fprintf(stderr, "%i\n", points->len);
  cairo_stroke (cr);

  cairo_move_to(cr, 0, 0);
  cairo_line_to(cr, 1920, 1080);
  cairo_stroke (cr);
  

  //cairo_arc (cr, x + width - radius, y + radius, radius, -90 * degrees, 0 * degrees);
  //cairo_arc (cr, x + width - radius, y + height - radius, radius, 0 * degrees, 90 * degrees);
  //cairo_arc (cr, x + radius, y + height - radius, radius, 90 * degrees, 180 * degrees);
  //cairo_arc (cr, x + radius, y + radius, radius, 180 * degrees, 270 * degrees);
  //cairo_close_path (cr);


  /* we're done drawing */
  return TRUE;
}

static gboolean
mouse_move (ClutterActor *actor,
                   ClutterEvent *event,
                   gpointer      user_data){
  
  gfloat stage_x, stage_y;
  clutter_event_get_coords (event, &stage_x, &stage_y);

  if(pressed){
    point p = {
      .x=stage_x, 
      .y=stage_y
    };
    point *pp = malloc(sizeof(point));
    memcpy(pp, &p, sizeof(point));
    g_ptr_array_add (points, (gpointer) pp);
    clutter_content_invalidate (canvas);
    //fprintf(stderr, "pointer at stage x %.0f, y %.0f; %p\n",
    //       p.x, p.y, &p);
  }
  

  return CLUTTER_EVENT_STOP;
}

static gboolean
mouse_press (ClutterActor *actor,
                   ClutterEvent *event,
                   gpointer      user_data){
  
  gfloat stage_x, stage_y;
  clutter_event_get_coords (event, &stage_x, &stage_y);

  //fprintf(stderr, "Press x %.0f, y %.0f;\n",
  //         stage_x, stage_y);

  pressed = TRUE;
  

  return CLUTTER_EVENT_STOP;
}

static gboolean
mouse_release (ClutterActor *actor,
                   ClutterEvent *event,
                   gpointer      user_data){
  
  gfloat stage_x, stage_y;
  clutter_event_get_coords (event, &stage_x, &stage_y);

  pressed = FALSE;

  //fprintf(stderr, "Release x %.0f, y %.0f;\n",
  //         stage_x, stage_y);

  
  

  return CLUTTER_EVENT_STOP;
}


int
main (int argc, char *argv[]){
  ClutterActor *stage, *actor;
  
  ClutterTransition *transition;

  points = g_ptr_array_new ();


  /* initialize Clutter */
  if (clutter_init (&argc, &argv) != CLUTTER_INIT_SUCCESS)
    return EXIT_FAILURE;

  /* create a stage */
  stage = clutter_stage_new ();
  clutter_stage_set_title (CLUTTER_STAGE (stage), "Multi touch tracker");
  //clutter_stage_set_use_alpha (CLUTTER_STAGE (stage), TRUE);
  clutter_actor_set_background_color (stage, CLUTTER_COLOR_White);
  //clutter_actor_set_size (stage, 500, 500);

  //clutter_actor_set_opacity (stage, 64);
  clutter_actor_show (stage);

  /* our 2D canvas, courtesy of Cairo */
  canvas = clutter_canvas_new ();
  clutter_canvas_set_size (CLUTTER_CANVAS (canvas), 1920, 1080);
  clutter_stage_set_user_resizable(CLUTTER_STAGE(stage), TRUE);
  clutter_stage_set_fullscreen(CLUTTER_STAGE(stage), TRUE);

  /* the actor that will display the contents of the canvas */
  actor = clutter_actor_new ();
  clutter_actor_set_content (actor, canvas);
  clutter_actor_set_content_gravity (actor, CLUTTER_CONTENT_GRAVITY_CENTER);
  clutter_actor_set_content_scaling_filters (actor,
                                             CLUTTER_SCALING_FILTER_TRILINEAR,
                                             CLUTTER_SCALING_FILTER_LINEAR);
  clutter_actor_set_pivot_point (actor, 0.5f, 0.5f);
  clutter_actor_add_constraint (actor, clutter_align_constraint_new (stage, CLUTTER_ALIGN_BOTH, 0.5));
  clutter_actor_set_request_mode (actor, CLUTTER_REQUEST_CONTENT_SIZE);
  clutter_actor_add_child (stage, actor);

  /* the actor now owns the canvas */
  g_object_unref (canvas);

  /* create the continuous animation of the actor spinning around its center */
  //transition = clutter_property_transition_new ("rotation-angle-y");
  //clutter_transition_set_from (transition, G_TYPE_DOUBLE, 0.0);
  //clutter_transition_set_to (transition, G_TYPE_DOUBLE, 360.0);
  //clutter_timeline_set_duration (CLUTTER_TIMELINE (transition), 2000);
  //clutter_timeline_set_repeat_count (CLUTTER_TIMELINE (transition), -1);
  //clutter_actor_add_transition (actor, "rotateActor", transition);

  /* the actor now owns the transition */
  //g_object_unref (transition);

  g_signal_connect(stage, "motion-event",  G_CALLBACK (mouse_move), NULL);
  //g_signal_connect(stage, "touch-event", touch_event)

  g_signal_connect(stage, "button-press-event",  G_CALLBACK (mouse_press), NULL);
  g_signal_connect(stage, "button-release-event",  G_CALLBACK (mouse_release), NULL);

  /* quit on destroy */
  g_signal_connect (stage, "destroy", G_CALLBACK (clutter_main_quit), NULL);

  /* connect our drawing code */
  g_signal_connect (canvas, "draw", G_CALLBACK (draw_content), NULL);

  /* invalidate the canvas, so that we can draw before the main loop starts */
  clutter_content_invalidate (canvas);

  clutter_main ();

  return EXIT_SUCCESS;
}
