Import requirements::

    >>> import yafowil.loader
    >>> import yafowil.widget.array
    >>> from yafowil.base import factory

Create array with missing entry definition::

    >>> form = factory(
    ...     'form',
    ...     name='myform',
    ...     props={'action': 'myaction'})
    >>> form['myarray'] = factory(
    ...     'array',
    ...     props={'label': 'My Array'})
    >>> pxml(form())
    Traceback (most recent call last):
      ...
    Exception: Empty array widget defined

Create empty array widget::
    
    >>> form = factory(
    ...     'form',
    ...     name='myform',
    ...     props={'action': 'myaction'})
    >>> form['myarray'] = factory(
    ...     'array',
    ...     props={'label': 'My Array'})
    >>> form['myarray']['myfield'] = factory(
    ...     'field:label:text',
    ...     props={'label': 'My Field'})
    
    >>> form.printtree()
    <class 'yafowil.base.Widget'>: myform
      <class 'yafowil.base.Widget'>: myarray
        <class 'yafowil.base.Widget'>: table
          <class 'yafowil.base.Widget'>: head
            <class 'yafowil.base.Widget'>: row
              <class 'yafowil.base.Widget'>: label
              <class 'yafowil.base.Widget'>: actions
          <class 'yafowil.base.Widget'>: body
        <class 'yafowil.base.Widget'>: myfield
    
    >>> pxml(form())
    <form action="myaction" enctype="multipart/form-data" id="form-myform" method="post" novalidate="novalidate">
      <div class="array array-add array-remove array-sort" id="array-myform-myarray">
        <table>
          <thead>
            <tr>
              <th>My Array</th>
              <th>
                <div class="array_actions">
                  <a class="array_row_add" href="#">
                    <i class="icon-plus-sign">&#160;</i>
                  </a>
                </div>
              </th>
            </tr>
          </thead>
          <tbody/>
        </table>
        <div class="arraytemplate">
          <div class="field" id="field-myform-myarray-TEMPLATE">
            <label for="input-myform-myarray-TEMPLATE">My Field</label>
            <input class="text" id="input-myform-myarray-TEMPLATE" name="myform.myarray.TEMPLATE" type="text" value=""/>
          </div>
        </div>
      </div>
    </form>
    <BLANKLINE>

Create empty array widget with add action disabled::

    >>> form['myarray'] = factory(
    ...     'array',
    ...     props={
    ...         'label': 'My Array',
    ...         'add': False,
    ...     })
    >>> form['myarray']['myfield'] = factory(
    ...     'field:label:text',
    ...     props={'label': 'My Field'})
    
    >>> form.printtree()
    <class 'yafowil.base.Widget'>: myform
      <class 'yafowil.base.Widget'>: myarray
        <class 'yafowil.base.Widget'>: table
          <class 'yafowil.base.Widget'>: head
            <class 'yafowil.base.Widget'>: row
              <class 'yafowil.base.Widget'>: label
              <class 'yafowil.base.Widget'>: actions
          <class 'yafowil.base.Widget'>: body
        <class 'yafowil.base.Widget'>: myfield
    
    >>> pxml(form())
    <form action="myaction" enctype="multipart/form-data" id="form-myform" method="post" novalidate="novalidate">
      <div class="array array-remove array-sort" id="array-myform-myarray">
        <table>
          <thead>
            <tr>
              <th>My Array</th>
              <th>
                <div class="array_actions"/>
              </th>
            </tr>
          </thead>
          <tbody/>
        </table>
      </div>
    </form>
    <BLANKLINE>

Create array widget with overwritten class property. if CSS class 'array'
missing, it gets added transparently::

    >>> form['myarray'] = factory(
    ...     'array',
    ...     props={
    ...         'label': 'My Array',
    ...         'class': 'specialclass',
    ...     })
    >>> form['myarray']['myfield'] = factory(
    ...     'field:label:text',
    ...     props={'label': 'My Field'})
    
    >>> pxml(form())
    <form action="myaction" enctype="multipart/form-data" id="form-myform" method="post" novalidate="novalidate">
      <div class="array specialclass array-add array-remove array-sort" id="array-myform-myarray">
        <table>
          ...
        </table>
        <div class="arraytemplate">
          ...
        </div>
      </div>
    </form>
    <BLANKLINE>

Display mode is not implemented yet::

    >>> form['myarray'].mode = 'display'
    >>> pxml(form())
    Traceback (most recent call last):
      ...
    NotImplementedError: yafowil.widget.array: Display mode not implemented yet

Create empty static array widget::

    >>> form['myarray'] = factory(
    ...     'array',
    ...     props={
    ...         'label': 'My Array',
    ...         'static': True,
    ...     })
    >>> form['myarray']['myfield'] = factory(
    ...     'field:label:text',
    ...     props={'label': 'My Field'})
    
    >>> form.printtree()
     <class 'yafowil.base.Widget'>: myform
      <class 'yafowil.base.Widget'>: myarray
        <class 'yafowil.base.Widget'>: table
          <class 'yafowil.base.Widget'>: head
            <class 'yafowil.base.Widget'>: row
              <class 'yafowil.base.Widget'>: label
          <class 'yafowil.base.Widget'>: body
        <class 'yafowil.base.Widget'>: myfield
    
    >>> pxml(form())
    <form action="myaction" enctype="multipart/form-data" id="form-myform" method="post" novalidate="novalidate">
      <div class="array array-static" id="array-myform-myarray">
        <table>
          <thead>
            <tr>
              <th>My Array</th>
            </tr>
          </thead>
          <tbody/>
        </table>
      </div>
    </form>
    <BLANKLINE>

Create empty array widget with compound as template widget. If compound is
used as array template, this must not be structural::

    >>> form['myarray'] = factory(
    ...     'array',
    ...     props={'label': 'My Compound Array'})
    >>> form['myarray']['mycompound'] = factory(
    ...     'compound',
    ...     props={'structural': True})
    >>> pxml(form())
    Traceback (most recent call last):
      ...
    Exception: Compound templates for arrays must not be structural.

Now with valid compound template::

    >>> form['myarray'] = factory(
    ...     'array',
    ...     props={'label': 'My Compound Array'})
    >>> form['myarray']['mycompound'] = factory('compound')
    >>> form['myarray']['mycompound']['f1'] = factory(
    ...     'field:label:text',
    ...     props={'label': 'F1'})
    >>> form['myarray']['mycompound']['f2'] = factory(
    ...     'field:label:text',
    ...     props={'label': 'F2'})
    
    >>> form.printtree()
    <class 'yafowil.base.Widget'>: myform
      <class 'yafowil.base.Widget'>: myarray
        <class 'yafowil.base.Widget'>: table
          <class 'yafowil.base.Widget'>: head
            <class 'yafowil.base.Widget'>: row
              <class 'yafowil.base.Widget'>: label
              <class 'yafowil.base.Widget'>: actions
          <class 'yafowil.base.Widget'>: body
        <class 'yafowil.base.Widget'>: mycompound
          <class 'yafowil.base.Widget'>: f1
          <class 'yafowil.base.Widget'>: f2
    
    >>> pxml(form())
    <form action="myaction" enctype="multipart/form-data" id="form-myform" method="post" novalidate="novalidate">
      <div class="array array-add array-remove array-sort" id="array-myform-myarray">
        <table>
          ...
        </table>
        <div class="arraytemplate">
          <div class="field" id="field-myform-myarray-TEMPLATE-f1">
            <label for="input-myform-myarray-TEMPLATE-f1">F1</label>
            <input class="text" id="input-myform-myarray-TEMPLATE-f1" name="myform.myarray.TEMPLATE.f1" type="text" value=""/>
          </div>
          <div class="field" id="field-myform-myarray-TEMPLATE-f2">
            <label for="input-myform-myarray-TEMPLATE-f2">F2</label>
            <input class="text" id="input-myform-myarray-TEMPLATE-f2" name="myform.myarray.TEMPLATE.f2" type="text" value=""/>
          </div>
        </div>
      </div>
    </form>
    <BLANKLINE>
    
    >>> del form['myarray']

