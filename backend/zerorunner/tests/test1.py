# -*- coding: utf-8 -*-
# @project: zerorunner
# @author: xiaobai
# @create time: 2022/9/9 14:53
import re

function_regex_compile = re.compile(r"\$\{([a-zA-Z_]\w*)\(([\$\w\.\-/\s\[\]{}=,]*)\)\}")
function_regexp_compile = re.compile(r'^([\w_]+)\(([\$\w\.\-_ =,{}:""\[\]\u4e00-\u9fa5]*)\)$')

c = '${test(${test},b)}'

print(function_regex_compile.match(c))
print(function_regex_compile.match(c).group(1))
print(function_regex_compile.match(c).group(2))
# print(function_regex_compile.match(c).group(2))
# print(function_regexp_compile.match(c).group(1))
# print(function_regexp_compile.match(c).group(2))


