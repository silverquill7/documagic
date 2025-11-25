from behave import given, when, then

@given('a user exists with email "{email}" and password "{password}"')
def step_impl(context, email, password):
    context.email = email
    context.password = password

@when("the user logs in with correct credentials")
def step_impl(context):
    context.response = context.client.post("/login", data={
        "email": context.email,
        "password": context.password
    })

@then("the system should log the user in successfully")
def step_impl(context):
    assert context.response.status_code == 200