Create empty array widget with another array as template widget::

    >>> form['myarrayarray'] = factory(
    ...     'array',
    ...     props={'label': 'My Array Array'})
    >>> form['myarrayarray']['myarray'] = factory(
    ...     'array',
    ...     props={'label': 'My Array'})
    >>> form['myarrayarray']['myarray']['myfield'] = factory(
    ...     'field:label:text',
    ...     props={'label': 'My Field'})
    
    >>> form.printtree()
    <class 'yafowil.base.Widget'>: myform
      <class 'yafowil.base.Widget'>: myarrayarray
        <class 'yafowil.base.Widget'>: table
          <class 'yafowil.base.Widget'>: head
            <class 'yafowil.base.Widget'>: row
              <class 'yafowil.base.Widget'>: label
              <class 'yafowil.base.Widget'>: actions
          <class 'yafowil.base.Widget'>: body
        <class 'yafowil.base.Widget'>: myarray
          <class 'yafowil.base.Widget'>: table
            <class 'yafowil.base.Widget'>: head
              <class 'yafowil.base.Widget'>: row
                <class 'yafowil.base.Widget'>: label
                <class 'yafowil.base.Widget'>: actions
            <class 'yafowil.base.Widget'>: body
          <class 'yafowil.base.Widget'>: myfield
    
    >>> pxml(form())
    <form action="myaction" enctype="multipart/form-data" id="form-myform" method="post" novalidate="novalidate">
      <div class="array array-add array-remove array-sort" id="array-myform-myarrayarray">
        <table>
          ...
        </table>
        <div class="arraytemplate">
          <div class="array array-add array-remove array-sort" id="array-myform-myarrayarray-TEMPLATE">
            <table>
              ...
            </table>
            <div class="arraytemplate">
              <div class="field" id="field-myform-myarrayarray-TEMPLATE-TEMPLATE">
                <label for="input-myform-myarrayarray-TEMPLATE-TEMPLATE">My Field</label>
                <input class="text" id="input-myform-myarrayarray-TEMPLATE-TEMPLATE" name="myform.myarrayarray.TEMPLATE.TEMPLATE" type="text" value=""/>
              </div>
            </div>
          </div>
        </div>
      </div>
    </form>
    <BLANKLINE>
    
    >>> del form['myarrayarray']

Create array widget with invalid preset value::

    >>> form['myarray'] = factory(
    ...     'array',
    ...     value=object(),
    ...     props={'label': 'My Array'})
    >>> form['myarray']['myfield'] = factory(
    ...     'field:label:text',
    ...     props={'label': 'My Field'})
    >>> pxml(form())
    Traceback (most recent call last):
      ...
    ValueError: Expected list or dict as value. Got '<type 'object'>'

Create array widget with preset values.

Value as list. Disable ``add``::
    
    >>> form['myarray'] = factory(
    ...     'array',
    ...     value=['1', '2'],
    ...     props={
    ...         'label': 'My Array',
    ...         'add': False,
    ...     })
    >>> form['myarray']['myfield'] = factory(
    ...     'field:label:text',
    ...     props={'label': 'My Field'})
    >>> pxml(form())
    <form action="myaction" enctype="multipart/form-data" id="form-myform" method="post" novalidate="novalidate">
      <div class="array array-remove array-sort" id="array-myform-myarray">
        <table>
          <thead>
            <tr>
              <th>My Array</th>
              <th>
                <div class="array_actions"/>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="widget">
                <div class="field" id="field-myform-myarray-0">
                  <label for="input-myform-myarray-0">My Field</label>
                  <input class="text" id="input-myform-myarray-0" name="myform.myarray.0" type="text" value="1"/>
                </div>
              </td>
              <td class="actions">
                <div class="array_actions">
                  <a class="array_row_remove" href="#">
                    <i class="icon-minus-sign">&#160;</i>
                  </a>
                  <a class="array_row_up" href="#">
                    <i class="icon-circle-arrow-up">&#160;</i>
                  </a>
                  <a class="array_row_down" href="#">
                    <i class="icon-circle-arrow-down">&#160;</i>
                  </a>
                </div>
              </td>
            </tr>
            <tr>
              ...
            </tr>
          </tbody>
        </table>
      </div>
    </form>
    <BLANKLINE>

Value as list. Disable ``sort``::

    >>> form['myarray'] = factory(
    ...     'array',
    ...     value=['1', '2'],
    ...     props={
    ...         'label': 'My Array',
    ...         'sort': False,
    ...     })
    >>> form['myarray']['myfield'] = factory(
    ...     'field:label:text',
    ...     props={'label': 'My Field'})
    >>> pxml(form())
    <form action="myaction" enctype="multipart/form-data" id="form-myform" method="post" novalidate="novalidate">
      <div class="array array-add array-remove" id="array-myform-myarray">
        <table>
          <thead>
            <tr>
              <th>My Array</th>
              <th>
                <div class="array_actions">
                  ...
                </div>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="widget">
                <div class="field" id="field-myform-myarray-0">
                  <label for="input-myform-myarray-0">My Field</label>
                  <input class="text" id="input-myform-myarray-0" name="myform.myarray.0" type="text" value="1"/>
                </div>
              </td>
              <td class="actions">
                <div class="array_actions">
                  <a class="array_row_add" href="#">
                    <i class="icon-plus-sign">&#160;</i>
                  </a>
                  <a class="array_row_remove" href="#">
                    <i class="icon-minus-sign">&#160;</i>
                  </a>
                </div>
              </td>
            </tr>
            ...
          </tbody>
        </table>
        <div class="arraytemplate">
          ...
        </div>
      </div>
    </form>
    <BLANKLINE>

