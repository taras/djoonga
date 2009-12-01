.. _roadmap

=========================
Djoonga Evolution Roadmap
=========================

Phase 1: Joomla Administration
================================
Goal of this phase is to create a Django app that can be used to administer an
existing Joomla website.
    
Requirements
------------

Backwards Compatible
    The code produced during this phase must not modify the database schema
    of the Joomla! site in a way that might break backwards compatibility with
    Joomla!. At this phase, the user must be able to use Djoonga Admin or Joomla!
    Administrator interchanchably without negatively impacting one or the other.

Components
    Here is a list of components that will be included in Phase 1 and their
    corresponding Django App that will provide same Djoonga functionality.

    Content Components
        * *com_content* - :doc:`Articles </apps/articles>`
        * *com_section* - :doc:`Categories </apps/categories>`
        * *com_category* - :doc:`Categories </apps/categories>`
        * *com_weblinks* - :doc:`Links </apps/links>`
        * *com_contact* - :doc:`Contacts </apps/contacts>`
    
    Administrative Components
        * *com_user* - :doc:`Users </apps/users>`
        * *com_menu* - :doc:`Menu </apps/menus>`

Phase 2: Extending Joomla
=========================
The goal of this phase is to enable Joomla! service providers to expand Joomla!
functionality via Django framework.

    * Changes to Django models will provide new functionality via Djoonga Admin.
    * Changes to Django models will cause database schema changes, migration of these changes will be handled by Django South.
    * The modified database schema will become available to Joomla via Djoonga plugin that will allow the PHP developer to access information from expended fields.
    * Interaction with expended fields might be read or read/write ( this has not been determined yet )

Phase 3: Scaffolding of Joomla Components
=========================================
The goal of this phase is to enable Joomla! service providers to create custom
Joomla applications that will be administered through Django Admin, but are
visually presented to the user through Joomla.

    * Developer will follow the process of creating a Django application, this will provide administration of content from Django admin
    * Once the models are defined, Djoonga will build Joomla component that can be installed on Joomla
    * The component will be scaffolded according to Joomla!'s best practices and MVC pattern