from pytest import raises
from jinja_unquote_resolvers_filter.unquote_resolvers import unquote_resolvers


def assert_output_matches(expected_output, actual_output):
    """
    Depending on versions of libraries loaded, the yaml
    dumper may add single quotes and emit:
     !stack_output_external 'mystack::subnet_a'
    instead of:
     !stack_output_external mystack::subnet_a
    To avoid complexity in these tests, we simply
    delete single quotes here.
    """
    assert expected_output == actual_output.replace("'", "")


def test_single_resolver():
    input_data = {"key": "!stack_output mystack::subnet_a"}
    expected_output = "key: !stack_output mystack::subnet_a\n"
    actual_output = unquote_resolvers(input_data)
    assert_output_matches(expected_output, actual_output)


def test_list_of_resolvers():
    input_data = {
        "Subnets": [
            "!stack_output_external mystack::subnet_a",
            "!stack_output_external mystack::subnet_b",
        ]
    }
    expected_output = (
        "Subnets:\n"
        "- !stack_output_external mystack::subnet_a\n"
        "- !stack_output_external mystack::subnet_b\n"
    )
    actual_output = unquote_resolvers(input_data)
    assert_output_matches(expected_output, actual_output)


def test_nested_resolvers():
    input_data = {
        "Resources": {
            "Subnets": [
                "!stack_output_external mystack::subnet_a",
                "!stack_output_external mystack::subnet_b",
            ],
            "VPC": "!stack_output_external mystack::vpc_id",
        }
    }
    expected_output = (
        "Resources:\n"
        "  Subnets:\n"
        "  - !stack_output_external mystack::subnet_a\n"
        "  - !stack_output_external mystack::subnet_b\n"
        "  VPC: !stack_output_external mystack::vpc_id\n"
    )
    actual_output = unquote_resolvers(input_data)
    assert_output_matches(expected_output, actual_output)


def test_mixed_data():
    input_data = {
        "Resources": {
            "Subnets": [
                "!stack_output_external mystack::subnet_a",
                "non-resolver-value",
            ],
            "VPC": "!stack_output_external mystack::vpc_id",
            "Tags": {"Environment": "production"},
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
    actual_output = unquote_resolvers(input_data)
    assert_output_matches(expected_output, actual_output)


def test_multiline_in_one_line_resolver():
    input_data = {
        "my_multiline_resolver": "!from_json [!request http://www.whatever.com]"
    }
    expected_output = (
        "my_multiline_resolver: !from_json [!request http://www.whatever.com]\n"
    )
    actual_output = unquote_resolvers(input_data)
    assert_output_matches(expected_output, actual_output)


def test_multiline_raises():
    input_data = {
        "my_multiline_resolver": "!from_json\n  - !request http://www.whatever.com\n"
    }
    with raises(NotImplementedError, match="Multiline expressions not supported"):
        unquote_resolvers(input_data)
