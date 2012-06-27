from yafowil.base import factory


DOC_ARRAY_WITH_LEAFS = """
Array with single fields as array entries
-----------------------------------------

Array containing single field entries. Preset value is expected as list.

.. code-block:: python

    array = factory('#array', value=['1', '2', '3'], props={
                    'label': 'My Array'})
    array['field'] = factory('field:error:label:text', props={
                             'label': 'Some Field',
                             'required': 'Some Field is required'})

"""

def array_with_leafs():
    form = factory('fieldset', name='yafowil.widget.array.array_with_leafs')
    arr = form['somearray'] = factory('#array', value=['1', '2', '3'], props={
                                      'label': 'My Array'})
    arr['somefield'] = factory('field:error:label:text', props={
                               'label': 'Field',
                               'required': 'Field is required'})
    return {'widget': form,
            'doc': DOC_ARRAY_WITH_LEAFS,
            'title': 'Single field array'}


DOC_ARRAY_WITH_COMPOUNDS = """
Array with compounds as array entries
-------------------------------------

Array containing compound entries. Preset value is expected as list containing
dictionaries addressing array child compound fields by key.

.. code-block:: python
    
    value = [{'f1': 'Value 1.1 F1', 'f2': 'Value 1.2 F2'},
             {'f1': 'Value 2.1 F1', 'f2': 'Value 2.2 F2'}]
    array = factory('#array', value=value, props={
                    'label': 'Compound Array'})
    compound = array['compound'] = factory('compound')
    compound['f1'] = factory('field:label:text', props={
                             'label': 'Field 1'})
    compound['f2'] = factory('field:error:label:text', props={
                             'label': 'Field 2',
                             'required': 'Field 2 is required'})

"""

def array_with_compounds():
    form = factory('fieldset',
                   name='yafowil.widget.array.array_with_compounds')
    value = [{'f1': 'Value 1.1 F1', 'f2': 'Value 1.2 F2'},
             {'f1': 'Value 2.1 F1', 'f2': 'Value 2.2 F2'}]
    arr = form['compoundarray'] = factory('#array', value=value, props={
                                          'label': 'Compound Array'})
    comp = arr['somecompound'] = factory('compound')
    comp['f1'] = factory('field:label:text', props={
                         'label': 'Field 1'})
    comp['f2'] = factory('field:error:label:text', props={
                         'label': 'Field 2',
                         'required': 'Field 2 is required'})
    return {'widget': form,
            'doc': DOC_ARRAY_WITH_COMPOUNDS,
            'title': 'Compound field array'}


DOC_ARRAY_WITH_ARRAY_WITH_LEAFS = """
Array in array with single fields
---------------------------------

Array in array containing single field entries. Preset value is a 2-dimensional
list

.. code-block:: python
    
    value = [['1', '2'], ['3', '4'], ['5', '6']]
    array = factory('#array', value=value, props={
                    'label': 'Array Array'})
    subarray = array['subarray'] = factory(
        '#array', props={'label': 'Some Array'})
    subarray['field'] = factory(
        'field:error:label:text', props={
        'label': 'Some Field',
        'required': 'Some Field is required'})

"""

def array_with_array_with_leafs():
    form = factory('fieldset',
                   name='yafowil.widget.array_with_array_with_leafs')
    value = [['1', '2'], ['3', '4'], ['5', '6']]
    arr = form['arrayarray'] = factory('#array', value=value, props={
                                       'label': 'Array Array'})
    subarr = arr['somearray'] = factory('#array', props={
                                        'label': 'Some Array'})
    subarr['somefield'] = factory('field:error:label:text', props={
                                  'label': 'Some Field',
                                  'required': 'Some Field is required'})
    return {'widget': form,
            'doc': DOC_ARRAY_WITH_ARRAY_WITH_LEAFS,
            'title': 'Single field array in array'}


DOC_ARRAY_WITH_ARRAY_WITH_COMPOUNDS = """\
Array in array with compounds as array entries
----------------------------------------------

Array in array containing compound entries. Preset value is lists in list 
containing dictionaries addressing inner array child compound fields by key.

.. code-block:: python
    
    value = [[{'f1': 'Value 0.0 F1', 'f2': 'Value 0.0 F2'},
              {'f1': 'Value 0.1 F1', 'f2': 'Value 0.1 F2'}],
             [{'f1': 'Value 1.0 F1', 'f2': 'Value 1.0 F2'},
              {'f1': 'Value 1.1 F1', 'f2': 'Value 1.1 F2'}]]
    array = factory('#array', value=value, props={'label': 'Array 1'})
    subarray = array['subarray'] = factory(
        '#array', props={'label': 'Array 2'})
    compound = subarray['comp'] = factory('compound')
    compound['f1'] = factory('field:label:text', props={
                             'label': 'F1'})
    compound['f2'] = factory('field:error:label:text', props={
                             'label': 'F2',
                             'required': 'F2 is required'})

"""

