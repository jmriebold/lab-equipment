<b>Claire Jaja & John Riebold</b><br />
an equipment reservation system for the University of Washington Phonetics and Sociolinguistics labs

* Created using Django v. 1.6.11 (for more information on Django, see [documentation](https://docs.djangoproject.com/en/1.6/))
* Using additional app South for database migration (for more information on South, see [documentation](http://south.readthedocs.org/en/latest/index.html))
* Using MySQL database as backend (named lab_equipment, can be accessed by user: calendar)
* Using virtualenv for local packages (the virtual environment is automatically activated upon login using the command: <code>source ./.virtualenv/lab-equipment/bin/activate</code> Deactivate it by executing <code>deactivate</code>)
* Currently set up to appear at [https://zeos.ling.washington.edu/equipment-reservations](https://zeos.ling.washington.edu/equipment-reservations)

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
