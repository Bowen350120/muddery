"""
At_initial_setup module template

Custom at_initial_setup method. This allows you to hook special
modifications to the initial server startup process. Note that this
will only be run once - when the server starts up for the very first
time! It is called last in the startup process and can thus be used to
overload things that happened before it.

The module must contain a global function at_initial_setup().  This
will be called without arguments. Note that tracebacks in this module
will be QUIETLY ignored, so make sure to check it well to make sure it
does what you expect it to.

"""

from __future__ import print_function

from django.conf import settings
from evennia.utils import search, logger
from muddery.utils import builder, importer, utils
from muddery.utils.game_settings import GAME_SETTINGS
from muddery.typeclasses.character_skills import MudderySkill
import traceback

LIMBO_DESC = "Welcome to your new {wMuddery{n-based game! " +\
             "Visit http://www.muddery.org if you need help, " +\
             "want to contribute, report issues or just join the community."

def at_initial_setup():
    """
    Build up the default world and set default locations.
    """

    try:
        # load world data
        importer.import_local_all()

        # load game settings
        GAME_SETTINGS.reset()

        # build world
        builder.build_all()
        
        # set limbo's desc
        limbo_obj = search.search_object("#2", exact=True)
        if limbo_obj:
            limbo_obj[0].db.desc = LIMBO_DESC
            limbo_obj[0].position = None

        # set default locations
        builder.reset_default_locations()

        superuser = search.search_object("#1", exact=True)
        if superuser:
            superuser = superuser[0]

            # move the superuser to the start location
            start_location = search.search_object(settings.START_LOCATION, exact=True)
            if start_location:
                start_location = start_location[0]
                superuser.move_to(start_location, quiet=True)

            # set superuser's data
            superuser.set_data_key(GAME_SETTINGS.get("default_player_character_key"))
            superuser.set_level(1)
            superuser.set_nickname("superuser")

    except Exception, e:
        ostring = "Can't build world: %s" % e
        print(ostring)
        print(traceback.format_exc())