Value as list. All actions disabled. Actions col still rendered::
    
    >>> form['myarray'] = factory(
    ...     'array',
    ...     value=['1', '2'],
    ...     props={
    ...         'label': 'My Array',
    ...         'add': False,
    ...         'remove': False,
    ...         'sort': False,
    ...     })
    >>> form['myarray']['myfield'] = factory(
    ...     'field:label:text',
    ...     props={'label': 'My Field'})
    >>> pxml(form())
    <form action="myaction" enctype="multipart/form-data" id="form-myform" method="post" novalidate="novalidate">
      <div class="array" id="array-myform-myarray">
        <table>
          <thead>
            <tr>
              <th>My Array</th>
              <th>
                <div class="array_actions"/>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="widget">
                <div class="field" id="field-myform-myarray-0">
                  <label for="input-myform-myarray-0">My Field</label>
                  <input class="text" id="input-myform-myarray-0" name="myform.myarray.0" type="text" value="1"/>
                </div>
              </td>
              <td class="actions">
                <div class="array_actions"/>
              </td>
            </tr>
            ...
          </tbody>
        </table>
      </div>
    </form>
    <BLANKLINE>

Value as list. Set ``static`` property to ``True``. Actions col is skipped::
    
    >>> form['myarray'] = factory(
    ...     'array',
    ...     value=['1', '2'],
    ...     props={
    ...         'label': 'My Array',
    ...         'static': True,
    ...     })
    >>> form['myarray']['myfield'] = factory(
    ...     'field:label:text',
    ...     props={'label': 'My Field'})
    
    >>> form.printtree()
    <class 'yafowil.base.Widget'>: myform
      <class 'yafowil.base.Widget'>: myarray
        <class 'yafowil.base.Widget'>: table
          <class 'yafowil.base.Widget'>: head
            <class 'yafowil.base.Widget'>: row
              <class 'yafowil.base.Widget'>: label
          <class 'yafowil.base.Widget'>: body
        <class 'yafowil.base.Widget'>: myfield
    
    >>> pxml(form())
    <form action="myaction" enctype="multipart/form-data" id="form-myform" method="post" novalidate="novalidate">
      <div class="array array-static" id="array-myform-myarray">
        <table>
          <thead>
            <tr>
              <th>My Array</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="widget">
                <div class="field" id="field-myform-myarray-0">
                  <label for="input-myform-myarray-0">My Field</label>
                  <input class="text" id="input-myform-myarray-0" name="myform.myarray.0" type="text" value="1"/>
                </div>
              </td>
            </tr>
            <tr>
              <td class="widget">
                <div class="field" id="field-myform-myarray-1">
                  <label for="input-myform-myarray-1">My Field</label>
                  <input class="text" id="input-myform-myarray-1" name="myform.myarray.1" type="text" value="2"/>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </form>
    <BLANKLINE>

Value as list::
    
    >>> form['myarray'] = factory(
    ...     'array',
    ...     value=['1', '2'],
    ...     props={'label': 'My Array'})
    >>> form['myarray']['myfield'] = factory(
    ...     'field:label:text',
    ...     props={'label': 'My Field'})
    >>> pxml(form())
    <form action="myaction" enctype="multipart/form-data" id="form-myform" method="post" novalidate="novalidate">
      <div class="array array-add array-remove array-sort" id="array-myform-myarray">
        <table>
          <thead>
            ...
          </thead>
          <tbody>
            <tr>
              <td class="widget">
                <div class="field" id="field-myform-myarray-0">
                  <label for="input-myform-myarray-0">My Field</label>
                  <input class="text" id="input-myform-myarray-0" name="myform.myarray.0" type="text" value="1"/>
                </div>
              </td>
              <td class="actions">
                <div class="array_actions">
                  <a class="array_row_add" href="#">
                    <i class="icon-plus-sign">&#160;</i>
                  </a>
                  <a class="array_row_remove" href="#">
                    <i class="icon-minus-sign">&#160;</i>
                  </a>
                  <a class="array_row_up" href="#">
                    <i class="icon-circle-arrow-up">&#160;</i>
                  </a>
                  <a class="array_row_down" href="#">
                    <i class="icon-circle-arrow-down">&#160;</i>
                  </a>
                </div>
              </td>
            </tr>
            <tr>
              <td class="widget">
                <div class="field" id="field-myform-myarray-1">
                  <label for="input-myform-myarray-1">My Field</label>
                  <input class="text" id="input-myform-myarray-1" name="myform.myarray.1" type="text" value="2"/>
                </div>
              </td>
              <td class="actions">
                ...
              </td>
            </tr>
          </tbody>
        </table>
        <div class="arraytemplate">
          ...
        </div>
      </div>
    </form>
    <BLANKLINE>

Value as dict, must contain indices as keys::

    >>> from odict import odict
    >>> value = odict()
    >>> value['a'] = '1'
    >>> form['myarray'] = factory(
    ...     'array',
    ...     value=value,
    ...     props={'label': 'My Array'})
    >>> form['myarray']['myfield'] = factory(
    ...     'field:label:text',
    ...     props={'label': 'My Field'})
    >>> pxml(form())
    Traceback (most recent call last):
      ...
    Exception: Array value error. invalid literal for int() with base 10: 'a'

Valid dict value::

    >>> value = odict()
    >>> value['0'] = '1'
    >>> value['1'] = '2'
    >>> form['myarray'] = factory(
    ...     'array',
    ...     value=value,
    ...     props={'label': 'My Array'})
    >>> form['myarray']['myfield'] = factory(
    ...     'field:label:text',
    ...     props={'label': 'My Field'})
    >>> pxml(form())
    <form action="myaction" enctype="multipart/form-data" id="form-myform" method="post" novalidate="novalidate">
      <div class="array array-add array-remove array-sort" id="array-myform-myarray">
        <table>
          <thead>
            ...
          </thead>
          <tbody>
            <tr>
              <td class="widget">
                <div class="field" id="field-myform-myarray-0">
                  <label for="input-myform-myarray-0">My Field</label>
                  <input class="text" id="input-myform-myarray-0" name="myform.myarray.0" type="text" value="1"/>
                </div>
              </td>
              <td class="actions">
                ...
              </td>
            </tr>
            <tr>
              ...
            </tr>
          </tbody>
        </table>
        <div class="arraytemplate">
          ...
        </div>
      </div>
    </form>
    <BLANKLINE>

