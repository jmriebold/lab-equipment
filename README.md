<b>Claire Jaja, with modifications by John Riebold</b><br />
an equipment reservation system for the University of Washington Phonetics and Sociolinguistics labs

* Created using Django v. 1.6.4 (for more information on Django, see [documentation](https://docs.djangoproject.com/en/1.6/))
* Using additional app South for database migration (for more information on South, see [documentation](http://south.readthedocs.org/en/latest/index.html))
* Using MySQL database as backend (named lab_equipment, can be accessed by user: calendar)
* Using virtualenv for local packages (to activate virtual environment within calendar user home folder (required for successfully running application with all dependencies), use command: <code>source ./virtualenv/lab-equipment/bin/activate</code>)
* Currently set up to appear at [https://zeos.ling.washington.edu/equipment-reservations](https://zeos.ling.washington.edu/equipment-reservations)

# Usage
## South
<b>Important:</b> Whenever changes are made to "equipment" app, run (within the top level lab-equipment repository folder that this README is found in):
    
    python manage.py schemamigration equipment --auto
    python manage.py migrate equipment
    
If you've modified database fields, this will prompt you for how to migrate existing items (equipment, users, etc) in the database.

## General
* To add equipment and other entries, do so via the [admin site](https://zeos.ling.washington.edu/equipment-reservations/admin/).

# Django Basics
* To update fields (e.g. what types of information are associated with a piece of equipment), edit equipment/models.py.
* To update what information (about equipment, user, etc) is passed from the underlying database to a website, edit equipment/views.py.
* To update what URL patterns are viable, edit equipment/urls.py.
* To update how webpages actually appear, edit templates (which appear within equipment/templates folder).
* To update general settings, edit lab_equipment/settings.py file.
* <b>Important:</b> After changing views, models, or other configuration files, execute <code>touch lab_equipment/lab_equipment/wsgi.py</code> to trigger a reload of the server.

# To Do
## Major
* Add "Your Reservations" page for users that show past, current, and future reservations, with options to cancel reservation, mark equipment as lost/broken/stolen, use checklist for verifying taking out/returning equipment, renew reservation (if equipment is not already reserved by others for requested dates), etc.
* Use Google Calendar API to automatically add reservation events to the existing lab calendars.
* Implement email notifications to be sent 24 hours before start of reservation, 24 hour before end of reservation, and 24 hours after end of reservation if the equipment was not marked as returned (within "Your Reservations" page) - last email also sent to appropriate lab director(s).
* Add override capabilities for lab directors, so that they can make/allow reservations longer than the equipment's maximum reservation length, less than 24 hours in advance, etc.

## Minor
* On the page where date and time are filled in when starting a reservation, catch and return appropriate error when those fields are not completely filled.
* Change the location field for equipment to a text field, instead of set options (more flexible since location designations are likely to change).
* Add privilege levels for Sociolinguistics Lab - discuss with lab directors if privileges should be totally separate or have some interaction.
* Change privileges to checkboxes (instead of distinct categories, can check one box for lab equipment privileges, another for field equipment privileges, etc, to allow for intersections).
* Possibly implement functionality for quarterly privileges (automatically removed at end of quarter) or guest faculty privileges (limited in time frame and possibly scope of equipment allowed - discuss with lab directors).
* Add a category of equipment for reserving rooms (currently have 'booth' for recording booths - maybe expand this to be rooms?).
