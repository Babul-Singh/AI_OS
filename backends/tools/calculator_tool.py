def calculator(expression):

    try:
        result = eval(expression)

        return result

    except Exception as e:
        return str(e)