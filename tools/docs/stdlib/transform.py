import re


def normalize(text):
    if text is not None:
        return text.strip()

    return None


def normalize_type(text):
    text = normalize(text)

    if text is None:
        text = ""

    if text.startswith('{'):
        text = text[1:]

    if text.endswith('}'):
        text = text[:-1]

    return text


def process_name(text):
    if text is None:
        return None, False, None

    is_optional = text.startswith('[')
    default_value = None

    if not is_optional:
        return text, False, None

    regex = re.compile(
        '\[(?P<name>[A-Za-z]+)(?P<eq>=)?(?P<value>.+)?\]',
    )

    match = regex.search(text)
    name = normalize(match.group('name'))

    try:
        default_value = normalize(match.group('value'))
    except:
        pass

    return name, is_optional, normalize(default_value)


def preprocess_line(target):
    target = target.replace('@params', '@param')
    target = target.replace('@returns', '@return')

    return target


def parse(regex, target):
    match = regex.search(target)

    if match is None:
        print("Failed to match string: " + target)
        return None, None, None

    arg_name = None
    arg_type = normalize(match.group('type'))
    arg_desc = normalize(match.group('desc'))

    try:
        arg_name = normalize(match.group('name'))
    except:
        pass

    arg_type = normalize_type(
        arg_type,
    )

    arg_types = list(map(
        str.strip,
        filter(None, arg_type.split('|')),
    ))

    arg_desc = arg_desc.capitalize()

    return arg_name, arg_types, arg_desc


def process_returns(returns):
    if returns is None:
        return None

    regex = re.compile(
        '@return\s*(?P<type>{.+})\s*-\s*(?P<desc>.+)',
    )

    arg_name, arg_types, arg_desc = parse(
        regex,
        returns,
    )

    if arg_desc is None:
        return None

    return {
        'name': arg_name,
        'type': arg_types,
        'desc': arg_desc,
    }


def process_params(params):
    regex = re.compile(
        '@param\s*(?P<type>{.+})\s*(?P<name>.+)?\s*-\s*(?P<desc>.+)',
    )

    for num, param in enumerate(params, start=1):
        arg_name, arg_types, arg_desc = parse(
            regex,
            param,
        )

        arg_optional = False
        arg_default_value = None

        if arg_name is not None:
            arg_name, arg_optional, arg_default_value = process_name(arg_name)
        else:
            print(param)
            arg_name = "param" + str(num)

        if arg_types is not None:
            yield {
                'name': arg_name,
                'type': arg_types,
                'desc': arg_desc,
                'optional': arg_optional,
                'default_value': arg_default_value
            }


def transform_extract(extract):
    content, params, returns = [], [], None

    for line in extract.content:
        line = preprocess_line(line.strip())

        if line.startswith('@param'):
            params.append(line)
            continue

        if line.startswith('@return'):
            returns = line
            continue

        if returns is not None:
            returns = f'{returns} {line}'
            continue

        if len(params) > 0:
            params[-1] = f'{params[-1]} {line}'
            continue

        if len(params) == 0:
            content.append(line)
            continue

    content = ' '.join(content)
    returns = process_returns(returns)
    params = list(process_params(params))

    return {
        'desc': content,
        'params': params,
        'returns': returns,
    }
