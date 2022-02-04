
Select Menus Explained
=======================

How are Select Menus structured?
---------------------------------

Select Menus(:class:`tungsten.SelectMenu`) methods work by accessing an item from the :attr:`options` using indexes. 
This library does allow setting a custom ID for select menus, but it doesn't really change anything.
The indexes function the same way as list indexes do, starting at 0.

Methods
-------

Besides the :meth:`edit_option<tungsten.SelectMenu.edit_option>` method used in the :ref:`Getting Started<getting-started>` section, 
there are more methods that can add more functionality to your :meth:`select_menu_callback<tungsten.Components.select_menu_callback>`.
You can find the :class:`here<tungsten.SelectMenu>`.