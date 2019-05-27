#!/usr/bin/env python3
''' A pandoc filter that has the LaTeX writer use minted for typesetting code.

Author: Gabriel Pelouze
Changed: 2016-04-14 11:39:18 (CEST)

Usage:
    pandoc --filter ./minted.py -o myfile.tex myfile.md

'''

from pandocfilters import toJSONFilter, RawBlock, RawInline

def unpack_code(c, meta):
    ''' Unpack the body and language of a pandoc code element.
    Args:
        value   contents of pandoc object
        meta    document metadata
    '''
    [attrib, body] = c
    try:
        [_, [language, *_], _] = attrib
    except ValueError:
        # Use default language, or don't highlight.
        language = meta.get('minted-language')
        if language is not None:
            language = language['c'][0]['c']

    return body, language

def latex(s):
    return RawInline('latex', s)

def pd_filter(t, c, to_format, meta):
    ''' Use minted for code in LaTeX.
    Args:
        t           type of pandoc object
        c           contents of pandoc object
        to_format   target output format
        meta        document metadata
    '''
    if to_format == 'latex':
        if t == 'CodeBlock':
            body, language = unpack_code(c, meta)
            if language is None:
                return

            begin = r'\begin{minted}{' + language + '}\n'
            end = '\n' + r'\end{minted}'

            return [RawBlock(to_format, begin + body + end)]

        elif t == 'Code':
            body, language = unpack_code(c, meta)
            if language is None:
                return
            
            begin = r'\mintinline{' + language + '}{'
            end = '}'

            return [latex(begin + body + end)]
        elif t == 'Strong': # **text**
            begin = r'\strong{'
            body = c[0]['c']
            end = r'}'
            return [latex(begin)] + c + [latex(end)]
        # elif t == 'Emph': # *text*
            # begin = r'\emph{'
            # body = c 
            # end = r'}'
            # return [Str(to_format, begin + body + end)]
        elif t == 'Math':
            math_type = c[0]['t']
            content = c[1]
            if math_type == 'InlineMath':
                begin = r'$'
                end = r'$'
                return [latex(begin + content + end)]
            if math_type == 'DisplayMath':
                begin = r'\begin{equation}'
                end = r'\end{equation}'
                return [latex(begin + content + end)]

if __name__ == '__main__':
    toJSONFilter(pd_filter)
