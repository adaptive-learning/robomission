import pegRoboCodeParser from './pegRoboCodeParser';

export function parseRoboCode(code) {
  const normalizedCode = preprocess(code);
  try {
    const roboAst = pegRoboCodeParser.parse(normalizedCode);
    return roboAst;
  } catch (error) {
    if (error instanceof pegRoboCodeParser.SyntaxError) {
      const { message, location, expected, found } = error;
      const { line, column } = getOriginalLocation(location.start, normalizedCode);
      let problem = message;
      let position = `line ${line}, column ${column}`;
      if (expected.some(exp => exp.text === '>' || exp.text === '<')
         || (found === '>' || found === '<')) {
        problem = 'Bad indentation';
        position = `line ${line}`;
      }
      const report = `Syntax Error: ${problem} (${position})`;
      throw new RoboCodeSyntaxError(report);
    } else {
      throw error;
    }
  }
}


export function RoboCodeSyntaxError(message) {
  this.name = 'RoboCodeSyntaxError';
  this.message = message;
}


function preprocess(code) {
  const lines = removeEmpty(toNumberedIndentedLines(code));
  const linesAndIndents = addIndentationTokens(lines);
  const normalizedLines = linesAndIndents.map(line => {
    switch (line) {
      case 'INDENT':
        return '>';
      case 'DEDENT':
        return '<';
      default:
        return `${line.number}| ${line.text}`;
    }
  });
  const normalizedCode = normalizedLines.join('\n');
  return normalizedCode;
}

function addIndentationTokens(lines) {
  const levels = [0];
  const linesAndIndents = [];
  for (const line of lines) {
    if (line.indentation > levels[levels.length - 1]) {
      linesAndIndents.push('INDENT');
      levels.push(line.indentation);
    }
    while (line.indentation < levels[levels.length - 1]) {
      linesAndIndents.push('DEDENT');
      levels.pop();
    }
    linesAndIndents.push(line);
  }
  while (levels.length > 1) {
    linesAndIndents.push('DEDENT');
    levels.pop();
  }
  return linesAndIndents;
}

function toNumberedIndentedLines(code) {
  const lines = code.split(/\n/);
  const numberedIndentedLines = lines.map((line, index) => {
    const number = index + 1;
    const indentation = line.search(/\S|$/);
    const text = line.trim();
    return { number, indentation, text };
  });
  return numberedIndentedLines;
}


function removeEmpty(numberedIndentedLines) {
  return numberedIndentedLines.filter(line => line.text.length > 0);
}


function getOriginalLocation({ line, column }, normalizedCode) {
  const lines = normalizedCode.split('\n');
  const insertedLines = lines.slice(0, line).filter(l => l === '>' || l === '<');
  let insertedCount = insertedLines.length;
  if (lines[line - 1] === '>') {
    insertedCount -= 1;
  }
  const linePrefix = lines[line - 1].indexOf('|') + 1;
  const originalLocation = {
    line: line - insertedCount,
    column: column - linePrefix,
  };
  return originalLocation;
}

export default parseRoboCode;