Create array widget with compounds, default values set::

    >>> form['myarray'] = factory(
    ...     'array',
    ...     value=[
    ...         {
    ...             'f1': 'Value 1.1 F1',
    ...             'f2': 'Value 1.2 F2',
    ...         },
    ...         {
    ...             'f1': 'Value 2.1 F1',
    ...             'f2': 'Value 2.2 F2',
    ...         }
    ...     ],
    ...     props={'label': 'My Compound Array'})
    >>> form['myarray']['mycompound'] = factory('compound')
    >>> form['myarray']['mycompound']['f1'] = factory(
    ...     'field:label:text',
    ...     props={'label': 'F1'})
    >>> form['myarray']['mycompound']['f2'] = factory(
    ...     'field:label:text',
    ...     props={'label': 'F2'})
    >>> rendered = form()
    >>> pxml(rendered)
    <form action="myaction" enctype="multipart/form-data" id="form-myform" method="post" novalidate="novalidate">
      <div class="array array-add array-remove array-sort" id="array-myform-myarray">
        <table>
          <thead>
            ...
          </thead>
          <tbody>
            <tr>
              <td class="widget">
                <div class="field" id="field-myform-myarray-0-f1">
                  <label for="input-myform-myarray-0-f1">F1</label>
                  <input class="text" id="input-myform-myarray-0-f1" name="myform.myarray.0.f1" type="text" value="Value 1.1 F1"/>
                </div>
                <div class="field" id="field-myform-myarray-0-f2">
                  <label for="input-myform-myarray-0-f2">F2</label>
                  <input class="text" id="input-myform-myarray-0-f2" name="myform.myarray.0.f2" type="text" value="Value 1.2 F2"/>
                </div>
              </td>
              <td class="actions">
                ...
              </td>
            </tr>
            <tr>
              <td class="widget">
                <div class="field" id="field-myform-myarray-1-f1">
                  <label for="input-myform-myarray-1-f1">F1</label>
                  <input class="text" id="input-myform-myarray-1-f1" name="myform.myarray.1.f1" type="text" value="Value 2.1 F1"/>
                </div>
                <div class="field" id="field-myform-myarray-1-f2">
                  <label for="input-myform-myarray-1-f2">F2</label>
                  <input class="text" id="input-myform-myarray-1-f2" name="myform.myarray.1.f2" type="text" value="Value 2.2 F2"/>
                </div>
              </td>
              <td class="actions">
                ...
              </td>
            </tr>
          </tbody>
        </table>
        <div class="arraytemplate">
          ...
        </div>
      </div>
    </form>
    <BLANKLINE>

Create array widget with array, default values set as list::

    >>> form['myarray'] = factory(
    ...     'array',
    ...     value=[
    ...         ['1', '2'],
    ...         ['4', '5'],
    ...     ],
    ...     props={'label': 'My Array Array'})
    >>> form['myarray']['subarray'] = factory(
    ...     'array',
    ...     props={'label': 'Subrray'})
    >>> form['myarray']['subarray']['myfield'] = factory(
    ...     'field:label:text',
    ...     props={'label': 'My Field'})
    >>> rendered = form()
    >>> pxml(rendered)
    <form action="myaction" enctype="multipart/form-data" id="form-myform" method="post" novalidate="novalidate">
      <div class="array array-add array-remove array-sort" id="array-myform-myarray">
        <table>
          <thead>
            ...
          </thead>
          <tbody>
            <tr>
              <td class="widget">
                <div class="array array-add array-remove array-sort" id="array-myform-myarray-0">
                  <table>
                    <thead>
                      <tr>
                        <th>Subrray</th>
                        ...
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td class="widget">
                          <div class="field" id="field-myform-myarray-0-0">
                            <label for="input-myform-myarray-0-0">My Field</label>
                            <input class="text" id="input-myform-myarray-0-0" name="myform.myarray.0.0" type="text" value="1"/>
                          </div>
                        </td>
                        <td class="actions">
                          ...
                        </td>
                      </tr>
                      <tr>
                        <td class="widget">
                          <div class="field" id="field-myform-myarray-0-1">
                            <label for="input-myform-myarray-0-1">My Field</label>
                            <input class="text" id="input-myform-myarray-0-1" name="myform.myarray.0.1" type="text" value="2"/>
                          </div>
                        </td>
                        <td class="actions">
                          ...
                        </td>
                      </tr>
                    </tbody>
                  </table>
                  <div class="arraytemplate">
                    <div class="field" id="field-myform-myarray-0-TEMPLATE">
                      <label for="input-myform-myarray-0-TEMPLATE">My Field</label>
                      <input class="text" id="input-myform-myarray-0-TEMPLATE" name="myform.myarray.0.TEMPLATE" type="text" value=""/>
                    </div>
                  </div>
                </div>
              </td>
              <td class="actions">
                ...
              </td>
            </tr>
            <tr>
              <td class="widget">
                <div class="array array-add array-remove array-sort" id="array-myform-myarray-1">
                  ...
                </div>
              </td>
              <td class="actions">
                ...
              </td>
            </tr>
          </tbody>
        </table>
        <div class="arraytemplate">
          <div class="array array-add array-remove array-sort" id="array-myform-myarray-TEMPLATE">
            <table>
              <thead>
                <tr>
                  <th>Subrray</th>
                  ...
                </tr>
              </thead>
              <tbody/>
            </table>
            <div class="arraytemplate">
              ...
            </div>
          </div>
        </div>
      </div>
    </form>
    <BLANKLINE>

Create array widget with array, default values set as dict::

    >>> form['myarray'] = factory(
    ...     'array',
    ...     value={
    ...         '0': {'0': '1', '1': '2'},
    ...         '1': {'0': '4', '1': '5'},
    ...     },
    ...     props={'label': 'My Array Array'})
    >>> form['myarray']['subarray'] = factory(
    ...     'array',
    ...     props={'label': 'Subrray'})
    >>> form['myarray']['subarray']['myfield'] = factory(
    ...     'field:label:text',
    ...     props={'label': 'My Field'})
    >>> form() == rendered
    True

Create array widget with array, default values mixed::

    >>> form['myarray'] = factory(
    ...     'array',
    ...     value={
    ...         '0': ['1', '2'],
    ...         '1': ['4', '5'],
    ...     },
    ...     props={'label': 'My Array Array'})
    >>> form['myarray']['subarray'] = factory(
    ...     'array',
    ...     props={'label': 'Subrray'})
    >>> form['myarray']['subarray']['myfield'] = factory(
    ...     'field:label:text',
    ...     props={'label': 'My Field'})
    >>> form() == rendered
    True
    
    >>> form['myarray'] = factory(
    ...     'array',
    ...     value=[
    ...         {'0': '1', '1': '2'},
    ...         {'0': '4', '1': '5'},
    ...     ],
    ...     props={'label': 'My Array Array'})
    >>> form['myarray']['subarray'] = factory(
    ...     'array',
    ...     props={'label': 'Subrray'})
    >>> form['myarray']['subarray']['myfield'] = factory(
    ...     'field:label:text',
    ...     props={'label': 'My Field'})
    >>> form() == rendered
    True

