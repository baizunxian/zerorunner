const colType = {Object, Array}

export function getJsonPath(text: string, offSet: number) {
  let pos: number = 0
  let stack: Array<Object> = []
  let isInKey: boolean = false

  while (pos < offSet) {
    const startPos = pos
    switch (text[pos]) {
      case '"':
        const {text: s, pos: newPos} = readString(text, pos)
        if (stack.length) {
          const frame: any = stack[stack.length - 1]
          if (frame.colType === colType.Object && isInKey) {
            frame.key = s
            isInKey = false
          }
        }
        pos = newPos
        break
      case '{':
        stack.push({colType: colType.Object})
        isInKey = true
        break
      case '[':
        stack.push({colType: colType.Array, index: 0})
        break
      case '}':
      case ']':
        stack.pop()
        break
      case ',':
        if (stack.length) {
          const frame: any = stack[stack.length - 1]
          if (frame.colType === colType.Object) {
            isInKey = true
          } else {
            frame.index++
          }
        }
        break
    }
    if (pos === startPos) {
      pos++
    }
  }
  return pathToString(stack);
}

function pathToString(path: any) {
  let s = '$'
  try {
    for (const frame of path) {
      if (frame.colType === colType.Object) {
        if (!frame.key.match(/^[a-zA-Z$_][a-zA-Z\d$_]*$/)) {
          const key = frame.key.replace('"', '\\"')
          s += `["${frame.key}"]`
        } else {
          if (s.length) {
            s += '.'
          }
          s += frame.key
        }
      } else {
        s += `[${frame.index}]`
      }
    }
    return s;
  } catch (ex) {
    return '';
  }
}

function isEven(n: number) {
  return n % 2 === 0;
}

function readString(text: string, pos: number) {
  let i = pos + 1
  i = findEndQuote(text, i)
  return {
    text: text.substring(pos + 1, i),
    pos: i + 1
  }
}

// Find the next end quote
function findEndQuote(text: string, i: number) {
  while (i < text.length) {
    // console.log('findEndQuote: ' + i + ' : ' + text[i])
    if (text[i] === '"') {
      var bt = i
      // Handle backtracking to find if this quote is escaped (or, if the escape is escaping a slash)
      while (0 <= bt && text[bt] == '\\') {
        bt--
      }
      if (isEven(i - bt)) {
        break;
      }
    }
    i++
  }
  return i
}