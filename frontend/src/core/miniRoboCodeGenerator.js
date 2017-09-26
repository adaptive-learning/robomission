export function generateMiniRoboCode(roboAst) {
  const { head, body } = roboAst;
  if (head !== 'start') {
    throw new Error(`Unexpected root of roboAst: ${head}`);
  }
  const roboCode = (body.length > 0) ? generateBody(body) : '';
  return roboCode;
}


function generateBody(nodes) {
  const nodesCode = nodes.map(generateStatement);
  const bodyCode = nodesCode.join('');
  return bodyCode;
}


function generateStatement({ statement }) {
  switch (statement.head) {
    case 'repeat':
      return generateRepeatLoop(statement);
    case 'while':
      return generateWhileLoop(statement);
    case 'if':
      return generateIfStatement(statement);
    default:
      return generateSimpleStatement(statement);
  }
}

function generateSimpleStatement({ head }) {
  switch (head) {
    case 'fly':
      return 'f';
    case 'left':
      return 'l';
    case 'right':
      return 'r';
    case 'shoot':
      return 's';
    default:
      throw new Error(`Unknown statement: ${head}`);
  }
}


function generateRepeatLoop({ count, body }) {
  const bodyCode = generateBody(body);
  const code = `R${count}{${bodyCode}}`;
  return code;
}


function generateWhileLoop({ test, body }) {
  const testCode = generateTest(test);
  const bodyCode = generateBody(body);
  const code = `W${testCode}{${bodyCode}}`;
  return code;
}


function generateIfStatement({ test, body, orelse }) {
  const testCode = generateTest(test);
  const bodyCode = generateBody(body);
  const orelseCode = orelse ? generateOrelseBlock(orelse) : '';
  const code = `I${testCode}{${bodyCode}}${orelseCode}`;
  return code;
}


function generateOrelseBlock({ statement }) {
  switch (statement.head) {
    case 'elif':
      return generateElif(statement);
    case 'else':
      return generateElse(statement);
    default:
      throw new Error(`Unexpected orelse head: ${statement.head}`);
  }
}


function generateElif({ test, body, orelse }) {
  const testCode = generateTest(test);
  const bodyCode = generateBody(body);
  const orelseCode = orelse ? generateOrelseBlock(orelse) : '';
  const code = `/${testCode}{${bodyCode}}${orelseCode}`;
  return code;
}


function generateElse({ body }) {
  const bodyCode = generateBody(body);
  const code = `/{${bodyCode}}`;
  return code;
}


function generateTest(node) {
  if (node == null) {
    return '';
  }
  switch (node.head) {
    case 'and':
      return generateCompoundTest('a', node.left, node.right);
    case 'or':
      return generateCompoundTest('o', node.left, node.right);
    default:
      return generateSimpleTest(node);
  }
}


function generateCompoundTest(operator, leftTestNode, rightTestNode) {
  const leftTest = generateSimpleTest(leftTestNode);
  const rightTest = generateSimpleTest(rightTestNode);
  return `(${leftTest}${operator}${rightTest})`;
}


function generateSimpleTest({ head, comparator, value }) {
  switch (head) {
    case 'color':
      return (comparator === '==') ? value : `!${value}`;
    case 'position':
      return `x${generateComparator(comparator)}${value}`;
    default:
      throw new Error(`Unknown test head: ${head}`);
  }
}


function generateComparator(value) {
  switch (value) {
    case '==':
      return '=';
    case '!=':
      return '!=';
    default:
      return value;
  }
}
