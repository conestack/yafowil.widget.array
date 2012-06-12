from yafowil.base import factory


def add_array_with_leafs(form):
    arr = form['somearray'] = factory(
        'array',
        value=['1', '2', '3'],
        props={
            'label': 'My Array',
        })
    arr['somefield'] = factory(
        'field:error:label:text',
        props={
            'label': 'Some Field',
            'required': 'Some Field is required',
        })


def add_array_with_compounds(form):
    arr = form['compoundarray'] = factory(
        'array',
        value=[
            {
                'f1': 'Value 1.1 F1',
                'f2': 'Value 1.2 F2',
            },
            {
                'f1': 'Value 2.1 F1',
                'f2': 'Value 2.2 F2',
            },
        ],
        props={
            'label': 'Compound Array',
        })
    comp = arr['somecompound'] = factory('compound')
    comp['f1'] = factory(
        'field:label:text',
        props={
            'label': 'Field 1',
        })
    comp['f2'] = factory(
        'field:error:label:text',
        props={
            'label': 'Field 2',
            'required': 'Field 2 is required',
        })


def add_array_with_array_with_leafs(form):
    arr = form['arrayarray'] = factory(
        'array',
        value=[['1', '2'], ['3', '4'], ['5', '6']],
        props={
            'label': 'Array Array',
        })
    subarr = arr['somearray'] = factory(
        'array',
        props={
            'label': 'Some Array',
        })
    subarr['somefield'] = factory(
        'field:error:label:text',
        props={
            'label': 'Some Field',
            'required': 'Some Field is required',
        })


def add_array_with_array_with_compounds(form):
    arr = form['arrayarraycomp'] = factory(
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
            [
                {
                    'f1': 'Value 1.0 F1',
                    'f2': 'Value 1.0 F2',
                },
                {
                    'f1': 'Value 1.1 F1',
                    'f2': 'Value 1.1 F2',
                },
            ],
        ],
        props={'label': 'Array 1'})
    subarr = arr['subarray'] = factory(
        'array',
        props={
            'label': 'Array 2',
        })
    comp = subarr['comp'] = factory('compound')
    comp['f1'] = factory(
        'field:label:text',
        props={
            'label': 'F1',
        })
    comp['f2'] = factory(
        'field:error:label:text',
        props={
            'label': 'F2',
            'required': 'F2 is required',
        })


def add_array_with_array_with_array_with_leafs(form):
    arr_1 = form['array_1'] = factory(
        'array',
        value=[
            [
                ['1', '2'],
                ['3'],
            ],
            [
                ['4', '5'],
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


def add_array_with_array_with_array_with_compounds(form):
    arr_1 = form['comp_array_1'] = factory(
        'array',
        value=[
            [
                [
                    {
                        'f1': 'Value F1',
                        'f2': 'Value F2',
                    },
                ],
            ],
            [
                [
                    {
                        'f1': 'Value F1',
                        'f2': 'Value F2',
                    },
                ],
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
    comp = arr_3['comp'] = factory('compound')
    comp['f1'] = factory(
        'field:label:text',
        props={
            'label': 'F1',
        })
    comp['f2'] = factory(
        'field:error:label:text',
        props={
            'label': 'F2',
            'required': 'F2 is required',
        })


def get_example():
    root = factory('fieldset', name='yafowil.widget.array')
    add_array_with_leafs(root)
    add_array_with_compounds(root)
    add_array_with_array_with_leafs(root)
    add_array_with_array_with_compounds(root)
    add_array_with_array_with_array_with_leafs(root)
    add_array_with_array_with_array_with_compounds(root)
    return {'widget': root, 'routes': {}}