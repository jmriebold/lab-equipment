<b>Claire Jaja & John Riebold</b><br />
an equipment reservation system for the University of Washington Phonetics and Sociolinguistics labs

* Created using Django v. 1.6.11 (for more information on Django, see [documentation](https://docs.djangoproject.com/en/1.6/))
* Using additional app South for database migration (for more information on South, see [documentation](http://south.readthedocs.org/en/latest/index.html))
* Using MySQL database as backend (named lab_equipment, can be accessed by user: calendar)
* Using virtualenv for local packages (the virtual environment is automatically activated upon login using the command: <code>source ./.virtualenv/lab-equipment/bin/activate</code> Deactivate it by executing <code>deactivate</code>)
* Currently set up to appear at [https://zeos.ling.washington.edu/equipment-reservations](https://zeos.ling.washington.edu/equipment-reservations)

# Functionality
* The lab equipment reservation system (LERS) includes a listing of all lab equipment, including the locations, links to manuals and wiki guides, indicators for the condition (e.g. "ok", "broken", "lost"), whether it is reservable or not.
* Google Calendar events will automatically be created on the appropriate calendar (or Misc if there is none) so that it’s easier to see at a glance what's been checked out. 
* Confirmation emails will also be sent upon making a reservation, canceling a reservation, or returning a piece of equipment, and reminder emails will be sent leading up to a reservation or return, or when a piece of equipment has not been returned.
* A number of restrictions govern who can make reservations and how they are allowed to be made. Each user and each piece of equipment is assigned a lab and a permission level (ranging from "none" to "lab director"). All equipment has a maximum reservation time, and reservations must be made at least 24 hours in advance. These restrictions can be overridden by lab directors and staff.


# Structure
## Django
* Django is broadly organized into projects and apps. Each project (in this case, 'lab-equipment') contains one or more apps (only one here: 'equipment').
* equipment/models.py contains the 'models' (i.e. objects, classes) for the app. This includes equipment, reservation, etc., as well as fields for every piece of information stored in the models.
* equipment/views.py contains methods that pass information (e.g. equipment, user, etc.) database to the webpages that are displayed to the user.
* equipment/utils.py is not a standard Django module, but contains all the helper methods used in the webapp (e.g. sending emails, making Google Calendar reservations, resizing images).
* equipment/urls.py contains regex patterns for matching URLS, used to direct users from page to page within the webapp.
* equipment/templates and its subdirectories contain the pages themselves.
* lab_equipment/settings.py contains the settings for the project (e.g. apps, middleware, etc.).

# Usage
## South
<b>Important:</b> Whenever changes are made to models that will require changes to the database, run (within the top level lab-equipment repository folder that this README is found in):
    
    python manage.py schemamigration equipment --auto
    python manage.py migrate equipment
    
If you've modified database fields, this will prompt you for how to migrate existing items (equipment, users, etc) in the database.

## General
* To add equipment, modify user permissions, and other tasks, do so via the [admin site](https://zeos.ling.washington.edu/equipment-reservations/admin/).
* Restrictions on reservations (e.g. maximum length, permissions) can be overridden by an admin via the [admin site](https://zeos.ling.washington.edu/equipment-reservations/admin/).
* <b>Important:</b> After changing views, models, or other configuration files, execute <code>touch lab_equipment/lab_equipment/wsgi.py</code> to trigger a reload of the server.

## Maintenance
* Although user accounts are created automatically, the default lab membership is "neither", and the default permission level is "none", to ensure new users can't simply log on to the site and immediately check out equipment without first being cleared by a lab director. Once a new user has been cleared for use of the site, they must have their permissions set via the [admin site](https://zeos.ling.washington.edu/equipment-reservations/admin/). To do so, edit the user, and add the required lab membership and privileges near the bottom of the page.
* If equipment names are changed or new calendars are added, the [dictionary](https://en.wikipedia.org/wiki/Associative_array) of calendars (which allows for Google Calendar IDs to be looked up using the equipment names) must be edited to reflect that. The dictionary 'calendars' is defined in the <code>get_calendar()</code> method in utils.py (~/lab-equipment/equipment). If the name of a piece of equipment tied to a specific calendar has been changed, its entry in the dictionary must also be changed (note: the names must match <i>exactly</i>, with the exception of caps). If you are adding a new piece of equipment that's tied to a specific calendar, you must add an entry for it, with the value being the Google Calendar ID (Google Calendar > Settings > Calendars > desired calendar > Calendar ID). The format of dictionary entries should be clear from the existing entries, but see the [Python documentation](https://docs.python.org/2/tutorial/datastructures.html#dictionaries) for more details and examples. Lastly, if the calendar itself is new, you must also share it with the Google service account which makes the API calls to create/delete events. To do so, navigate to Google Calendar > Settings > Calendars > desired calendar > Share this Calendar, and add the email address 275676223429-p0g1vpujgfric1gjoo020e898lhui6pa@developer.gserviceaccount.com with permissions to "Make changes AND manage sharing".