Create array widget with array with compound, default values as list::

    >>> form['myarray'] = factory(
    ...     'array',
    ...     value=[
    ...         [
    ...             {
    ...                 'f1': 'Value 0.0 F1',
    ...                 'f2': 'Value 0.0 F2',
    ...             },
    ...             {
    ...                 'f1': 'Value 0.1 F1',
    ...                 'f2': 'Value 0.1 F2',
    ...             },
    ...         ],
    ...     ],
    ...     props={'label': 'My Compound Array'})
    >>> form['myarray']['subarray'] = factory(
    ...     'array',
    ...     props={'label': 'Subarray'})
    >>> form['myarray']['subarray']['compoundinsub'] = factory('compound')
    >>> form['myarray']['subarray']['compoundinsub']['f1'] = factory(
    ...     'field:label:text',
    ...     props={'label': 'F1'})
    >>> form['myarray']['subarray']['compoundinsub']['f2'] = factory(
    ...     'field:label:text',
    ...     props={'label': 'F2'})
    
    >>> form.printtree()
    <class 'yafowil.base.Widget'>: myform
      <class 'yafowil.base.Widget'>: myarray
        <class 'yafowil.base.Widget'>: table
          <class 'yafowil.base.Widget'>: head
            <class 'yafowil.base.Widget'>: row
              <class 'yafowil.base.Widget'>: label
              <class 'yafowil.base.Widget'>: actions
          <class 'yafowil.base.Widget'>: body
        <class 'yafowil.base.Widget'>: subarray
          <class 'yafowil.base.Widget'>: table
            <class 'yafowil.base.Widget'>: head
              <class 'yafowil.base.Widget'>: row
                <class 'yafowil.base.Widget'>: label
                <class 'yafowil.base.Widget'>: actions
            <class 'yafowil.base.Widget'>: body
          <class 'yafowil.base.Widget'>: compoundinsub
            <class 'yafowil.base.Widget'>: f1
            <class 'yafowil.base.Widget'>: f2
    
    >>> rendered = form()
    >>> pxml(rendered)
    <form action="myaction" enctype="multipart/form-data" id="form-myform" method="post" novalidate="novalidate">
      <div class="array array-add array-remove array-sort" id="array-myform-myarray">
        <table>
          <thead>
            <tr>
              <th>My Compound Array</th>
              ...
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="widget">
                <div class="array array-add array-remove array-sort" id="array-myform-myarray-0">
                  <table>
                    <thead>
                      <tr>
                        <th>Subarray</th>
                        ...
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td class="widget">
                          <div class="field" id="field-myform-myarray-0-0-f1">
                            <label for="input-myform-myarray-0-0-f1">F1</label>
                            <input class="text" id="input-myform-myarray-0-0-f1" name="myform.myarray.0.0.f1" type="text" value="Value 0.0 F1"/>
                          </div>
                          <div class="field" id="field-myform-myarray-0-0-f2">
                            <label for="input-myform-myarray-0-0-f2">F2</label>
                            <input class="text" id="input-myform-myarray-0-0-f2" name="myform.myarray.0.0.f2" type="text" value="Value 0.0 F2"/>
                          </div>
                        </td>
                        <td class="actions">
                          ...
                        </td>
                      </tr>
                      <tr>
                        <td class="widget">
                          <div class="field" id="field-myform-myarray-0-1-f1">
                            <label for="input-myform-myarray-0-1-f1">F1</label>
                            <input class="text" id="input-myform-myarray-0-1-f1" name="myform.myarray.0.1.f1" type="text" value="Value 0.1 F1"/>
                          </div>
                          <div class="field" id="field-myform-myarray-0-1-f2">
                            <label for="input-myform-myarray-0-1-f2">F2</label>
                            <input class="text" id="input-myform-myarray-0-1-f2" name="myform.myarray.0.1.f2" type="text" value="Value 0.1 F2"/>
                          </div>
                        </td>
                        <td class="actions">
                          ...
                        </td>
                      </tr>
                    </tbody>
                  </table>
                  <div class="arraytemplate">
                    ...
                  </div>
                </div>
              </td>
              <td class="actions">
                ...
              </td>
            </tr>
          </tbody>
        </table>
        <div class="arraytemplate">
          <div class="array array-add array-remove array-sort" id="array-myform-myarray-TEMPLATE">
            <table>
              <thead>
                <tr>
                  <th>Subarray</th>
                  ...
                </tr>
              </thead>
              <tbody/>
            </table>
            <div class="arraytemplate">
              <div class="field" id="field-myform-myarray-TEMPLATE-TEMPLATE-f1">
                <label for="input-myform-myarray-TEMPLATE-TEMPLATE-f1">F1</label>
                <input class="text" id="input-myform-myarray-TEMPLATE-TEMPLATE-f1" name="myform.myarray.TEMPLATE.TEMPLATE.f1" type="text" value=""/>
              </div>
              <div class="field" id="field-myform-myarray-TEMPLATE-TEMPLATE-f2">
                <label for="input-myform-myarray-TEMPLATE-TEMPLATE-f2">F2</label>
                <input class="text" id="input-myform-myarray-TEMPLATE-TEMPLATE-f2" name="myform.myarray.TEMPLATE.TEMPLATE.f2" type="text" value=""/>
              </div>
            </div>
          </div>
        </div>
      </div>
    </form>
    <BLANKLINE>

Create array widget with array with compound, default values as dict::

    >>> form['myarray'] = factory(
    ...     'array',
    ...     value={
    ...         '0': {
    ...             '0': {
    ...                 'f1': 'Value 0.0 F1',
    ...                 'f2': 'Value 0.0 F2',
    ...             },
    ...             '1': {
    ...                 'f1': 'Value 0.1 F1',
    ...                 'f2': 'Value 0.1 F2',
    ...             },
    ...         },
    ...     },
    ...     props={'label': 'My Compound Array'})
    >>> form['myarray']['subarray'] = factory(
    ...     'array',
    ...     props={'label': 'Subarray'})
    >>> form['myarray']['subarray']['mycompound'] = factory('compound')
    >>> form['myarray']['subarray']['mycompound']['f1'] = factory(
    ...     'field:label:text',
    ...     props={'label': 'F1'})
    >>> form['myarray']['subarray']['mycompound']['f2'] = factory(
    ...     'field:label:text',
    ...     props={'label': 'F2'})
    >>> rendered == form()
    True

Create array widget with array with compound, default values mixed::

    >>> form['myarray'] = factory(
    ...     'array',
    ...     value=[
    ...         {
    ...             '0': {
    ...                 'f1': 'Value 0.0 F1',
    ...                 'f2': 'Value 0.0 F2',
    ...             },
    ...             '1': {
    ...                 'f1': 'Value 0.1 F1',
    ...                 'f2': 'Value 0.1 F2',
    ...             },
    ...         },
    ...     ],
    ...     props={'label': 'My Compound Array'})
    >>> form['myarray']['subarray'] = factory(
    ...     'array',
    ...     props={'label': 'Subarray'})
    >>> form['myarray']['subarray']['mycompound'] = factory('compound')
    >>> form['myarray']['subarray']['mycompound']['f1'] = factory(
    ...     'field:label:text',
    ...     props={'label': 'F1'})
    >>> form['myarray']['subarray']['mycompound']['f2'] = factory(
    ...     'field:label:text',
    ...     props={'label': 'F2'})
    >>> rendered == form()
    True

