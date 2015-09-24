<b>Claire Jaja, with modifications by John Riebold</b><br />
an equipment reservation system for the University of Washington Phonetics and Sociolinguistics labs

* Created using Django v. 1.6.11 (for more information on Django, see [documentation](https://docs.djangoproject.com/en/1.6/))
* Using additional app South for database migration (for more information on South, see [documentation](http://south.readthedocs.org/en/latest/index.html))
* Using MySQL database as backend (named lab_equipment, can be accessed by user: calendar)
* Using virtualenv for local packages (the virtual environment is automatically activated upon login using the command: <code>source ./.virtualenv/lab-equipment/bin/activate</code> Deactivate it by executing <code>deactivate</code>)
* Currently set up to appear at [https://zeos.ling.washington.edu/equipment-reservations](https://zeos.ling.washington.edu/equipment-reservations)

# Usage
## South
<b>Important:</b> Whenever changes are made to models that will require changes to the database, run (within the top level lab-equipment repository folder that this README is found in):
    
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
