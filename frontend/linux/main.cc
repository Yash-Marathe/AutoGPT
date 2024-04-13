#include <glib.h>
#include "my_application.h"

int
main (int argc, char **argv)
{
  g_autoptr(MyApplication) app = my_application_new ();
  gint status;

  /* Check if the application is already running */
  if (!g_application_is_initialized (G_APPLICATION (app)))
    status = g_application_run (G_APPLICATION (app), argc, argv);
  else
    {
      /* Get the existing instance and send a message to it */
      GApplication *existing = g_application_get_default ();
      g_application_activate (existing, argc, argv);
      status = 0;
    }

  return status;
}
