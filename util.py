import tokenize
import token
from StringIO import StringIO
import colorsys


def fixLazyJson(in_text):
    tokengen = tokenize.generate_tokens(StringIO(in_text).readline)
    result = []

    for tokid, tokval, _, _, _ in tokengen:
        # fix unquoted strings
        if (tokid == token.NAME):
            if tokval not in ['true', 'false', 'null', '-Infinity', 'Infinity', 'NaN']:
                tokid = token.STRING
                tokval = u'"%s"' % tokval

        # fix single-quoted strings
        elif (tokid == token.STRING):
            if tokval.startswith("'"):
                tokval = u'"%s"' % tokval[1:-1].replace('"', '\\"')

        # remove invalid commas
        elif (tokid == token.OP) and ((tokval == '}') or (tokval == ']')):
            if (len(result) > 0) and (result[-1][1] == ','):
                result.pop()

        # fix single-quoted strings
        elif (tokid == token.STRING):
            if tokval.startswith("'"):
                tokval = u'"%s"' % tokval[1:-1].replace('"', '\\"')

        result.append((tokid, tokval))

    return tokenize.untokenize(result)


def get_hsv(hexrgb):
    hexrgb = hexrgb.lstrip("#")   # in case you have Web color specs
    r, g, b = (int(hexrgb[i:i+2], 16) / 255.0 for i in xrange(0, 5, 2))
    return colorsys.rgb_to_hsv(r, g, b)


def get_rgb(hexrgb):
    hexrgb = hexrgb.lstrip("#")   # in case you have Web color specs
    split = (hexrgb[0:2], hexrgb[2:4], hexrgb[4:6])
    return [int(x, 16) for x in split]