Array with single fields extraction::

    >>> form['myarray'] = factory(
    ...     'array',
    ...     props={'label': 'My Array'})
    >>> form['myarray']['myfield'] = factory(
    ...     'field:label:text',
    ...     props={'label': 'My Field'})
    >>> request = {
    ...     'myform.myarray.0': '1',
    ...     'myform.myarray.1': '2',
    ...     'myform.myarray.2': '3',
    ...     'myform.myarray.3': '4',
    ... }
    >>> data = form.extract(request=request)
    >>> data.printtree()
    <RuntimeData myform, value=<UNSET>, extracted=odict([('myarray', ['1', '2', '3', '4'])]) at ...>
      <RuntimeData myform.myarray, value=<UNSET>, extracted=['1', '2', '3', '4'] at ...>
        <RuntimeData myform.myarray.0, value=<UNSET>, extracted='1' at ...>
        <RuntimeData myform.myarray.1, value=<UNSET>, extracted='2' at ...>
        <RuntimeData myform.myarray.2, value=<UNSET>, extracted='3' at ...>
        <RuntimeData myform.myarray.3, value=<UNSET>, extracted='4' at ...>
    
    >>> data.extracted
    odict([('myarray', ['1', '2', '3', '4'])])
    
    >>> data['myarray'].extracted
    ['1', '2', '3', '4']
    
    >>> form['myarray'] = factory(
    ...     'array',
    ...     value=['4', '3', '2', '1'],
    ...     props={'label': 'My Array'})
    >>> form['myarray']['myfield'] = factory(
    ...     'field:label:text',
    ...     props={'label': 'My Field'})
    >>> data = form.extract(request=request)
    >>> data.printtree()
    <RuntimeData myform, value=<UNSET>, extracted=odict([('myarray', ['1', '2', '3', '4'])]) at ...>
      <RuntimeData myform.myarray, value=['4', '3', '2', '1'], extracted=['1', '2', '3', '4'] at ...>
        <RuntimeData myform.myarray.0, value=<UNSET>, extracted='1' at ...>
        <RuntimeData myform.myarray.1, value=<UNSET>, extracted='2' at ...>
        <RuntimeData myform.myarray.2, value=<UNSET>, extracted='3' at ...>
        <RuntimeData myform.myarray.3, value=<UNSET>, extracted='4' at ...>

Entries increased in UI::

    >>> request = {
    ...     'myform.myarray.0': '1',
    ...     'myform.myarray.1': '2',
    ...     'myform.myarray.2': '3',
    ...     'myform.myarray.3': '4',
    ...     'myform.myarray.4': '5',
    ... }
    >>> data = form.extract(request=request)
    >>> data.printtree()
    <RuntimeData myform, value=<UNSET>, extracted=odict([('myarray', ['1', '2', '3', '4', '5'])]) at ...>
      <RuntimeData myform.myarray, value=['4', '3', '2', '1'], extracted=['1', '2', '3', '4', '5'] at ...>
        <RuntimeData myform.myarray.0, value=<UNSET>, extracted='1' at ...>
        <RuntimeData myform.myarray.1, value=<UNSET>, extracted='2' at ...>
        <RuntimeData myform.myarray.2, value=<UNSET>, extracted='3' at ...>
        <RuntimeData myform.myarray.3, value=<UNSET>, extracted='4' at ...>
        <RuntimeData myform.myarray.4, value=<UNSET>, extracted='5' at ...>

Entries decreased in UI::

    >>> request = {
    ...     'myform.myarray.0': '1',
    ...     'myform.myarray.1': '2',
    ...     'myform.myarray.2': '3',
    ... }
    >>> data = form.extract(request=request)
    >>> data.printtree()
    <RuntimeData myform, value=<UNSET>, extracted=odict([('myarray', ['1', '2', '3'])]) at ...>
      <RuntimeData myform.myarray, value=['4', '3', '2', '1'], extracted=['1', '2', '3'] at ...>
        <RuntimeData myform.myarray.0, value=<UNSET>, extracted='1' at ...>
        <RuntimeData myform.myarray.1, value=<UNSET>, extracted='2' at ...>
        <RuntimeData myform.myarray.2, value=<UNSET>, extracted='3' at ...>

Required Array::

    >>> form['myarray'] = factory(
    ...     'error:array',
    ...     value=['4', '3', '2', '1'],
    ...     props={
    ...         'label': 'My Array',
    ...         'required': 'Array is required',
    ...     })
    >>> form['myarray']['myfield'] = factory(
    ...     'field:label:text',
    ...     props={'label': 'My Field'})
    >>> request = {}
    >>> data = form.extract(request=request)
    
    >>> data.printtree()
    <RuntimeData myform, value=<UNSET>, extracted=odict([('myarray', [])]) at ...>
      <RuntimeData myform.myarray, value=['4', '3', '2', '1'], extracted=[], 1 error(s) at ...>
    
    >>> pxml(form(data=data))
    <form action="myaction" enctype="multipart/form-data" id="form-myform" method="post" novalidate="novalidate">
      <div class="error">
        <div class="errormessage">Array is required</div>
        <div class="array error array-add array-remove array-sort" id="array-myform-myarray">
          ...
        </div>
      </div>
    </form>
    <BLANKLINE>

Array with compound fields extraction::

    >>> form['myarray'] = factory(
    ...     'array',
    ...     props={'label': 'My Compound Array'})
    >>> form['myarray']['mycompound'] = factory('compound')
    >>> form['myarray']['mycompound']['f1'] = factory(
    ...     'field:label:text',
    ...     props={'label': 'F1'})
    >>> form['myarray']['mycompound']['f2'] = factory(
    ...     'field:label:text',
    ...     props={'label': 'F2'})
    >>> request = {
    ...     'myform.myarray.0.f1': '1',
    ...     'myform.myarray.0.f2': '2',
    ...     'myform.myarray.1.f1': '3',
    ...     'myform.myarray.1.f2': '4',
    ... }
    >>> data = form.extract(request=request)
    >>> data.printtree()
    <RuntimeData myform, value=<UNSET>, extracted=odict([('myarray', [odict([('f1', '1'), ('f2', '2')]), odict([('f1', '3'), ('f2', '4')])])]) at ...>
      <RuntimeData myform.myarray, value=<UNSET>, extracted=[odict([('f1', '1'), ('f2', '2')]), odict([('f1', '3'), ('f2', '4')])] at ...>
        <RuntimeData myform.myarray.0, value=<UNSET>, extracted=odict([('f1', '1'), ('f2', '2')]) at ...>
          <RuntimeData myform.myarray.0.f1, value=<UNSET>, extracted='1' at ...>
          <RuntimeData myform.myarray.0.f2, value=<UNSET>, extracted='2' at ...>
        <RuntimeData myform.myarray.1, value=<UNSET>, extracted=odict([('f1', '3'), ('f2', '4')]) at ...>
          <RuntimeData myform.myarray.1.f1, value=<UNSET>, extracted='3' at ...>
          <RuntimeData myform.myarray.1.f2, value=<UNSET>, extracted='4' at ...>