def array_with_array_with_compounds():
    form = factory('fieldset',
                   name='yafowil.widget.array_with_array_with_compounds')
    value = [[{'f1': 'Value 0.0 F1', 'f2': 'Value 0.0 F2'},
              {'f1': 'Value 0.1 F1', 'f2': 'Value 0.1 F2'}],
             [{'f1': 'Value 1.0 F1', 'f2': 'Value 1.0 F2'},
              {'f1': 'Value 1.1 F1', 'f2': 'Value 1.1 F2'}]]
    arr = form['arrayarraycomp'] = factory('#array', value=value, props={
                                           'label': 'Array 1'})
    subarr = arr['subarray'] = factory('#array', props={
                                       'label': 'Array 2'})
    comp = subarr['comp'] = factory('compound')
    comp['f1'] = factory('field:label:text', props={
                         'label': 'F1'})
    comp['f2'] = factory('field:error:label:text', props={
                         'label': 'F2',
                         'required': 'F2 is required'})
    return {'widget': form,
            'doc': DOC_ARRAY_WITH_ARRAY_WITH_COMPOUNDS,
            'title': 'Compound array in array'}


DOC_ARRAY_WITH_ARRAY_WITH_ARRAY_WITH_LEAFS = """\
3-Dimensional Array with single fields
--------------------------------------

3-Dimensional array containing single field entries. Preset value is a
3-dimensional list

.. code-block:: python

    value = [[['1', '2'], ['3']], [['4', '5']]]
    arr_1 = factory('#array', value=value, props={
                    'label': 'Array 1'})
    arr_2 = arr_1['array_2'] = factory('#array', props={
                                       'label': 'Array 2'})
    arr_3 = arr_2['array_3'] = factory('#array', props={
                                       'label': 'Array 3'})
    arr_3['field'] = factory('field:error:label:text', props={
                             'label': 'Text Field',
                             'required': 'Text Field is required'})

"""

def array_with_array_with_array_with_leafs():
    form = factory(
        'fieldset',
        name='yafowil.widget.array_with_array_with_array_with_leafs')
    value = [[['1', '2'], ['3']], [['4', '5']]]
    arr_1 = form['array_1'] = factory('#array', value=value, props={
                                      'label': 'Array 1'})
    arr_2 = arr_1['array_2'] = factory('#array', props={
                                       'label': 'Array 2'})
    arr_3 = arr_2['array_3'] = factory('#array', props={
                                       'label': 'Array 3'})
    arr_3['textfield'] = factory('field:error:label:text', props={
                                 'label': 'Text Field',
                                 'required': 'Text Field is required'})
    return {'widget': form,
            'doc': DOC_ARRAY_WITH_ARRAY_WITH_ARRAY_WITH_LEAFS,
            'title': 'Single fields in 3-dimensional array'}


DOC_ARRAY_WITH_ARRAY_WITH_ARRAY_WITH_COMPOUNDS = """\
3-Dimensional Array with compounds
----------------------------------

3-Dimensional array containing compound entries. Preset value is a
3-dimensional list containing dictionaries addressing most inner array child
compound fields by key.

.. code-block:: python

    value = [[[{'f1': 'Value F1', 'f2': 'Value F2'}]],
             [[{'f1': 'Value F1', 'f2': 'Value F2'}]]]
    arr_1 = factory('#array', value=value, props={
                    'label': 'Array 1'})
    arr_2 = arr_1['array_2'] = factory('#array', props={
                                       'label': 'Array 2'})
    arr_3 = arr_2['array_3'] = factory('#array', props={
                                       'label': 'Array 3'})
    compound = arr_3['comp'] = factory('compound')
    compound['f1'] = factory('field:label:text', props={
                             'label': 'F1'})
    compound['f2'] = factory('field:error:label:text', props={
                             'label': 'F2',
                            'required': 'F2 is required'})

"""

def array_with_array_with_array_with_compounds():
    form = factory(
        'fieldset',
        name='yafowil.widget.array_with_array_with_array_with_compounds')
    value = [[[{'f1': 'Value F1', 'f2': 'Value F2'}]],
             [[{'f1': 'Value F1', 'f2': 'Value F2'}]]]
    arr_1 = form['comp_array_1'] = factory('#array', value=value, props={
                                           'label': 'Array 1'})
    arr_2 = arr_1['array_2'] = factory('#array', props={
                                       'label': 'Array 2'})
    arr_3 = arr_2['array_3'] = factory('#array', props={
                                       'label': 'Array 3'})
    comp = arr_3['comp'] = factory('compound')
    comp['f1'] = factory('field:label:text', props={
                         'label': 'F1'})
    comp['f2'] = factory('field:error:label:text', props={
                         'label': 'F2',
                         'required': 'F2 is required'})
    return {'widget': form,
            'doc': DOC_ARRAY_WITH_ARRAY_WITH_ARRAY_WITH_COMPOUNDS,
            'title': 'Compounds in 3-dimensional array'}


def get_example():
    return [
        array_with_leafs(),
        array_with_compounds(),
        array_with_array_with_leafs(),
        array_with_array_with_compounds(),
        array_with_array_with_array_with_leafs(),
        array_with_array_with_array_with_compounds(),
    ]