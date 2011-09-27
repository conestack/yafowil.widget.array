Import requirements::

    >>> import yafowil.loader
    >>> import yafowil.widget.array
    >>> from yafowil.base import factory

Create empty Array widget::
    
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
    >>> pxml(form())
    <form action="myaction" enctype="multipart/form-data" id="form-myform" method="post" novalidate="novalidate">
      <div class="array" id="array-myform-myarray">
        <table>
          <thead>
            <tr>
              <th>My Array</th>
              <th>
                <div class="array_actions">
                  <a class="array_row_add" href="#">&#160;</a>
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

Create empty Array widget with compound as template widget. If compound is
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
    >>> pxml(form())
    <form action="myaction" enctype="multipart/form-data" id="form-myform" method="post" novalidate="novalidate">
      <div class="array" id="array-myform-myarray">
        <table>
          <thead>
            <tr>
              <th>My Compound Array</th>
              <th>
                <div class="array_actions">
                  <a class="array_row_add" href="#">&#160;</a>
                </div>
              </th>
            </tr>
          </thead>
          <tbody/>
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

Create empty Array widget with another array as template widget::

    >>> form['myarrayarray'] = factory(
    ...     'array',
    ...     props={'label': 'My Array Array'})
    >>> form['myarrayarray']['myarray'] = factory(
    ...     'array',
    ...     props={'label': 'My Array'})
    >>> form['myarrayarray']['myarray']['myfield'] = factory(
    ...     'field:label:text',
    ...     props={'label': 'My Field'})
    >>> pxml(form())
    <form action="myaction" enctype="multipart/form-data" id="form-myform" method="post" novalidate="novalidate">
      <div class="array" id="array-myform-myarrayarray">
        <table>
          <thead>
            <tr>
              <th>My Array Array</th>
              <th>
                <div class="array_actions">
                  <a class="array_row_add" href="#">&#160;</a>
                </div>
              </th>
            </tr>
          </thead>
          <tbody/>
        </table>
        <div class="arraytemplate">
          <div class="array" id="array-myform-myarrayarray-TEMPLATE">
            <table>
              <thead>
                <tr>
                  <th>My Array</th>
                  <th>
                    <div class="array_actions">
                      <a class="array_row_add" href="#">&#160;</a>
                    </div>
                  </th>
                </tr>
              </thead>
              <tbody/>
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

Create Array widget with invalid preset value::

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

Create Array widget with preset values.