Array in array with single fields extraction::

    >>> form['myarray'] = factory(
    ...     'array',
    ...     value=[
    ...         ['1', '2'],
    ...         ['4', '5'],
    ...     ],
    ...     props={'label': 'My Array Array'})
    >>> form['myarray']['subarray'] = factory(
    ...     'array',
    ...     props={'label': 'Subrray'})
    >>> form['myarray']['subarray']['myfield'] = factory(
    ...     'field:label:text',
    ...     props={'label': 'My Field'})
    >>> request = {
    ...     'myform.myarray.0.0': '1',
    ...     'myform.myarray.0.1': '2',
    ...     'myform.myarray.1.0': '3',
    ...     'myform.myarray.1.1': '4',
    ... }
    >>> data = form.extract(request=request)
    >>> data.printtree()
    <RuntimeData myform, value=<UNSET>, extracted=odict([('myarray', [['1', '2'], ['3', '4']])]) at ...>
      <RuntimeData myform.myarray, value=[['1', '2'], ['4', '5']], extracted=[['1', '2'], ['3', '4']] at ...>
        <RuntimeData myform.myarray.0, value=<UNSET>, extracted=['1', '2'] at ...>
          <RuntimeData myform.myarray.0.0, value=<UNSET>, extracted='1' at ...>
          <RuntimeData myform.myarray.0.1, value=<UNSET>, extracted='2' at ...>
        <RuntimeData myform.myarray.1, value=<UNSET>, extracted=['3', '4'] at ...>
          <RuntimeData myform.myarray.1.0, value=<UNSET>, extracted='3' at ...>
          <RuntimeData myform.myarray.1.1, value=<UNSET>, extracted='4' at ...>

Array in array with compound fields extraction::

    >>> form['myarray'] = factory(
    ...     'array',
    ...     props={'label': 'My Compound Array'})
    >>> form['myarray']['subarray'] = factory(
    ...     'array',
    ...     props={'label': 'Subarray'})
    >>> form['myarray']['subarray']['mycompound'] = factory('compound')
    >>> form['myarray']['subarray']['mycompound']['f1'] = factory(
    ...     'field:label:text',
    ...     props={'label': 'F1'})
    >>> form['myarray']['subarray']['mycompound']['f2'] = factory(
    ...     'field:label:text',
    ...     props={'label': 'F2'})
    >>> request = {
    ...     'myform.myarray.0.0.f1': '1',
    ...     'myform.myarray.0.0.f2': '2',
    ...     'myform.myarray.1.0.f1': '3',
    ...     'myform.myarray.1.0.f2': '4',
    ...     'myform.myarray.1.1.f1': '5',
    ...     'myform.myarray.1.1.f2': '6',
    ... }
    >>> data = form.extract(request=request)
    >>> data.printtree()
    <RuntimeData myform, value=<UNSET>, extracted=odict([('myarray', [[odict([('f1', '1'), ('f2', '2')])], [odict([('f1', '3'), ('f2', '4')]), odict([('f1', '5'), ('f2', '6')])]])]) at ...>
      <RuntimeData myform.myarray, value=<UNSET>, extracted=[[odict([('f1', '1'), ('f2', '2')])], [odict([('f1', '3'), ('f2', '4')]), odict([('f1', '5'), ('f2', '6')])]] at ...>
        <RuntimeData myform.myarray.0, value=<UNSET>, extracted=[odict([('f1', '1'), ('f2', '2')])] at ...>
          <RuntimeData myform.myarray.0.0, value=<UNSET>, extracted=odict([('f1', '1'), ('f2', '2')]) at ...>
            <RuntimeData myform.myarray.0.0.f1, value=<UNSET>, extracted='1' at ...>
            <RuntimeData myform.myarray.0.0.f2, value=<UNSET>, extracted='2' at ...>
        <RuntimeData myform.myarray.1, value=<UNSET>, extracted=[odict([('f1', '3'), ('f2', '4')]), odict([('f1', '5'), ('f2', '6')])] at ...>
          <RuntimeData myform.myarray.1.0, value=<UNSET>, extracted=odict([('f1', '3'), ('f2', '4')]) at ...>
            <RuntimeData myform.myarray.1.0.f1, value=<UNSET>, extracted='3' at ...>
            <RuntimeData myform.myarray.1.0.f2, value=<UNSET>, extracted='4' at ...>
          <RuntimeData myform.myarray.1.1, value=<UNSET>, extracted=odict([('f1', '5'), ('f2', '6')]) at ...>
            <RuntimeData myform.myarray.1.1.f1, value=<UNSET>, extracted='5' at ...>
            <RuntimeData myform.myarray.1.1.f2, value=<UNSET>, extracted='6' at ...>

Array hidden proxy for display mode children.

``yafowil.widget.array`` differs in value extraction when rerendering forms.
Normally the value gets fetched from the getter if not found on request.
Since it's hard to reference the origin value for array entries if not found
on request - you have possibly a mutable array containing componds with some 
fields disabled or in display mode - a hidden field is added for such widgets
in the tree on the fly in order to rerender forms correctly::

    >>> form['myarray'] = factory(
    ...     'array',
    ...     value=[{'f1': 'foo1', 'f2': 'foo2'}],
    ...     props={'label': 'My Compound Array with display children'})
    >>> form['myarray']['mycompound'] = factory('compound')
    >>> form['myarray']['mycompound']['f1'] = factory(
    ...     'field:label:text',
    ...     props={'label': 'F1'},
    ...     mode='display')
    >>> form['myarray']['mycompound']['f2'] = factory(
    ...     'field:label:text',
    ...     props={'label': 'F2', 'disabled': 'disabled'})
    
    >>> pxml(form())
    <form action="myaction" enctype="multipart/form-data" id="form-myform" method="post" novalidate="novalidate">
      <div class="array array-add array-remove array-sort" id="array-myform-myarray">
        <table>
          ...
              <td class="widget">
                <input id="input-myform-myarray-0-f1" name="myform.myarray.0.f1" type="hidden" value="foo1"/>
                <div class="field" id="field-myform-myarray-0-f1">
                  <label>F1</label>
                  <div class="display-text" id="display-myform-myarray-0-f1">foo1</div>
                </div>
                <input id="input-myform-myarray-0-f2" name="myform.myarray.0.f2" type="hidden" value="foo2"/>
                <div class="field" id="field-myform-myarray-0-f2">
                  <label for="input-myform-myarray-0-f2">F2</label>
                  <input class="text" disabled="disabled" id="input-myform-myarray-0-f2" name="myform.myarray.0.f2" type="text" value="foo2"/>
                </div>
              </td>
              ...
        </table>
        ...
    <BLANKLINE>

Callable array label::

    >>> form['myarray'] = factory(
    ...     'array',
    ...     props={'label': lambda: 'Callable label'})
    >>> form['myarray']['f1'] = factory(
    ...     'field:label:text',
    ...     props={'label': 'F1'},
    ...     mode='display')
    
    >>> pxml(form())
    <form action="myaction" enctype="multipart/form-data" id="form-myform" method="post" novalidate="novalidate">
      <div class="array array-add array-remove array-sort" id="array-myform-myarray">
        <table>
          <thead>
            <tr>
              <th>Callable label</th>
              ...
    <BLANKLINE>

