
History
=======

1.4 (unreleased)
----------------

- Use ``yafowil.utils.entry_point`` decorator.
  [rnix]

- Minor bootstrap theme CSS changes.
  [rnix, 2016-06-27]

- Explicitely define ``font-family`` for each icon in bootstrap theme to avoid
  overwriting with CSS wild card selectors.
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