Value as list::
    
    >>> form['myarray'] = factory(
    ...     'array',
    ...     value=['1', '2', '3'],
    ...     props={'label': 'My Array'})
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
                <div class="array_actions">
                  <a class="array_row_add" href="#">&#160;</a>
                </div>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <div class="field" id="field-myform-myarray-0">
                <label for="input-myform-myarray-0">My Field</label>
                <input class="text" id="input-myform-myarray-0" name="myform.myarray.0" type="text" value="1"/>
              </div>
            </tr>
            <tr>
              <div class="field" id="field-myform-myarray-1">
                <label for="input-myform-myarray-1">My Field</label>
                <input class="text" id="input-myform-myarray-1" name="myform.myarray.1" type="text" value="2"/>
              </div>
            </tr>
            <tr>
              <div class="field" id="field-myform-myarray-2">
                <label for="input-myform-myarray-2">My Field</label>
                <input class="text" id="input-myform-myarray-2" name="myform.myarray.2" type="text" value="3"/>
              </div>
            </tr>
          </tbody>
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
    >>> value['1'] = '1'
    >>> value['2'] = '2'
    >>> value['3'] = '3'
    >>> form['myarray'] = factory(
    ...     'array',
    ...     value=value,
    ...     props={'label': 'My Array'})
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
                <div class="array_actions">
                  <a class="array_row_add" href="#">&#160;</a>
                </div>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <div class="field" id="field-myform-myarray-1">
                <label for="input-myform-myarray-1">My Field</label>
                <input class="text" id="input-myform-myarray-1" name="myform.myarray.1" type="text" value="1"/>
              </div>
            </tr>
            <tr>
              <div class="field" id="field-myform-myarray-2">
                <label for="input-myform-myarray-2">My Field</label>
                <input class="text" id="input-myform-myarray-2" name="myform.myarray.2" type="text" value="2"/>
              </div>
            </tr>
            <tr>
              <div class="field" id="field-myform-myarray-3">
                <label for="input-myform-myarray-3">My Field</label>
                <input class="text" id="input-myform-myarray-3" name="myform.myarray.3" type="text" value="3"/>
              </div>
            </tr>
          </tbody>
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
      <div class="array" id="array-myform-myarray">
        <table>
          <thead>
            <tr>
              <th>My Compound Array</th>
              <th>
                <div class="array_actions">
                  <a class="array_row_add" href="#">&#160;</a>
                </div>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <div class="field" id="field-myform-myarray-0-f1">
                <label for="input-myform-myarray-0-f1">F1</label>
                <input class="text" id="input-myform-myarray-0-f1" name="myform.myarray.0.f1" type="text" value="Value 1.1 F1"/>
              </div>
              <div class="field" id="field-myform-myarray-0-f2">
                <label for="input-myform-myarray-0-f2">F2</label>
                <input class="text" id="input-myform-myarray-0-f2" name="myform.myarray.0.f2" type="text" value="Value 1.2 F2"/>
              </div>
            </tr>
            <tr>
              <div class="field" id="field-myform-myarray-1-f1">
                <label for="input-myform-myarray-1-f1">F1</label>
                <input class="text" id="input-myform-myarray-1-f1" name="myform.myarray.1.f1" type="text" value="Value 2.1 F1"/>
              </div>
              <div class="field" id="field-myform-myarray-1-f2">
                <label for="input-myform-myarray-1-f2">F2</label>
                <input class="text" id="input-myform-myarray-1-f2" name="myform.myarray.1.f2" type="text" value="Value 2.2 F2"/>
              </div>
            </tr>
          </tbody>
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
      <div class="array" id="array-myform-myarray">
        <table>
          <thead>
            <tr>
              <th>My Array Array</th>
              <th>
                <div class="array_actions">
                  <a class="array_row_add" href="#">&#160;</a>
                </div>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <div class="array" id="array-myform-myarray-0">
                <table>
                  <thead>
                    <tr>
                      <th>Subrray</th>
                      <th>
                        <div class="array_actions">
                          <a class="array_row_add" href="#">&#160;</a>
                        </div>
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <div class="field" id="field-myform-myarray-0-0">
                        <label for="input-myform-myarray-0-0">My Field</label>
                        <input class="text" id="input-myform-myarray-0-0" name="myform.myarray.0.0" type="text" value="1"/>
                      </div>
                    </tr>
                    <tr>
                      <div class="field" id="field-myform-myarray-0-1">
                        <label for="input-myform-myarray-0-1">My Field</label>
                        <input class="text" id="input-myform-myarray-0-1" name="myform.myarray.0.1" type="text" value="2"/>
                      </div>
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
            </tr>
            <tr>
              <div class="array" id="array-myform-myarray-1">
                <table>
                  <thead>
                    <tr>
                      <th>Subrray</th>
                      <th>
                        <div class="array_actions">
                          <a class="array_row_add" href="#">&#160;</a>
                        </div>
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <div class="field" id="field-myform-myarray-1-0">
                        <label for="input-myform-myarray-1-0">My Field</label>
                        <input class="text" id="input-myform-myarray-1-0" name="myform.myarray.1.0" type="text" value="4"/>
                      </div>
                    </tr>
                    <tr>
                      <div class="field" id="field-myform-myarray-1-1">
                        <label for="input-myform-myarray-1-1">My Field</label>
                        <input class="text" id="input-myform-myarray-1-1" name="myform.myarray.1.1" type="text" value="5"/>
                      </div>
                    </tr>
                  </tbody>
                </table>
                <div class="arraytemplate">
                  <div class="field" id="field-myform-myarray-1-TEMPLATE">
                    <label for="input-myform-myarray-1-TEMPLATE">My Field</label>
                    <input class="text" id="input-myform-myarray-1-TEMPLATE" name="myform.myarray.1.TEMPLATE" type="text" value=""/>
                  </div>
                </div>
              </div>
            </tr>
          </tbody>
        </table>
        <div class="arraytemplate">
          <div class="array" id="array-myform-myarray-TEMPLATE">
            <table>
              <thead>
                <tr>
                  <th>Subrray</th>
                  <th>
                    <div class="array_actions">
                      <a class="array_row_add" href="#">&#160;</a>
                    </div>
                  </th>
                </tr>
              </thead>
              <tbody/>
            </table>
            <div class="arraytemplate">
              <div class="field" id="field-myform-myarray-TEMPLATE-TEMPLATE">
                <label for="input-myform-myarray-TEMPLATE-TEMPLATE">My Field</label>
                <input class="text" id="input-myform-myarray-TEMPLATE-TEMPLATE" name="myform.myarray.TEMPLATE.TEMPLATE" type="text" value=""/>
              </div>
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
    >>> form['myarray']['subarray']['mycompound'] = factory('compound')
    >>> form['myarray']['subarray']['mycompound']['f1'] = factory(
    ...     'field:label:text',
    ...     props={'label': 'F1'})
    >>> form['myarray']['subarray']['mycompound']['f2'] = factory(
    ...     'field:label:text',
    ...     props={'label': 'F2'})
    >>> rendered = form()
    >>> pxml(rendered)
    <form action="myaction" enctype="multipart/form-data" id="form-myform" method="post" novalidate="novalidate">
      <div class="array" id="array-myform-myarray">
        <table>
          <thead>
            <tr>
              <th>My Compound Array</th>
              <th>
                <div class="array_actions">
                  <a class="array_row_add" href="#">&#160;</a>
                </div>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <div class="array" id="array-myform-myarray-0">
                <table>
                  <thead>
                    <tr>
                      <th>Subarray</th>
                      <th>
                        <div class="array_actions">
                          <a class="array_row_add" href="#">&#160;</a>
                        </div>
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <div class="field" id="field-myform-myarray-0-0-f1">
                        <label for="input-myform-myarray-0-0-f1">F1</label>
                        <input class="text" id="input-myform-myarray-0-0-f1" name="myform.myarray.0.0.f1" type="text" value="Value 0.0 F1"/>
                      </div>
                      <div class="field" id="field-myform-myarray-0-0-f2">
                        <label for="input-myform-myarray-0-0-f2">F2</label>
                        <input class="text" id="input-myform-myarray-0-0-f2" name="myform.myarray.0.0.f2" type="text" value="Value 0.0 F2"/>
                      </div>
                    </tr>
                    <tr>
                      <div class="field" id="field-myform-myarray-0-1-f1">
                        <label for="input-myform-myarray-0-1-f1">F1</label>
                        <input class="text" id="input-myform-myarray-0-1-f1" name="myform.myarray.0.1.f1" type="text" value="Value 0.1 F1"/>
                      </div>
                      <div class="field" id="field-myform-myarray-0-1-f2">
                        <label for="input-myform-myarray-0-1-f2">F2</label>
                        <input class="text" id="input-myform-myarray-0-1-f2" name="myform.myarray.0.1.f2" type="text" value="Value 0.1 F2"/>
                      </div>
                    </tr>
                  </tbody>
                </table>
                <div class="arraytemplate">
                  <div class="field" id="field-myform-myarray-0-TEMPLATE-f1">
                    <label for="input-myform-myarray-0-TEMPLATE-f1">F1</label>
                    <input class="text" id="input-myform-myarray-0-TEMPLATE-f1" name="myform.myarray.0.TEMPLATE.f1" type="text" value=""/>
                  </div>
                  <div class="field" id="field-myform-myarray-0-TEMPLATE-f2">
                    <label for="input-myform-myarray-0-TEMPLATE-f2">F2</label>
                    <input class="text" id="input-myform-myarray-0-TEMPLATE-f2" name="myform.myarray.0.TEMPLATE.f2" type="text" value=""/>
                  </div>
                </div>
                <div class="field" id="field-myform-myarray-0-f1">
                  <label for="input-myform-myarray-0-f1">F1</label>
                  <input class="text" id="input-myform-myarray-0-f1" name="myform.myarray.0.f1" type="text" value=""/>
                </div>
                <div class="field" id="field-myform-myarray-0-f2">
                  <label for="input-myform-myarray-0-f2">F2</label>
                  <input class="text" id="input-myform-myarray-0-f2" name="myform.myarray.0.f2" type="text" value=""/>
                </div>
              </div>
            </tr>
          </tbody>
        </table>
        <div class="arraytemplate">
          <div class="array" id="array-myform-myarray-TEMPLATE">
            <table>
              <thead>
                <tr>
                  <th>Subarray</th>
                  <th>
                    <div class="array_actions">
                      <a class="array_row_add" href="#">&#160;</a>
                    </div>
                  </th>
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

Base Extraction::

    >>> 

Entries increased in UI::

    >>> 

Entries decreased in UI::

    >>> 

Check required::

    >>>
 