Required::

    >>> form['myarray'] = factory(
    ...     'array',
    ...     props={'label': 'My Array'})
    >>> form['myarray']['myfield'] = factory(
    ...     'field:label:error:text',
    ...     props={
    ...         'label': 'My Field',
    ...         'required': 'My Field is required',
    ...     })
    >>> request = {
    ...     'myform.myarray.0': '0',
    ...     'myform.myarray.1': '',
    ... }
    >>> data = form.extract(request=request)
    >>> data.printtree()
    <RuntimeData myform, value=<UNSET>, extracted=odict([('myarray', ['0', ''])]) at ...>
      <RuntimeData myform.myarray, value=<UNSET>, extracted=['0', ''] at ...>
        <RuntimeData myform.myarray.0, value=<UNSET>, extracted='0' at ...>
        <RuntimeData myform.myarray.1, value=<UNSET>, extracted='', 1 error(s) at ...>

    >>> pxml(form(data))
    <form action="myaction" enctype="multipart/form-data" id="form-myform" method="post" novalidate="novalidate">
      <div class="array array-add array-remove array-sort" id="array-myform-myarray">
        <table>
          ...
          <tbody>
            <tr>
              ...
            </tr>
            <tr>
              <td class="widget">
                <div class="field" id="field-myform-myarray-1">
                  <label for="input-myform-myarray-1">My Field</label>
                  <div class="error">
                    <div class="errormessage">My Field is required</div>
                    <input class="required text" id="input-myform-myarray-1" name="myform.myarray.1" required="required" type="text" value=""/>
                  </div>
                </div>
              </td>
              <td class="actions">
                ...
              </td>
            </tr>
          </tbody>
        </table>
        <div class="arraytemplate">
          ...
        </div>
      </div>
    </form>
    <BLANKLINE>
    
    >>> del form['myarray']

3-Dimensional Array::

    >>> arr_1 = form['array_1'] = factory(
    ...     'array',
    ...     value=[
    ...         [
    ...             ['1'],
    ...         ],
    ...         [
    ...             ['2'],
    ...         ],
    ...     ],
    ...     props={
    ...         'label': 'Array 1',
    ...     })
    >>> arr_2 = arr_1['array_2'] = factory(
    ...     'array',
    ...     props={
    ...         'label': 'Array 2',
    ...     })
    >>> arr_3 = arr_2['array_3'] = factory(
    ...     'array',
    ...     props={
    ...         'label': 'Array 3',
    ...     })
    >>> arr_3['textfield'] = factory(
    ...     'field:error:label:text',
    ...     props={
    ...         'label': 'Text Field',
    ...         'required': 'Text Field is required',
    ...     })
    
    >>> form.printtree()
    <class 'yafowil.base.Widget'>: myform
      <class 'yafowil.base.Widget'>: array_1
        <class 'yafowil.base.Widget'>: table
          <class 'yafowil.base.Widget'>: head
            <class 'yafowil.base.Widget'>: row
              <class 'yafowil.base.Widget'>: label
              <class 'yafowil.base.Widget'>: actions
          <class 'yafowil.base.Widget'>: body
        <class 'yafowil.base.Widget'>: array_2
          <class 'yafowil.base.Widget'>: table
            <class 'yafowil.base.Widget'>: head
              <class 'yafowil.base.Widget'>: row
                <class 'yafowil.base.Widget'>: label
                <class 'yafowil.base.Widget'>: actions
            <class 'yafowil.base.Widget'>: body
          <class 'yafowil.base.Widget'>: array_3
            <class 'yafowil.base.Widget'>: table
              <class 'yafowil.base.Widget'>: head
                <class 'yafowil.base.Widget'>: row
                  <class 'yafowil.base.Widget'>: label
                  <class 'yafowil.base.Widget'>: actions
              <class 'yafowil.base.Widget'>: body
            <class 'yafowil.base.Widget'>: textfield

    >>> rendered = form()
    >>> pxml(rendered)
    <form action="myaction" enctype="multipart/form-data" id="form-myform" method="post" novalidate="novalidate">
      <div class="array array-add array-remove array-sort" id="array-myform-array_1">
        <table>
          <thead>
            <tr>
              <th>Array 1</th>
              ...
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="widget">
                <div class="array array-add array-remove array-sort" id="array-myform-array_1-0">
                  <table>
                    <thead>
                      <tr>
                        <th>Array 2</th>
                        ...
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td class="widget">
                          <div class="array array-add array-remove array-sort" id="array-myform-array_1-0-0">
                            <table>
                              <thead>
                                <tr>
                                  <th>Array 3</th>
                                  ...
                                </tr>
                              </thead>
                              <tbody>
                                <tr>
                                  <td class="widget">
                                    <div class="field" id="field-myform-array_1-0-0-0">
                                      <label for="input-myform-array_1-0-0-0">Text Field</label>
                                      <input class="required text" id="input-myform-array_1-0-0-0" name="myform.array_1.0.0.0" required="required" type="text" value="1"/>
                                    </div>
                                  </td>
                                  <td class="actions">
                                    ...
                                  </td>
                                </tr>
                              </tbody>
                            </table>
                            <div class="arraytemplate">
                              <div class="field" id="field-myform-array_1-0-0-TEMPLATE">
                                <label for="input-myform-array_1-0-0-TEMPLATE">Text Field</label>
                                <input class="required text" id="input-myform-array_1-0-0-TEMPLATE" name="myform.array_1.0.0.TEMPLATE" required="required" type="text" value=""/>
                              </div>
                            </div>
                          </div>
                        </td>
                        <td class="actions">
                          ...
                        </td>
                      </tr>
                    </tbody>
                  </table>
                  <div class="arraytemplate">
                    <div class="array array-add array-remove array-sort" id="array-myform-array_1-0-TEMPLATE">
                      <table>
                        <thead>
                          <tr>
                            <th>Array 3</th>
                            ...
                          </tr>
                        </thead>
                        <tbody/>
                      </table>
                      <div class="arraytemplate">
                        <div class="field" id="field-myform-array_1-0-TEMPLATE-TEMPLATE">
                          <label for="input-myform-array_1-0-TEMPLATE-TEMPLATE">Text Field</label>
                          <input class="required text" id="input-myform-array_1-0-TEMPLATE-TEMPLATE" name="myform.array_1.0.TEMPLATE.TEMPLATE" required="required" type="text" value=""/>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </td>
              <td class="actions">
                ...
              </td>
            </tr>
            <tr>
              ...
            </tr>
          </tbody>
        </table>
        <div class="arraytemplate">
          <div class="array array-add array-remove array-sort" id="array-myform-array_1-TEMPLATE">
            <table>
              <thead>
                <tr>
                  <th>Array 2</th>
                  ...
                </tr>
              </thead>
              <tbody/>
            </table>
            <div class="arraytemplate">
              <div class="array array-add array-remove array-sort" id="array-myform-array_1-TEMPLATE-TEMPLATE">
                <table>
                  <thead>
                    <tr>
                      <th>Array 3</th>
                      ...
                    </tr>
                  </thead>
                  <tbody/>
                </table>
                <div class="arraytemplate">
                  <div class="field" id="field-myform-array_1-TEMPLATE-TEMPLATE-TEMPLATE">
                    <label for="input-myform-array_1-TEMPLATE-TEMPLATE-TEMPLATE">Text Field</label>
                    <input class="required text" id="input-myform-array_1-TEMPLATE-TEMPLATE-TEMPLATE" name="myform.array_1.TEMPLATE.TEMPLATE.TEMPLATE" required="required" type="text" value=""/>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </form>
    <BLANKLINE>
