from unquote_resolvers import unquote_resolvers


def test_single_resolver():
    input_data = {'key': '!stack_output mystack::subnet_a'}
    expected_output = "key: !stack_output mystack::subnet_a\n"
    assert unquote_resolvers(input_data) == expected_output


def test_list_of_resolvers():
    input_data = {
        'Subnets': [
            '!stack_output_external mystack::subnet_a',
            '!stack_output_external mystack::subnet_b'
        ]
    }
    expected_output = (
        "Subnets:\n"
        "- !stack_output_external mystack::subnet_a\n"
        "- !stack_output_external mystack::subnet_b\n"
    )
    assert unquote_resolvers(input_data) == expected_output


def test_nested_resolvers():
    input_data = {
        'Resources': {
            'Subnets': [
                '!stack_output_external mystack::subnet_a',
                '!stack_output_external mystack::subnet_b'
            ],
            'VPC': '!stack_output_external mystack::vpc_id'
        }
    }
    expected_output = (
        "Resources:\n"
        "  Subnets:\n"
        "  - !stack_output_external mystack::subnet_a\n"
        "  - !stack_output_external mystack::subnet_b\n"
        "  VPC: !stack_output_external mystack::vpc_id\n"
    )
    assert unquote_resolvers(input_data) == expected_output


def test_mixed_data():
    input_data = {
        'Resources': {
            'Subnets': [
                '!stack_output_external mystack::subnet_a',
                'non-resolver-value'
            ],
            'VPC': '!stack_output_external mystack::vpc_id',
            'Tags': {
                'Environment': 'production'
            }
        }
    }
    expected_output = (
        "Resources:\n"
        "  Subnets:\n"
        "  - !stack_output_external mystack::subnet_a\n"
        "  - non-resolver-value\n"
        "  Tags:\n"
        "    Environment: production\n"
        "  VPC: !stack_output_external mystack::vpc_id\n"
    )
    assert unquote_resolvers(input_data) == expected_output
