import Blockly from 'node-blockly/browser';
import blocks from './blocks';


export function initGlobalBlockly() {
  global.Blockly = Blockly;
  initBlocks(blocks);
}


function initBlocks(allBlocks) {
  allBlocks.forEach(block => {
    Blockly.Blocks[block.id] = {
      init: initBlock(block),
    };
  });
}


function initBlock(block) {
  return function init() {
    this.jsonInit(block);
  };
}


export function blocklyXmlToRoboAst(blocklyXml) {
  const blocklyDom = Blockly.Xml.textToDom(blocklyXml);
  const roboAst = blocklyDomToRoboAst(blocklyDom);
  return roboAst;
}


function blocklyDomToRoboAst(dom) {
  const startBlock = dom.querySelector('block[type="start"]');
  return blockToAst(startBlock);
}


function blockToAst(block) {
  if (block == null) {
    return null;
  }
  const type = block.getAttribute('type');
  switch (type) {
    case 'start':
      return startBlockToAst(block);
    case 'repeat':
      return repeatBlockToAst(block);
    case 'while':
      return whileBlockToAst(block);
    case 'if':
      return ifBlockToAst(block);
    case 'if-else':
      return ifElseBlockToAst(block);
    case 'fly':
      return flyBlockToAst(block);
    case 'shoot':
      return shootBlockToAst(block);
    case 'color':
      return colorBlockToAst(block);
    case 'position':
      return positionBlockToAst(block);
    default:
      throw new Error(`Unknown block type: ${type}`);
  }
}


function startBlockToAst(block) {
  const nextBlock = getNextBlock(block);
  const body = getSequence(nextBlock);
  return { head: 'start', body, location: getLocation(block) };
}


function repeatBlockToAst(block) {
  const count = parseInt(getFieldValue(block, 'count'), 10);
  const body = getBody(block);
  const astNode = { head: 'repeat', count, body };
  return astNode;
}


function whileBlockToAst(block) {
  const test = blockToAst(getValueBlock(block, 'test'));
  const body = getBody(block);
  const astNode = { head: 'while', test, body };
  return astNode;
}


function ifBlockToAst(block) {
  const test = blockToAst(getValueBlock(block, 'test'));
  const body = getBody(block);
  const astNode = { head: 'if', test, body };
  return astNode;
}


function ifElseBlockToAst(block) {
  const test = blockToAst(getValueBlock(block, 'test'));
  const body = getBody(block);
  const bodyElse = getBody(block, 'body-else');
  const orelse = {
    statement: { head: 'else', body: bodyElse },
    location: getLocation(block),
  };
  const astNode = { head: 'if', test, body, orelse };
  return astNode;
}


function flyBlockToAst(block) {
  const direction = getFieldValue(block, 'direction');
  const command = (direction === 'ahead') ? 'fly' : direction;
  const astNode = { head: command };
  return astNode;
}


// eslint-disable-next-line no-unused-vars
function shootBlockToAst(block) {
  const astNode = { head: 'shoot' };
  return astNode;
}


function colorBlockToAst(block) {
  const comparator = getFieldValue(block, 'comparator');
  const value = getFieldValue(block, 'value');
  return { head: 'color', comparator, value };
}


function positionBlockToAst(block) {
  const comparator = getFieldValue(block, 'comparator');
  const value = parseInt(getFieldValue(block, 'value'), 10);
  return { head: 'position', comparator, value };
}


function getBody(block, name = 'body') {
  const bodyNode = getStatement(block, name);
  if (bodyNode == null) {
    return [];
  }
  const firstBlock = bodyNode.childNodes[0];
  const body = getSequence(firstBlock);
  return body;
}


function getSequence(firstBlock) {
  const body = [];
  let next = firstBlock;
  while (next != null) {
    body.push(blockToAstWithLocation(next));
    next = getNextBlock(next);
  }
  return body;
}


function blockToAstWithLocation(block) {
  return { statement: blockToAst(block), location: getLocation(block) };
}


function getFieldValue(block, name) {
  const field = getField(block, name);
  const value = field.textContent;
  return value;
}


function getField(block, name) {
  const id = block.getAttribute('id');
  const field = block.querySelector(`block[id="${id}"] > field[name="${name}"]`);
  return field;
}


function getStatement(block, name) {
  const id = block.getAttribute('id');
  const statement = block.querySelector(`block[id="${id}"] > statement[name="${name}"]`);
  return statement;
}


function getValueBlock(block, name) {
  const id = block.getAttribute('id');
  const field = block.querySelector(`block[id="${id}"] > value[name="${name}"] > block`);
  return field;
}


function getNextBlock(block) {
  const id = block.getAttribute('id');
  const nextBlock = block.querySelector(`block[id="${id}"] > next > block`);
  return nextBlock;
}


function getLocation(block) {
  return { blockId: block.getAttribute('id') };
}
