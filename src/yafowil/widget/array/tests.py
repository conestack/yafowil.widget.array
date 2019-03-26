from node.utils import UNSET
from odict import odict
from yafowil.base import ExtractionError
from yafowil.base import factory
from yafowil.compat import IS_PY2
from yafowil.tests import fxml
from yafowil.tests import YafowilTestCase
import unittest
import yafowil.loader


if not IS_PY2:
    from importlib import reload


class TestArrayWidget(YafowilTestCase):

    def setUp(self):
        super(TestArrayWidget, self).setUp()
        from yafowil.widget.array import widget
        reload(widget)

    def test_array_with_missing_entry_definition(self):
        form = factory(
            'form',
            name='myform',
            props={'action': 'myaction'})
        form['myarray'] = factory(
            'array',
            props={'label': 'My Array'})
        err = self.expect_error(
            Exception,
            form
        )
        msg = 'Empty array widget defined'
        self.assertEqual(str(err), msg)

    def test_empty_array(self):
        # Create empty array widget
        form = factory(
            'form',
            name='myform',
            props={'action': 'myaction'})
        form['myarray'] = factory(
            'array',
            props={'label': 'My Array'})
        form['myarray']['myfield'] = factory(
            'field:label:text',
            props={'label': 'My Field'})

        self.assertEqual(form.treerepr().split('\n'), [
            "<class 'yafowil.base.Widget'>: myform",
            "  <class 'yafowil.base.Widget'>: myarray",
            "    <class 'yafowil.base.Widget'>: table",
            "      <class 'yafowil.base.Widget'>: head",
            "        <class 'yafowil.base.Widget'>: row",
            "          <class 'yafowil.base.Widget'>: label",
            "          <class 'yafowil.base.Widget'>: actions",
            "      <class 'yafowil.base.Widget'>: body",
            "    <class 'yafowil.base.Widget'>: myfield",
            ""
        ])

        self.check_output("""
        <form action="myaction" enctype="multipart/form-data"
              id="form-myform" method="post" novalidate="novalidate">
          <div class="array array-add array-remove array-sort"
               id="array-myform-myarray">
            <table>
              <thead>
                <tr>
                  <th>My Array</th>
                  <th class="head_actions">
                    <div class="array_actions">
                      <a class="array_row_add" href="#">
                        <span class="icon-plus-sign"> </span>
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
                <input class="text" id="input-myform-myarray-TEMPLATE"
                       name="myform.myarray.TEMPLATE" type="text" value=""/>
              </div>
            </div>
          </div>
        </form>
        """, fxml(form()))

    def test_empty_array_with_add_action_disabled(self):
        form = factory(
            'form',
            name='myform',
            props={'action': 'myaction'})
        form['myarray'] = factory(
            'array',
            props={
                'label': 'My Array',
                'add': False,
            })
        form['myarray']['myfield'] = factory(
            'field:label:text',
            props={'label': 'My Field'})

        self.assertEqual(form.treerepr().split('\n'), [
            "<class 'yafowil.base.Widget'>: myform",
            "  <class 'yafowil.base.Widget'>: myarray",
            "    <class 'yafowil.base.Widget'>: table",
            "      <class 'yafowil.base.Widget'>: head",
            "        <class 'yafowil.base.Widget'>: row",
            "          <class 'yafowil.base.Widget'>: label",
            "          <class 'yafowil.base.Widget'>: actions",
            "      <class 'yafowil.base.Widget'>: body",
            "    <class 'yafowil.base.Widget'>: myfield",
            ""
        ])

        self.check_output("""
        <form action="myaction" enctype="multipart/form-data" id="form-myform"
              method="post" novalidate="novalidate">
          <div class="array array-remove array-sort" id="array-myform-myarray">
            <table>
              <thead>
                <tr>
                  <th>My Array</th>
                  <th class="head_actions">
                    <div class="array_actions"/>
                  </th>
                </tr>
              </thead>
              <tbody/>
            </table>
          </div>
        </form>
        """, fxml(form()))

    def test_array_with_overwritten_class(self):
        # Create array widget with overwritten class property. If CSS class
        # 'array' missing, it gets added transparently
        form = factory(
            'form',
            name='myform',
            props={'action': 'myaction'})
        form['myarray'] = factory(
            'array',
            props={
                'label': 'My Array',
                'class': 'specialclass',
            })
        form['myarray']['myfield'] = factory(
            'field:label:text',
            props={'label': 'My Field'})
        self.check_output("""
        <form action="myaction" enctype="multipart/form-data" id="form-myform"
              method="post" novalidate="novalidate">
          <div class="array specialclass array-add array-remove array-sort"
               id="array-myform-myarray">
            <table>
              ...
            </table>
            <div class="arraytemplate">
              ...
            </div>
          </div>
        </form>
        """, fxml(form()))

    def test_display_mode(self):
        # Display mode is not implemented yet
        form = factory(
            'form',
            name='myform',
            props={'action': 'myaction'})
        form['myarray'] = factory(
            'array',
            value=['1', '2'],
            props={
                'label': 'My Array',
                'class': 'specialclass',
            },
            mode='display')
        form['myarray']['myfield'] = factory(
            'field:label:text',
            props={'label': 'My Field'})
        self.check_output("""
        <form action="myaction" enctype="multipart/form-data" id="form-myform"
              method="post" novalidate="novalidate">
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
                    <label>My Field</label>
                    <div class="display-text" id="display-myform-myarray-0">1</div>
                  </div>
                </td>
              </tr>
              <tr>
                <td class="widget">
                  <div class="field" id="field-myform-myarray-1">
                    <label>My Field</label>
                    <div class="display-text" id="display-myform-myarray-1">2</div>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </form>
        """, fxml(form()))

    def test_empty_static_array(self):
        form = factory(
            'form',
            name='myform',
            props={'action': 'myaction'})
        form['myarray'] = factory(
            'array',
            props={
                'label': 'My Array',
                'static': True,
            })
        form['myarray']['myfield'] = factory(
            'field:label:text',
            props={'label': 'My Field'})

        self.assertEqual(form.treerepr().split('\n'), [
            "<class 'yafowil.base.Widget'>: myform",
            "  <class 'yafowil.base.Widget'>: myarray",
            "    <class 'yafowil.base.Widget'>: table",
            "      <class 'yafowil.base.Widget'>: head",
            "        <class 'yafowil.base.Widget'>: row",
            "          <class 'yafowil.base.Widget'>: label",
            "      <class 'yafowil.base.Widget'>: body",
            "    <class 'yafowil.base.Widget'>: myfield",
            ""
        ])

        self.check_output("""
        <form action="myaction" enctype="multipart/form-data" id="form-myform"
              method="post" novalidate="novalidate">
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
        """, fxml(form()))

    def test_empty_array_with_compound_as_template(self):
        # Create empty array widget with compound as template widget. If
        # compound is used as array template, this must not be structural
        form = factory(
            'form',
            name='myform',
            props={'action': 'myaction'})
        form['myarray'] = factory(
            'array',
            props={'label': 'My Compound Array'})
        form['myarray']['mycompound'] = factory(
            'compound',
            props={'structural': True})

        err = self.expect_error(
            Exception,
            form
        )
        msg = 'Compound templates for arrays must not be structural.'
        self.assertEqual(str(err), msg)

        # Now with valid compound template
        form['myarray'] = factory(
            'array',
            props={'label': 'My Compound Array'})
        form['myarray']['mycompound'] = factory('compound')
        form['myarray']['mycompound']['f1'] = factory(
            'field:label:text',
            props={'label': 'F1'})
        form['myarray']['mycompound']['f2'] = factory(
            'field:label:text',
            props={'label': 'F2'})

        self.assertEqual(form.treerepr().split('\n'), [
            "<class 'yafowil.base.Widget'>: myform",
            "  <class 'yafowil.base.Widget'>: myarray",
            "    <class 'yafowil.base.Widget'>: table",
            "      <class 'yafowil.base.Widget'>: head",
            "        <class 'yafowil.base.Widget'>: row",
            "          <class 'yafowil.base.Widget'>: label",
            "          <class 'yafowil.base.Widget'>: actions",
            "      <class 'yafowil.base.Widget'>: body",
            "    <class 'yafowil.base.Widget'>: mycompound",
            "      <class 'yafowil.base.Widget'>: f1",
            "      <class 'yafowil.base.Widget'>: f2",
            ""
        ])

        self.check_output("""
        <form action="myaction" enctype="multipart/form-data" id="form-myform"
              method="post" novalidate="novalidate">
          <div class="array array-add array-remove array-sort"
               id="array-myform-myarray">
            <table>
              ...
            </table>
            <div class="arraytemplate">
              <div class="field" id="field-myform-myarray-TEMPLATE-f1">
                <label for="input-myform-myarray-TEMPLATE-f1">F1</label>
                <input class="text" id="input-myform-myarray-TEMPLATE-f1"
                       name="myform.myarray.TEMPLATE.f1" type="text" value=""/>
              </div>
              <div class="field" id="field-myform-myarray-TEMPLATE-f2">
                <label for="input-myform-myarray-TEMPLATE-f2">F2</label>
                <input class="text" id="input-myform-myarray-TEMPLATE-f2"
                       name="myform.myarray.TEMPLATE.f2" type="text" value=""/>
              </div>
            </div>
          </div>
        </form>
        """, fxml(form()))

    def test_empty_array_with_array_as_template(self):
        form = factory(
            'form',
            name='myform',
            props={'action': 'myaction'})
        form['myarrayarray'] = factory(
            'array',
            props={'label': 'My Array Array'})
        form['myarrayarray']['myarray'] = factory(
            'array',
            props={'label': 'My Array'})
        form['myarrayarray']['myarray']['myfield'] = factory(
            'field:label:text',
            props={'label': 'My Field'})

        self.assertEqual(form.treerepr().split('\n'), [
            "<class 'yafowil.base.Widget'>: myform",
            "  <class 'yafowil.base.Widget'>: myarrayarray",
            "    <class 'yafowil.base.Widget'>: table",
            "      <class 'yafowil.base.Widget'>: head",
            "        <class 'yafowil.base.Widget'>: row",
            "          <class 'yafowil.base.Widget'>: label",
            "          <class 'yafowil.base.Widget'>: actions",
            "      <class 'yafowil.base.Widget'>: body",
            "    <class 'yafowil.base.Widget'>: myarray",
            "      <class 'yafowil.base.Widget'>: table",
            "        <class 'yafowil.base.Widget'>: head",
            "          <class 'yafowil.base.Widget'>: row",
            "            <class 'yafowil.base.Widget'>: label",
            "            <class 'yafowil.base.Widget'>: actions",
            "        <class 'yafowil.base.Widget'>: body",
            "      <class 'yafowil.base.Widget'>: myfield",
            ""
        ])

        self.check_output("""
        <form action="myaction" enctype="multipart/form-data" id="form-myform"
              method="post" novalidate="novalidate">
          <div class="array array-add array-remove array-sort"
               id="array-myform-myarrayarray">
            <table>
            ...
            </table>
            <div class="arraytemplate">
              <div class="array array-add array-remove array-sort"
                   id="array-myform-myarrayarray-TEMPLATE">
                <table>
                ...
                </table>
                <div class="arraytemplate">
                  <div class="field"
                       id="field-myform-myarrayarray-TEMPLATE-TEMPLATE">
                    <label for="input-myform-myarrayarray-TEMPLATE-TEMPLATE">My Field</label>
                    <input class="text" id="input-myform-myarrayarray-TEMPLATE-TEMPLATE"
                           name="myform.myarrayarray.TEMPLATE.TEMPLATE"
                           type="text" value=""/>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </form>
        """, fxml(form()))

    def test_array_with_invalid_preset_value(self):
        form = factory(
            'form',
            name='myform',
            props={'action': 'myaction'})
        form['myarray'] = factory(
            'array',
            value=object(),
            props={'label': 'My Array'})
        form['myarray']['myfield'] = factory(
            'field:label:text',
            props={'label': 'My Field'})

        err = self.expect_error(
            ValueError,
            form
        )
        if IS_PY2:
            msg = "Expected list or dict as value. Got '<type 'object'>'"
        else:
            msg = "Expected list or dict as value. Got '<class 'object'>'"
        self.assertEqual(str(err), msg)

    def test_array_with_preset_values_disable_add_action(self):
        # Value as list. Disable ``add``
        form = factory(
            'form',
            name='myform',
            props={'action': 'myaction'})
        form['myarray'] = factory(
            'array',
            value=['1', '2'],
            props={
                'label': 'My Array',
                'add': False,
            })
        form['myarray']['myfield'] = factory(
            'field:label:text',
            props={'label': 'My Field'})

        self.check_output("""
        <form action="myaction" enctype="multipart/form-data" id="form-myform"
              method="post" novalidate="novalidate">
          <div class="array array-remove array-sort" id="array-myform-myarray">
            <table>
              <thead>
                <tr>
                  <th>My Array</th>
                  <th class="head_actions">
                    <div class="array_actions"/>
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td class="widget">
                    <div class="field" id="field-myform-myarray-0">
                      <label for="input-myform-myarray-0">My Field</label>
                      <input class="text" id="input-myform-myarray-0"
                             name="myform.myarray.0" type="text" value="1"/>
                    </div>
                  </td>
                  <td class="actions">
                    <div class="array_actions">
                      <a class="array_row_remove" href="#">
                        <span class="icon-minus-sign"> </span>
                      </a>
                      <a class="array_row_up" href="#">
                        <span class="icon-circle-arrow-up"> </span>
                      </a>
                      <a class="array_row_down" href="#">
                        <span class="icon-circle-arrow-down"> </span>
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
        """, fxml(form()))

    def test_array_with_preset_values_disable_sort_actions(self):
        # Value as list. Disable ``sort``
        form = factory(
            'form',
            name='myform',
            props={'action': 'myaction'})
        form['myarray'] = factory(
            'array',
            value=['1', '2'],
            props={
                'label': 'My Array',
                'sort': False,
            })
        form['myarray']['myfield'] = factory(
            'field:label:text',
            props={'label': 'My Field'})

        self.check_output("""
        <form action="myaction" enctype="multipart/form-data" id="form-myform"
              method="post" novalidate="novalidate">
          <div class="array array-add array-remove" id="array-myform-myarray">
            <table>
              <thead>
                <tr>
                  <th>My Array</th>
                  <th class="head_actions">
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
                      <input class="text" id="input-myform-myarray-0"
                             name="myform.myarray.0" type="text" value="1"/>
                    </div>
                  </td>
                  <td class="actions">
                    <div class="array_actions">
                      <a class="array_row_add" href="#">
                        <span class="icon-plus-sign"> </span>
                      </a>
                      <a class="array_row_remove" href="#">
                        <span class="icon-minus-sign"> </span>
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
        """, fxml(form()))

    def test_array_with_preset_values_disable_all_actions(self):
        # Value as list. All actions disabled. Actions col still rendered
        form = factory(
            'form',
            name='myform',
            props={'action': 'myaction'})
        form['myarray'] = factory(
            'array',
            value=['1', '2'],
            props={
                'label': 'My Array',
                'add': False,
                'remove': False,
                'sort': False,
            })
        form['myarray']['myfield'] = factory(
            'field:label:text',
            props={'label': 'My Field'})

        self.check_output("""
        <form action="myaction" enctype="multipart/form-data" id="form-myform"
              method="post" novalidate="novalidate">
          <div class="array" id="array-myform-myarray">
            <table>
              <thead>
                <tr>
                  <th>My Array</th>
                  <th class="head_actions">
                    <div class="array_actions"/>
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td class="widget">
                    <div class="field" id="field-myform-myarray-0">
                      <label for="input-myform-myarray-0">My Field</label>
                      <input class="text" id="input-myform-myarray-0"
                             name="myform.myarray.0" type="text" value="1"/>
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
        """, fxml(form()))

    def test_static_array_with_preset_values(self):
        # Value as list. Set ``static`` property to ``True``. Actions col is
        # skipped
        form = factory(
            'form',
            name='myform',
            props={'action': 'myaction'})
        form['myarray'] = factory(
            'array',
            value=['1', '2'],
            props={
                'label': 'My Array',
                'static': True,
            })
        form['myarray']['myfield'] = factory(
            'field:label:text',
            props={'label': 'My Field'})

        self.assertEqual(form.treerepr().split('\n'), [
            "<class 'yafowil.base.Widget'>: myform",
            "  <class 'yafowil.base.Widget'>: myarray",
            "    <class 'yafowil.base.Widget'>: table",
            "      <class 'yafowil.base.Widget'>: head",
            "        <class 'yafowil.base.Widget'>: row",
            "          <class 'yafowil.base.Widget'>: label",
            "      <class 'yafowil.base.Widget'>: body",
            "    <class 'yafowil.base.Widget'>: myfield",
            ""
        ])

        self.check_output("""
        <form action="myaction" enctype="multipart/form-data" id="form-myform"
              method="post" novalidate="novalidate">
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
                      <input class="text" id="input-myform-myarray-0"
                             name="myform.myarray.0" type="text" value="1"/>
                    </div>
                  </td>
                </tr>
                <tr>
                  <td class="widget">
                    <div class="field" id="field-myform-myarray-1">
                      <label for="input-myform-myarray-1">My Field</label>
                      <input class="text" id="input-myform-myarray-1"
                             name="myform.myarray.1" type="text" value="2"/>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </form>
        """, fxml(form()))

    def test_array_with_preset_value_as_list(self):
        form = factory(
            'form',
            name='myform',
            props={'action': 'myaction'})
        form['myarray'] = factory(
            'array',
            value=['1', '2'],
            props={'label': 'My Array'})
        form['myarray']['myfield'] = factory(
            'field:label:text',
            props={'label': 'My Field'})

        self.check_output("""
        <form action="myaction" enctype="multipart/form-data" id="form-myform"
              method="post" novalidate="novalidate">
          <div class="array array-add array-remove array-sort"
               id="array-myform-myarray">
            <table>
              <thead>
                ...
              </thead>
              <tbody>
                <tr>
                  <td class="widget">
                    <div class="field" id="field-myform-myarray-0">
                      <label for="input-myform-myarray-0">My Field</label>
                      <input class="text" id="input-myform-myarray-0"
                             name="myform.myarray.0" type="text" value="1"/>
                    </div>
                  </td>
                  <td class="actions">
                    <div class="array_actions">
                      <a class="array_row_add" href="#">
                        <span class="icon-plus-sign"> </span>
                      </a>
                      <a class="array_row_remove" href="#">
                        <span class="icon-minus-sign"> </span>
                      </a>
                      <a class="array_row_up" href="#">
                        <span class="icon-circle-arrow-up"> </span>
                      </a>
                      <a class="array_row_down" href="#">
                        <span class="icon-circle-arrow-down"> </span>
                      </a>
                    </div>
                  </td>
                </tr>
                <tr>
                  <td class="widget">
                    <div class="field" id="field-myform-myarray-1">
                      <label for="input-myform-myarray-1">My Field</label>
                      <input class="text" id="input-myform-myarray-1"
                             name="myform.myarray.1" type="text" value="2"/>
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
        """, fxml(form()))

    def test_array_with_preset_value_as_dict_invalid(self):
        # Value as dict, must contain indices as keys
        form = factory(
            'form',
            name='myform',
            props={'action': 'myaction'})
        value = odict()
        value['a'] = '1'
        form['myarray'] = factory(
            'array',
            value=value,
            props={'label': 'My Array'})
        form['myarray']['myfield'] = factory(
            'field:label:text',
            props={'label': 'My Field'})

        err = self.expect_error(
            Exception,
            form
        )
        msg = "Array value error. invalid literal for int() with base 10: 'a'"
        self.assertEqual(str(err), msg)

    def test_array_with_preset_value_as_dict(self):
        # Valid dict value
        form = factory(
            'form',
            name='myform',
            props={'action': 'myaction'})
        value = odict()
        value['0'] = '1'
        value['1'] = '2'
        form['myarray'] = factory(
            'array',
            value=value,
            props={'label': 'My Array'})
        form['myarray']['myfield'] = factory(
            'field:label:text',
            props={'label': 'My Field'})

        self.check_output("""
        <form action="myaction" enctype="multipart/form-data" id="form-myform"
              method="post" novalidate="novalidate">
          <div class="array array-add array-remove array-sort"
               id="array-myform-myarray">
            <table>
              <thead>
                ...
              </thead>
              <tbody>
                <tr>
                  <td class="widget">
                    <div class="field" id="field-myform-myarray-0">
                      <label for="input-myform-myarray-0">My Field</label>
                      <input class="text" id="input-myform-myarray-0"
                             name="myform.myarray.0" type="text" value="1"/>
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
        """, fxml(form()))

    def test_array_with_compounds_default_values(self):
        form = factory(
            'form',
            name='myform',
            props={'action': 'myaction'})
        form['myarray'] = factory(
            'array',
            value=[
                {
                    'f1': 'Value 1.1 F1',
                    'f2': 'Value 1.2 F2',
                },
                {
                    'f1': 'Value 2.1 F1',
                    'f2': 'Value 2.2 F2',
                }
            ],
            props={'label': 'My Compound Array'})
        form['myarray']['mycompound'] = factory('compound')
        form['myarray']['mycompound']['f1'] = factory(
            'field:label:text',
            props={'label': 'F1'})
        form['myarray']['mycompound']['f2'] = factory(
            'field:label:text',
            props={'label': 'F2'})

        self.check_output("""
        <form action="myaction" enctype="multipart/form-data" id="form-myform"
              method="post" novalidate="novalidate">
          <div class="array array-add array-remove array-sort"
               id="array-myform-myarray">
            <table>
              <thead>
                ...
              </thead>
              <tbody>
                <tr>
                  <td class="widget">
                    <div class="field" id="field-myform-myarray-0-f1">
                      <label for="input-myform-myarray-0-f1">F1</label>
                      <input class="text" id="input-myform-myarray-0-f1"
                             name="myform.myarray.0.f1" type="text"
                             value="Value 1.1 F1"/>
                    </div>
                    <div class="field" id="field-myform-myarray-0-f2">
                      <label for="input-myform-myarray-0-f2">F2</label>
                      <input class="text" id="input-myform-myarray-0-f2"
                             name="myform.myarray.0.f2" type="text"
                             value="Value 1.2 F2"/>
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
                      <input class="text" id="input-myform-myarray-1-f1"
                             name="myform.myarray.1.f1" type="text"
                             value="Value 2.1 F1"/>
                    </div>
                    <div class="field" id="field-myform-myarray-1-f2">
                      <label for="input-myform-myarray-1-f2">F2</label>
                      <input class="text" id="input-myform-myarray-1-f2"
                             name="myform.myarray.1.f2" type="text"
                             value="Value 2.2 F2"/>
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
        """, fxml(form()))

    def test_array_with_array_default_values_set(self):
        # default values as list
        form = factory(
            'form',
            name='myform',
            props={'action': 'myaction'})
        form['myarray'] = factory(
            'array',
            value=[
                ['1', '2'],
                ['4', '5'],
            ],
            props={'label': 'My Array Array'})
        form['myarray']['subarray'] = factory(
            'array',
            props={'label': 'Subrray'})
        form['myarray']['subarray']['myfield'] = factory(
            'field:label:text',
            props={'label': 'My Field'})
        rendered = form()
        self.check_output("""
        <form action="myaction" enctype="multipart/form-data" id="form-myform"
              method="post" novalidate="novalidate">
          <div class="array array-add array-remove array-sort"
               id="array-myform-myarray">
            <table>
              <thead>
                ...
              </thead>
              <tbody>
                <tr>
                  <td class="widget">
                    <div class="array array-add array-remove array-sort"
                         id="array-myform-myarray-0">
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
                                <input class="text" id="input-myform-myarray-0-0"
                                       name="myform.myarray.0.0" type="text"
                                       value="1"/>
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
                                <input class="text" id="input-myform-myarray-0-1"
                                       name="myform.myarray.0.1" type="text"
                                       value="2"/>
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
                          <input class="text"
                                 id="input-myform-myarray-0-TEMPLATE"
                                 name="myform.myarray.0.TEMPLATE" type="text"
                                 value=""/>
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
                    <div class="array array-add array-remove array-sort"
                         id="array-myform-myarray-1">
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
              <div class="array array-add array-remove array-sort"
                   id="array-myform-myarray-TEMPLATE">
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
        """, fxml(rendered))

        # default values as dict
        form['myarray'] = factory(
        'array',
        value={
            '0': {'0': '1', '1': '2'},
            '1': {'0': '4', '1': '5'},
        },
        props={'label': 'My Array Array'})
        form['myarray']['subarray'] = factory(
            'array',
            props={'label': 'Subrray'})
        form['myarray']['subarray']['myfield'] = factory(
            'field:label:text',
            props={'label': 'My Field'})
        self.assertEqual(form(), rendered)

        # default values mixed
        form['myarray'] = factory(
            'array',
            value={
                '0': ['1', '2'],
                '1': ['4', '5'],
            },
            props={'label': 'My Array Array'})
        form['myarray']['subarray'] = factory(
            'array',
            props={'label': 'Subrray'})
        form['myarray']['subarray']['myfield'] = factory(
            'field:label:text',
            props={'label': 'My Field'})
        self.assertEqual(form(), rendered)

        form['myarray'] = factory(
            'array',
            value=[
                {'0': '1', '1': '2'},
                {'0': '4', '1': '5'},
            ],
            props={'label': 'My Array Array'})
        form['myarray']['subarray'] = factory(
            'array',
            props={'label': 'Subrray'})
        form['myarray']['subarray']['myfield'] = factory(
            'field:label:text',
            props={'label': 'My Field'})
        self.assertEqual(form(), rendered)

    def test_array_with_array_with_compound_default_values_set(self):
        # default values as list
        form = factory(
            'form',
            name='myform',
            props={'action': 'myaction'})
        form['myarray'] = factory(
            'array',
            value=[
                [
                    {
                        'f1': 'Value 0.0 F1',
                        'f2': 'Value 0.0 F2',
                    },
                    {
                        'f1': 'Value 0.1 F1',
                        'f2': 'Value 0.1 F2',
                    },
                ],
            ],
            props={'label': 'My Compound Array'})
        form['myarray']['subarray'] = factory(
            'array',
            props={'label': 'Subarray'})
        form['myarray']['subarray']['compoundinsub'] = factory('compound')
        form['myarray']['subarray']['compoundinsub']['f1'] = factory(
            'field:label:text',
            props={'label': 'F1'})
        form['myarray']['subarray']['compoundinsub']['f2'] = factory(
            'field:label:text',
            props={'label': 'F2'})

        self.assertEqual(form.treerepr().split('\n'), [
            "<class 'yafowil.base.Widget'>: myform",
            "  <class 'yafowil.base.Widget'>: myarray",
            "    <class 'yafowil.base.Widget'>: table",
            "      <class 'yafowil.base.Widget'>: head",
            "        <class 'yafowil.base.Widget'>: row",
            "          <class 'yafowil.base.Widget'>: label",
            "          <class 'yafowil.base.Widget'>: actions",
            "      <class 'yafowil.base.Widget'>: body",
            "    <class 'yafowil.base.Widget'>: subarray",
            "      <class 'yafowil.base.Widget'>: table",
            "        <class 'yafowil.base.Widget'>: head",
            "          <class 'yafowil.base.Widget'>: row",
            "            <class 'yafowil.base.Widget'>: label",
            "            <class 'yafowil.base.Widget'>: actions",
            "        <class 'yafowil.base.Widget'>: body",
            "      <class 'yafowil.base.Widget'>: compoundinsub",
            "        <class 'yafowil.base.Widget'>: f1",
            "        <class 'yafowil.base.Widget'>: f2",
            ""
        ])

        rendered = form()
        self.check_output("""
        <form action="myaction" enctype="multipart/form-data" id="form-myform"
              method="post" novalidate="novalidate">
          <div class="array array-add array-remove array-sort"
               id="array-myform-myarray">
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
                    <div class="array array-add array-remove array-sort"
                         id="array-myform-myarray-0">
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
                                <input class="text" id="input-myform-myarray-0-0-f1"
                                       name="myform.myarray.0.0.f1" type="text"
                                       value="Value 0.0 F1"/>
                              </div>
                              <div class="field" id="field-myform-myarray-0-0-f2">
                                <label for="input-myform-myarray-0-0-f2">F2</label>
                                <input class="text" id="input-myform-myarray-0-0-f2"
                                       name="myform.myarray.0.0.f2" type="text"
                                       value="Value 0.0 F2"/>
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
                                <input class="text" id="input-myform-myarray-0-1-f1"
                                       name="myform.myarray.0.1.f1" type="text"
                                       value="Value 0.1 F1"/>
                              </div>
                              <div class="field" id="field-myform-myarray-0-1-f2">
                                <label for="input-myform-myarray-0-1-f2">F2</label>
                                <input class="text" id="input-myform-myarray-0-1-f2"
                                       name="myform.myarray.0.1.f2" type="text"
                                       value="Value 0.1 F2"/>
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
              <div class="array array-add array-remove array-sort"
                   id="array-myform-myarray-TEMPLATE">
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
                    <input class="text" id="input-myform-myarray-TEMPLATE-TEMPLATE-f1"
                           name="myform.myarray.TEMPLATE.TEMPLATE.f1"
                           type="text" value=""/>
                  </div>
                  <div class="field" id="field-myform-myarray-TEMPLATE-TEMPLATE-f2">
                    <label for="input-myform-myarray-TEMPLATE-TEMPLATE-f2">F2</label>
                    <input class="text" id="input-myform-myarray-TEMPLATE-TEMPLATE-f2"
                           name="myform.myarray.TEMPLATE.TEMPLATE.f2" type="text"
                           value=""/>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </form>
        """, fxml(rendered))

        # default values as dict
        form['myarray'] = factory(
            'array',
            value={
                '0': {
                    '0': {
                        'f1': 'Value 0.0 F1',
                        'f2': 'Value 0.0 F2',
                    },
                    '1': {
                        'f1': 'Value 0.1 F1',
                        'f2': 'Value 0.1 F2',
                    },
                },
            },
            props={'label': 'My Compound Array'})
        form['myarray']['subarray'] = factory(
            'array',
            props={'label': 'Subarray'})
        form['myarray']['subarray']['mycompound'] = factory('compound')
        form['myarray']['subarray']['mycompound']['f1'] = factory(
            'field:label:text',
            props={'label': 'F1'})
        form['myarray']['subarray']['mycompound']['f2'] = factory(
            'field:label:text',
            props={'label': 'F2'})
        self.assertEqual(rendered, form())

        # default values mixed
        form['myarray'] = factory(
            'array',
            value=[
                {
                    '0': {
                        'f1': 'Value 0.0 F1',
                        'f2': 'Value 0.0 F2',
                    },
                    '1': {
                        'f1': 'Value 0.1 F1',
                        'f2': 'Value 0.1 F2',
                    },
                },
            ],
            props={'label': 'My Compound Array'})
        form['myarray']['subarray'] = factory(
            'array',
            props={'label': 'Subarray'})
        form['myarray']['subarray']['mycompound'] = factory('compound')
        form['myarray']['subarray']['mycompound']['f1'] = factory(
            'field:label:text',
            props={'label': 'F1'})
        form['myarray']['subarray']['mycompound']['f2'] = factory(
            'field:label:text',
            props={'label': 'F2'})
        self.assertEqual(rendered, form())

    def test_array_with_single_fields_extraction(self):
        # without preset values
        form = factory(
            'form',
            name='myform',
            props={'action': 'myaction'})
        form['myarray'] = factory(
            'array',
            props={'label': 'My Array'})
        form['myarray']['myfield'] = factory(
            'field:label:text',
            props={'label': 'My Field'})
        request = {
            'myform.myarray.0': '1',
            'myform.myarray.1': '2',
            'myform.myarray.2': '3',
            'myform.myarray.3': '4',
        }
        data = form.extract(request=request)
        self.assertEqual(
            [data.name, data.value, data.extracted, data.errors],
            ['myform', UNSET, odict([('myarray', ['1', '2', '3', '4'])]), []]
        )
        arrd = data['myarray']
        self.assertEqual(len(arrd), 4)
        self.assertEqual(
            [arrd.name, arrd.value, arrd.extracted, arrd.errors],
            ['myarray', UNSET, ['1', '2', '3', '4'], []]
        )
        arrd0 = data['myarray']['0']
        self.assertEqual(
            [arrd0.name, arrd0.value, arrd0.extracted, arrd0.errors],
            [ '0', UNSET, '1', []]
        )
        arrd1 = data['myarray']['1']
        self.assertEqual(
            [arrd1.name, arrd1.value, arrd1.extracted, arrd1.errors],
            [ '1', UNSET, '2', []]
        )
        arrd2 = data['myarray']['2']
        self.assertEqual(
            [arrd2.name, arrd2.value, arrd2.extracted, arrd2.errors],
            [ '2', UNSET, '3', []]
        )
        arrd3 = data['myarray']['3']
        self.assertEqual(
            [arrd3.name, arrd3.value, arrd3.extracted, arrd3.errors],
            [ '3', UNSET, '4', []]
        )

        # with preset values
        form['myarray'] = factory(
            'array',
            value=['4', '3', '2', '1'],
            props={'label': 'My Array'})
        form['myarray']['myfield'] = factory(
            'field:label:text',
            props={'label': 'My Field'})
        request = {
            'myform.myarray.0': '41',
            'myform.myarray.1': '31',
            'myform.myarray.2': '21',
            'myform.myarray.3': '11',
        }
        data = form.extract(request=request)
        self.assertEqual(
            [data.name, data.value, data.extracted, data.errors],
            ['myform', UNSET, odict([('myarray', ['41', '31', '21', '11'])]), []]
        )
        arrd = data['myarray']
        self.assertEqual(len(arrd), 4)
        self.assertEqual(
            [arrd.name, arrd.value, arrd.extracted, arrd.errors],
            ['myarray', ['4', '3', '2', '1'], ['41', '31', '21', '11'], []]
        )
        arrd0 = data['myarray']['0']
        self.assertEqual(
            [arrd0.name, arrd0.value, arrd0.extracted, arrd0.errors],
            [ '0', UNSET, '41', []]
        )
        arrd1 = data['myarray']['1']
        self.assertEqual(
            [arrd1.name, arrd1.value, arrd1.extracted, arrd1.errors],
            [ '1', UNSET, '31', []]
        )
        arrd2 = data['myarray']['2']
        self.assertEqual(
            [arrd2.name, arrd2.value, arrd2.extracted, arrd2.errors],
            [ '2', UNSET, '21', []]
        )
        arrd3 = data['myarray']['3']
        self.assertEqual(
            [arrd3.name, arrd3.value, arrd3.extracted, arrd3.errors],
            [ '3', UNSET, '11', []]
        )

        # entries increased in UI
        request = {
            'myform.myarray.0': 'a',
            'myform.myarray.1': 'b',
            'myform.myarray.2': 'c',
            'myform.myarray.3': 'd',
            'myform.myarray.4': 'e',
        }
        data = form.extract(request=request)
        self.assertEqual(
            [data.name, data.value, data.extracted, data.errors],
            ['myform', UNSET, odict([('myarray', ['a', 'b', 'c', 'd', 'e'])]), []]
        )
        arrd = data['myarray']
        self.assertEqual(len(arrd), 5)
        self.assertEqual(
            [arrd.name, arrd.value, arrd.extracted, arrd.errors],
            ['myarray', ['4', '3', '2', '1'], ['a', 'b', 'c', 'd', 'e'], []]
        )
        arrd0 = data['myarray']['0']
        self.assertEqual(
            [arrd0.name, arrd0.value, arrd0.extracted, arrd0.errors],
            [ '0', UNSET, 'a', []]
        )
        arrd1 = data['myarray']['1']
        self.assertEqual(
            [arrd1.name, arrd1.value, arrd1.extracted, arrd1.errors],
            [ '1', UNSET, 'b', []]
        )
        arrd2 = data['myarray']['2']
        self.assertEqual(
            [arrd2.name, arrd2.value, arrd2.extracted, arrd2.errors],
            [ '2', UNSET, 'c', []]
        )
        arrd3 = data['myarray']['3']
        self.assertEqual(
            [arrd3.name, arrd3.value, arrd3.extracted, arrd3.errors],
            [ '3', UNSET, 'd', []]
        )
        arrd4 = data['myarray']['4']
        self.assertEqual(
            [arrd4.name, arrd4.value, arrd4.extracted, arrd4.errors],
            [ '4', UNSET, 'e', []]
        )

        # entries decreased in UI
        request = {
            'myform.myarray.0': 'x',
            'myform.myarray.1': 'y',
            'myform.myarray.2': 'z',
        }
        data = form.extract(request=request)
        self.assertEqual(
            [data.name, data.value, data.extracted, data.errors],
            ['myform', UNSET, odict([('myarray', ['x', 'y', 'z'])]), []]
        )
        arrd = data['myarray']
        self.assertEqual(len(arrd), 3)
        self.assertEqual(
            [arrd.name, arrd.value, arrd.extracted, arrd.errors],
            ['myarray', ['4', '3', '2', '1'], ['x', 'y', 'z'], []]
        )
        arrd0 = data['myarray']['0']
        self.assertEqual(
            [arrd0.name, arrd0.value, arrd0.extracted, arrd0.errors],
            [ '0', UNSET, 'x', []]
        )
        arrd1 = data['myarray']['1']
        self.assertEqual(
            [arrd1.name, arrd1.value, arrd1.extracted, arrd1.errors],
            [ '1', UNSET, 'y', []]
        )
        arrd2 = data['myarray']['2']
        self.assertEqual(
            [arrd2.name, arrd2.value, arrd2.extracted, arrd2.errors],
            [ '2', UNSET, 'z', []]
        )

    def test_array_required_extraction(self):
        form = factory(
            'form',
            name='myform',
            props={'action': 'myaction'})
        form['myarray'] = factory(
            'error:array',
            value=['4', '3', '2', '1'],
            props={
                'label': 'My Array',
                'required': 'Array is required',
            })
        form['myarray']['myfield'] = factory(
            'field:label:text',
            props={'label': 'My Field'})
        request = {}
        data = form.extract(request=request)
        self.assertEqual(
            [data.name, data.value, data.extracted, data.errors],
            ['myform', UNSET, odict([('myarray', [])]), []]
        )
        arrd = data['myarray']
        self.assertEqual(len(arrd), 0)
        self.assertEqual(
            [arrd.name, arrd.value, arrd.extracted, arrd.errors],
            [
                'myarray',
                ['4', '3', '2', '1'],
                [],
                [ExtractionError('Array is required')]
            ]
        )

        self.check_output("""
        <form action="myaction" enctype="multipart/form-data" id="form-myform" method="post" novalidate="novalidate">
          <div class="error">
            <div class="errormessage">Array is required</div>
            <div class="array error array-add array-remove array-sort" id="array-myform-myarray">
              ...
            </div>
          </div>
        </form>
        """, fxml(form(data=data)))

    def test_array_field_required_extraction(self):
        form = factory(
            'form',
            name='myform',
            props={'action': 'myaction'})
        form['myarray'] = factory(
            'array',
            props={'label': 'My Array'})
        form['myarray']['myfield'] = factory(
            'field:label:error:text',
            props={
                'label': 'My Field',
                'required': 'My Field is required',
            })
        request = {
            'myform.myarray.0': '0',
            'myform.myarray.1': '',
        }

        data = form.extract(request=request)
        self.assertEqual(
            [data.name, data.value, data.extracted, data.errors],
            ['myform', UNSET, odict([('myarray', ['0', ''])]), []]
        )
        arrd = data['myarray']
        self.assertEqual(
            [arrd.name, arrd.value, arrd.extracted, arrd.errors],
            ['myarray', UNSET, ['0', ''], []]
        )
        arrd0 = data['myarray']['0']
        self.assertEqual(
            [arrd0.name, arrd0.value, arrd0.extracted, arrd0.errors],
            ['0', UNSET, '0', []]
        )
        arrd1 = data['myarray']['1']
        self.assertEqual(
            [arrd1.name, arrd1.value, arrd1.extracted, arrd1.errors],
            ['1', UNSET, '', [ExtractionError('My Field is required')]]
        )

        self.check_output("""
        <form action="myaction" enctype="multipart/form-data" id="form-myform"
              method="post" novalidate="novalidate">
          <div class="array array-add array-remove array-sort"
               id="array-myform-myarray">
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
                        <input class="required text"
                               id="input-myform-myarray-1"
                               name="myform.myarray.1"
                               required="required"
                               type="text"
                               value=""/>
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
        """, fxml(form(data)))

    def test_array_with_compound_fields_extraction(self):
        form = factory(
            'form',
            name='myform',
            props={'action': 'myaction'})
        form['myarray'] = factory(
            'array',
            props={'label': 'My Compound Array'})
        form['myarray']['mycompound'] = factory('compound')
        form['myarray']['mycompound']['f1'] = factory(
            'field:label:text',
            props={'label': 'F1'})
        form['myarray']['mycompound']['f2'] = factory(
            'field:label:text',
            props={'label': 'F2'})
        request = {
            'myform.myarray.0.f1': '1',
            'myform.myarray.0.f2': '2',
            'myform.myarray.1.f1': '3',
            'myform.myarray.1.f2': '4',
        }
        data = form.extract(request=request)
        extracted = odict([
            ('myarray', [
                odict([('f1', '1'), ('f2', '2')]),
                odict([('f1', '3'), ('f2', '4')])
            ])
        ])
        self.assertEqual(
            [data.name, data.value, data.extracted, data.errors],
            ['myform', UNSET, extracted, []]
        )
        arrd = data['myarray']
        self.assertEqual(len(arrd), 2)
        extracted = [
            odict([('f1', '1'), ('f2', '2')]),
            odict([('f1', '3'), ('f2', '4')])
        ]
        self.assertEqual(
            [arrd.name, arrd.value, arrd.extracted, arrd.errors],
            ['myarray', UNSET, extracted, []]
        )
        c0 = data['myarray']['0']
        self.assertEqual(len(c0), 2)
        self.assertEqual(
            [c0.name, c0.value, c0.extracted, c0.errors],
            ['0', UNSET, odict([('f1', '1'), ('f2', '2')]), []]
        )
        c0f1 = data['myarray']['0']['f1']
        self.assertEqual(
            [c0f1.name, c0f1.value, c0f1.extracted, c0f1.errors],
            ['f1', UNSET, '1', []]
        )
        c0f2 = data['myarray']['0']['f2']
        self.assertEqual(
            [c0f2.name, c0f2.value, c0f2.extracted, c0f2.errors],
            ['f2', UNSET, '2', []]
        )
        c1 = data['myarray']['1']
        self.assertEqual(len(c1), 2)
        self.assertEqual(
            [c1.name, c1.value, c1.extracted, c1.errors],
            ['1', UNSET, odict([('f1', '3'), ('f2', '4')]), []]
        )
        c1f1 = data['myarray']['1']['f1']
        self.assertEqual(
            [c1f1.name, c1f1.value, c1f1.extracted, c1f1.errors],
            ['f1', UNSET, '3', []]
        )
        c1f2 = data['myarray']['1']['f2']
        self.assertEqual(
            [c1f2.name, c1f2.value, c1f2.extracted, c1f2.errors],
            ['f2', UNSET, '4', []]
        )

    def test_array_in_array_with_single_fields_extraction(self):
        form = factory(
            'form',
            name='myform',
            props={'action': 'myaction'})
        form['myarray'] = factory(
            'array',
            value=[
                ['1', '2'],
                ['4', '5'],
            ],
            props={'label': 'My Array Array'})
        form['myarray']['subarray'] = factory(
            'array',
            props={'label': 'Subrray'})
        form['myarray']['subarray']['myfield'] = factory(
            'field:label:text',
            props={'label': 'My Field'})
        request = {
            'myform.myarray.0.0': '1',
            'myform.myarray.0.1': '2',
            'myform.myarray.1.0': '3',
            'myform.myarray.1.1': '4',
        }
        data = form.extract(request=request)
        extracted = odict([('myarray', [['1', '2'], ['3', '4']])])
        self.assertEqual(
            [data.name, data.value, data.extracted, data.errors],
            ['myform', UNSET, extracted, []]
        )
        arrd = data['myarray']
        self.assertEqual(len(arrd), 2)
        value = [['1', '2'], ['4', '5']]
        extracted = [['1', '2'], ['3', '4']]
        self.assertEqual(
            [arrd.name, arrd.value, arrd.extracted, arrd.errors],
            ['myarray', value, extracted, []]
        )
        a0 = data['myarray']['0']
        self.assertEqual(len(a0), 2)
        self.assertEqual(
            [a0.name, a0.value, a0.extracted, a0.errors],
            ['0', UNSET, ['1', '2'], []]
        )
        a0_0 = data['myarray']['0']['0']
        self.assertEqual(
            [a0_0.name, a0_0.value, a0_0.extracted, a0_0.errors],
            ['0', UNSET, '1', []]
        )
        a0_1 = data['myarray']['0']['1']
        self.assertEqual(
            [a0_1.name, a0_1.value, a0_1.extracted, a0_1.errors],
            ['1', UNSET, '2', []]
        )
        a1 = data['myarray']['1']
        self.assertEqual(len(a1), 2)
        self.assertEqual(
            [a1.name, a1.value, a1.extracted, a1.errors],
            ['1', UNSET, ['3', '4'], []]
        )
        a1_0 = data['myarray']['1']['0']
        self.assertEqual(
            [a1_0.name, a1_0.value, a1_0.extracted, a1_0.errors],
            ['0', UNSET, '3', []]
        )
        a1_1 = data['myarray']['1']['1']
        self.assertEqual(
            [a1_1.name, a1_1.value, a1_1.extracted, a1_1.errors],
            ['1', UNSET, '4', []]
        )

    def test_array_in_array_with_compound_fields_extraction(self):
        form = factory(
            'form',
            name='myform',
            props={'action': 'myaction'})
        form['myarray'] = factory(
            'array',
            props={'label': 'My Compound Array'})
        form['myarray']['subarray'] = factory(
            'array',
            props={'label': 'Subarray'})
        form['myarray']['subarray']['mycompound'] = factory('compound')
        form['myarray']['subarray']['mycompound']['f1'] = factory(
            'field:label:text',
            props={'label': 'F1'})
        form['myarray']['subarray']['mycompound']['f2'] = factory(
            'field:label:text',
            props={'label': 'F2'})
        request = {
            'myform.myarray.0.0.f1': '1',
            'myform.myarray.0.0.f2': '2',
            'myform.myarray.1.0.f1': '3',
            'myform.myarray.1.0.f2': '4',
            'myform.myarray.1.1.f1': '5',
            'myform.myarray.1.1.f2': '6',
        }
        data = form.extract(request=request)
        extracted = odict([
            ('myarray', [
                [
                    odict([('f1', '1'), ('f2', '2')])
                ], [
                    odict([('f1', '3'), ('f2', '4')]),
                    odict([('f1', '5'), ('f2', '6')])
                ]
            ])
        ])
        self.assertEqual(
            [data.name, data.value, data.extracted, data.errors],
            ['myform', UNSET, extracted, []]
        )
        arrd0 = data['myarray']
        self.assertEqual(len(arrd0), 2)
        extracted = [
            [
                odict([('f1', '1'), ('f2', '2')])
            ], [
                odict([('f1', '3'), ('f2', '4')]),
                odict([('f1', '5'), ('f2', '6')])
            ]
        ]
        self.assertEqual(
            [arrd0.name, arrd0.value, arrd0.extracted, arrd0.errors],
            ['myarray', UNSET, extracted, []]
        )
        a0 = data['myarray']['0']
        self.assertEqual(len(a0), 1)
        extracted = [odict([('f1', '1'), ('f2', '2')])]
        self.assertEqual(
            [a0.name, a0.value, a0.extracted, a0.errors],
            ['0', UNSET, extracted, []]
        )
        a0_0 = data['myarray']['0']['0']
        self.assertEqual(len(a0_0), 2)
        extracted = odict([('f1', '1'), ('f2', '2')])
        self.assertEqual(
            [a0_0.name, a0_0.value, a0_0.extracted, a0_0.errors],
            ['0', UNSET, extracted, []]
        )
        a0_0f1 = data['myarray']['0']['0']['f1']
        self.assertEqual(
            [a0_0f1.name, a0_0f1.value, a0_0f1.extracted, a0_0f1.errors],
            ['f1', UNSET, '1', []]
        )
        a0_0f2 = data['myarray']['0']['0']['f2']
        self.assertEqual(
            [a0_0f2.name, a0_0f2.value, a0_0f2.extracted, a0_0f2.errors],
            ['f2', UNSET, '2', []]
        )
        a1 = data['myarray']['1']
        self.assertEqual(len(a1), 2)
        extracted = [
            odict([('f1', '3'), ('f2', '4')]),
            odict([('f1', '5'), ('f2', '6')])
        ]
        self.assertEqual(
            [a1.name, a1.value, a1.extracted, a1.errors],
            ['1', UNSET, extracted, []]
        )
        a1_0 = data['myarray']['1']['0']
        self.assertEqual(len(a1_0), 2)
        extracted = odict([('f1', '3'), ('f2', '4')])
        self.assertEqual(
            [a1_0.name, a1_0.value, a1_0.extracted, a1_0.errors],
            ['0', UNSET, extracted, []]
        )
        a1_0f1 = data['myarray']['1']['0']['f1']
        self.assertEqual(
            [a1_0f1.name, a1_0f1.value, a1_0f1.extracted, a1_0f1.errors],
            ['f1', UNSET, '3', []]
        )
        a1_0f2 = data['myarray']['1']['0']['f2']
        self.assertEqual(
            [a1_0f2.name, a1_0f2.value, a1_0f2.extracted, a1_0f2.errors],
            ['f2', UNSET, '4', []]
        )
        a1_1 = data['myarray']['1']['1']
        self.assertEqual(len(a1_1), 2)
        extracted = odict([('f1', '5'), ('f2', '6')])
        self.assertEqual(
            [a1_1.name, a1_1.value, a1_1.extracted, a1_1.errors],
            ['1', UNSET, extracted, []]
        )
        a1_1f1 = data['myarray']['1']['1']['f1']
        self.assertEqual(
            [a1_1f1.name, a1_1f1.value, a1_1f1.extracted, a1_1f1.errors],
            ['f1', UNSET, '5', []]
        )
        a1_1f2 = data['myarray']['1']['1']['f2']
        self.assertEqual(
            [a1_1f2.name, a1_1f2.value, a1_1f2.extracted, a1_1f2.errors],
            ['f2', UNSET, '6', []]
        )

    def test_array_hidden_proxy_for_display_mode_children(self):
        # ``yafowil.widget.array`` differs in value extraction when rerendering
        # forms. Normally the value gets fetched from the getter if not found
        # on request. Since it's hard to reference the origin value for array
        # entries if not found on request - you have possibly a mutable array
        # containing componds with some fields disabled or in display mode - a
        # hidden field is added for such widgets in the tree on the fly in
        # order to rerender forms correctly
        form = factory(
            'form',
            name='myform',
            props={'action': 'myaction'})
        form['myarray'] = factory(
            'array',
            value=[{'f1': 'foo1', 'f2': 'foo2'}],
            props={'label': 'My Compound Array with display children'})
        form['myarray']['mycompound'] = factory('compound')
        form['myarray']['mycompound']['f1'] = factory(
            'field:label:text',
            props={'label': 'F1'},
            mode='display')
        form['myarray']['mycompound']['f2'] = factory(
            'field:label:text',
            props={'label': 'F2', 'disabled': 'disabled'})
        self.check_output("""
        <form action="myaction" enctype="multipart/form-data" id="form-myform"
              method="post" novalidate="novalidate">
          <div class="array array-add array-remove array-sort"
               id="array-myform-myarray">
            <table>
              ...
                  <td class="widget">
                    <input id="input-myform-myarray-0-f1"
                           name="myform.myarray.0.f1"
                           type="hidden" value="foo1"/>
                    <div class="field" id="field-myform-myarray-0-f1">
                      <label>F1</label>
                      <div class="display-text"
                           id="display-myform-myarray-0-f1">foo1</div>
                    </div>
                    <input id="input-myform-myarray-0-f2"
                           name="myform.myarray.0.f2"
                           type="hidden" value="foo2"/>
                    <div class="field" id="field-myform-myarray-0-f2">
                      <label for="input-myform-myarray-0-f2">F2</label>
                      <input class="text" disabled="disabled"
                             id="input-myform-myarray-0-f2"
                             name="myform.myarray.0.f2"
                             type="text" value="foo2"/>
                    </div>
                  </td>
                  ...
            </table>
            ...
        </form>
        """, fxml(form()))

    def test_callable_array_label(self):
        form = factory(
            'form',
            name='myform',
            props={'action': 'myaction'})
        form['myarray'] = factory(
            'array',
            props={'label': lambda: 'Callable label'})
        form['myarray']['f1'] = factory(
            'field:label:text',
            props={'label': 'F1'},
            mode='display')
        self.check_output("""
        <form action="myaction" enctype="multipart/form-data" id="form-myform"
              method="post" novalidate="novalidate">
          <div class="array array-add array-remove array-sort"
               id="array-myform-myarray">
            <table>
              <thead>
                <tr>
                  <th>Callable label</th>
                  ...
        </form>
        """, fxml(form()))

    def test_3_dimensional_array(self):
        form = factory(
            'form',
            name='myform',
            props={'action': 'myaction'})
        arr_1 = form['array_1'] = factory(
            'array',
            value=[
                [
                    ['1'],
                ],
                [
                    ['2'],
                ],
            ],
            props={
                'label': 'Array 1',
            })
        arr_2 = arr_1['array_2'] = factory(
            'array',
            props={
                'label': 'Array 2',
            })
        arr_3 = arr_2['array_3'] = factory(
            'array',
            props={
                'label': 'Array 3',
            })
        arr_3['textfield'] = factory(
            'field:error:label:text',
            props={
                'label': 'Text Field',
                'required': 'Text Field is required',
            })

        self.assertEqual(form.treerepr().split('\n'), [
            "<class 'yafowil.base.Widget'>: myform",
            "  <class 'yafowil.base.Widget'>: array_1",
            "    <class 'yafowil.base.Widget'>: table",
            "      <class 'yafowil.base.Widget'>: head",
            "        <class 'yafowil.base.Widget'>: row",
            "          <class 'yafowil.base.Widget'>: label",
            "          <class 'yafowil.base.Widget'>: actions",
            "      <class 'yafowil.base.Widget'>: body",
            "    <class 'yafowil.base.Widget'>: array_2",
            "      <class 'yafowil.base.Widget'>: table",
            "        <class 'yafowil.base.Widget'>: head",
            "          <class 'yafowil.base.Widget'>: row",
            "            <class 'yafowil.base.Widget'>: label",
            "            <class 'yafowil.base.Widget'>: actions",
            "        <class 'yafowil.base.Widget'>: body",
            "      <class 'yafowil.base.Widget'>: array_3",
            "        <class 'yafowil.base.Widget'>: table",
            "          <class 'yafowil.base.Widget'>: head",
            "            <class 'yafowil.base.Widget'>: row",
            "              <class 'yafowil.base.Widget'>: label",
            "              <class 'yafowil.base.Widget'>: actions",
            "          <class 'yafowil.base.Widget'>: body",
            "        <class 'yafowil.base.Widget'>: textfield",
            ""
        ])

        self.check_output("""
        <form action="myaction" enctype="multipart/form-data" id="form-myform"
              method="post" novalidate="novalidate">
          <div class="array array-add array-remove array-sort"
               id="array-myform-array_1">
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
                    <div class="array array-add array-remove array-sort"
                         id="array-myform-array_1-0">
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
                              <div class="array array-add array-remove array-sort"
                                   id="array-myform-array_1-0-0">
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
                                          <input class="required text"
                                                 id="input-myform-array_1-0-0-0"
                                                 name="myform.array_1.0.0.0"
                                                 required="required"
                                                 type="text" value="1"/>
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
                                    <input class="required text"
                                           id="input-myform-array_1-0-0-TEMPLATE"
                                           name="myform.array_1.0.0.TEMPLATE"
                                           required="required"
                                           type="text" value=""/>
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
                            <div class="field"
                                 id="field-myform-array_1-0-TEMPLATE-TEMPLATE">
                              <label for="input-myform-array_1-0-TEMPLATE-TEMPLATE">Text Field</label>
                              <input class="required text"
                                     id="input-myform-array_1-0-TEMPLATE-TEMPLATE"
                                     name="myform.array_1.0.TEMPLATE.TEMPLATE"
                                     required="required"
                                     type="text" value=""/>
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
              <div class="array array-add array-remove array-sort"
                   id="array-myform-array_1-TEMPLATE">
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
                  <div class="array array-add array-remove array-sort"
                       id="array-myform-array_1-TEMPLATE-TEMPLATE">
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
                        <input class="required text"
                               id="input-myform-array_1-TEMPLATE-TEMPLATE-TEMPLATE"
                               name="myform.array_1.TEMPLATE.TEMPLATE.TEMPLATE"
                               required="required" type="text" value=""/>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </form>
        """, fxml(form()))


if __name__ == '__main__':
    unittest.main()                                          # pragma: no cover
