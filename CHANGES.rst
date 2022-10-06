Changes
=======

1.7 (2022-10-06)
----------------

- Introduce new method ``set_value_index`` to allow correct custom indexing
  in index hooks.
  [lenadax]


1.6.1 (2019-11-20)
------------------

- Use ``bdajax.register`` for registering binder function.
  [rnix]


1.6 (2019-07-31)
----------------

- Add additional JS hooks when array gets modified. Provided hooks are now
  ``before_add``, ``add``, ``remove``, ``before_up``, ``up``, ``before_down``,
  ``down`` and ``index``.
  [rnix]

- Add ``array_display_renderer``.
  [rnix]


1.5 (2018-07-16)
----------------

- Python 3 compatibility.
  [rnix]

- Convert doctests to unittests.
  [rnix]


1.4 (2016-09-09)
----------------

- Add dedicated CSS for ``plone5`` theme provided by ``yafowil.plone``.
  [rnix, 2016-06-28]

- Use ``yafowil.utils.entry_point`` decorator.
  [rnix, 2016-06-27]

- Minor bootstrap theme CSS changes.
  [rnix, 2016-06-27]


1.3.1 (2015-06-25)
------------------

- Resolve JSHint errors and warnings.
  [thet]

- Fix CSS for displaying icons in default theme.
  [marfago]


1.3 (2015-01-23)
----------------

- Fix ``mark_disabled`` function.
  [rnix]

- Adopt to ``yafowil.bootstrap`` 1.2.
  [rnix]


1.2.1
-----

- Do not hook ``array_display_proxy`` if ``display_proxy`` proerty set on
  widget attributes.
  [rnix, 2012-10-26]

- Use ``yafowil.utils.attr_value`` wherever possible.
  [rnix, 2012-10-25]


1.2
---

- Add ``array`` CSS class to array wrapper DOM element if not present (may
  happen if ``class`` property for array blueprint gets overwritten). Javascript
  depends on this CSS class.
  [rnix, 2012-07-25]

- Adopt resource providing.
  [rnix, 2012-06-12]

- Remove example app.
  [rnix, 2012-06-12]


1.1
---

- pass parent to array extractor explicit extract call (as compound extractor 
  does).
  [jensens, 2012-05-20]

- Handle ``required`` property in ``array`` blueprint.
  [rnix, 2012-04-19]

- Handle ``display`` mode and ``disabled`` property for leaf array children.
  [rnix, 2012-04-17]

- Introduce ``add``, ``remove``, ``sort`` and ``static`` properties for
  ``array`` blueprint.
  [rnix, 2012-04-13]


1.0
---

- Implement yafowil 1.3 entry_point registration
  [agitator, 2012-02-15]


0.9
---

- Make it work
  [rnix]
