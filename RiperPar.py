#To compile
#python RiperLex.py 
#python RiperPar.py test.riper

import ply.yacc as yacc
import sys
import RiperLex
import SemanticCube

# import the lexical tokens
tokens = RiperLex.tokens

# Global function and variable directory
global globalDirectory
globalDirectory = {}

# Local variable directory
global localDirectory
localDirectory = {}

#Counter of expressions in arrays
global expCount
expCount = 0;


global correctProgram
correctProgram = True

global operandStack
operandStack = []
global operatorStack
operatorStack = []

global cuadruples
cuadruples = []


# Global Riper code structure
def p_program(p):
    '''program : globalVarDeclar functionDeclar main'''
    p[0] = 'OK'  


# Global variable declaration section
def p_globalVarDeclar(p):
    '''globalVarDeclar : initVarDeclar '''
    if (len(p) > 1):
        global localDirectory
        global globalDirectory
        if (len(localDirectory) > 0):
            globalDirectory = localDirectory.copy()
            localDirectory = {}


# Variable initialization section
def p_initVarDeclar(p):
    '''initVarDeclar : varDeclar initVarDeclar
                     | '''


# Function declaration section                   
def p_functionDeclar(p):
    '''functionDeclar : function functionDeclar
                      | '''

# Variable or array declaration statute
def p_varDeclar(p):
    '''varDeclar : vars ';'
                 | ARRAY arrays ';' '''
  

# Variable declaration statue
def p_vars(p):
    '''vars : type ID '=' expression moreVar'''
    if (len(p) > 1):
        global localDirectory
        if (p[2] in localDirectory or p[2] in globalDirectory):
            print "ERROR, variable ", p[2], " has already been declared"
            global correctProgram
            correctProgram = False
        else:
            localDirectory[p[2]] = [currentType]
            #NEED TO CHECK IF TYPE AND THE VALUE ARE EQUAL FOR ASSIGN


# Grammar rule used when more than one variable is declared
def p_moreVar(p):
    '''moreVar : ',' ID '=' expression moreVar
               | '''
    if (len(p) > 1):
        global localDirectory
        if (p[2] in localDirectory or p[2] in globalDirectory):
            print "ERROR, variable ", p[2], " has already been declared"
            global correctProgram
            correctProgram = False
        else:
            localDirectory[p[2]] = [currentType]
            #NEED TO CHECK IF TYPE AND THE VALUE ARE EQUAL FOR ASSIGN
  

# Grammar rulle used to match to one of the basic variable type declaration tokens
def p_type(p):
    '''type : INTTYPE
            | FLOATTYPE
            | STRINGTYPE
            | BOOLTYPE '''
    if (len(p) > 1):
        global currentType
        currentType = p[1]

# 
def p_arrays(p):
    '''arrays : array moreArray '''

def p_array(p):
    '''array : type ID '[' INT ']' '=' '{' expression sumExpCount moreExp '}' '''
    if (len(p) > 1):
        global expCount
        if (int(p[4][1]) != expCount):
            print "ERROR, the size of array ", p[2], " is different from the amount of contents declared"
            global correctProgram
            correctProgram = False
        expCount = 0;

def p_moreExp(p):
    '''moreExp : ',' expression sumExpCount moreExp
        | '''

def p_sumExpCount(p):
    '''sumExpCount : '''
    global expCount
    expCount += 1

  

def p_moreArray(p):
    '''moreArray : nextArray moreArray
        | '''

def p_nextArray(p):
    '''nextArray :  ',' ID '[' INT ']' '=' '{' expression sumExpCount moreExp '}' '''
    global expCount
    if (int(p[4][1]) != expCount):
        print "ERROR, the size of array ", p[2], " is different from the amount of contents declared"
        global correctProgram
        correctProgram = False
    expCount = 0;
  

def p_function(p):
  '''function : FUNCTION funcType ID '(' par ')' '{' block RETURN returnType ';' '}' '''
  if (len(p) > 1):
    global localDirectory
    global currentFuncType
    globalDirectory[p[3]] = [currentFuncType]
    localDirectory = {}
  

def p_funcType(p):
    '''funcType : INTTYPE
        | FLOATTYPE
        | STRINGTYPE
        | BOOLTYPE
        | VOID '''
    if (len(p) > 1):
        global currentFuncType
        currentFuncType = p[1]
  

def p_returnType(p):
    '''returnType : expression
        | VOID '''
  

def p_main(p):
    '''main : MAIN '(' par ')' '{' block '}' '''
    if (len(p) > 1):
        global localDirectory
        if (len(localDirectory) > 0):
            globalDirectory['main'] = localDirectory
            localDirectory = {}
  

def p_par(p):
    '''par : type ID morePar
        | '''
    if (len(p) > 1):
        global localDirectory
        localDirectory[p[2]] = [currentType]
  

def p_morePar(p):
    '''morePar : ',' type ID morePar
        | '''
    if (len(p) > 1):
        global localDirectory
        localDirectory[p[2]] = [currentType]
  

def p_funcCall(p):
    '''funcCall : ID '(' parIn ')' '''
  

def p_parIn(p):
    '''parIn : expression moreParIn
        | '''
  

def p_moreParIn(p):
    '''moreParIn : ',' expression moreParIn 
        | '''
  

def p_block(p):
    '''block : varDeclar block
        | assign ';' block
        | conditional block
        | loop block
        | funcCall ';' block
        | output block
        | input block
        | '''
  

def p_loopBlock(p):
    '''loopBlock : assign ';' loopBlock
        | conditional loopBlock
        | loop loopBlock
        | funcCall ';' loopBlock
        | output loopBlock
        | input loopBlock
        | '''
  

def p_assign(p):
    '''assign : ID possibleArray '=' expression '''
    if (len(p) > 1):
        global localDirectory
        global globalDirectory
        if (p[1] not in localDirectory):
            if (p[1] not in globalDirectory):
                print "ERROR, variable ", p[1], " has not been declared"
                global correctProgram
                correctProgram = False

def p_possibleArray(p):
    '''possibleArray : '[' exp ']'
        | '''
  

def p_conditional(p):
    '''conditional : IF '(' expression ')' '{' block '}' possibleElif possibleElse '''
  

def p_possibleElif(p):
    '''possibleElif : ELIF '(' expression ')' '{' block '}' possibleElif
        | '''
  

def p_possibleElse(p):
    '''possibleElse : ELSE '{' block '}' 
        | '''
  

def p_output(p):
    '''output : CONSOLE '(' expression ')' ';' '''
  

def p_loop(p):
    '''loop : for
        | while
        | doWhile '''
  

def p_for(p):
    '''for : FOR '('  expression ';' assign ')' '{' loopBlock '}' '''
  

def p_while(p):
    '''while : WHILE '(' expression ')' '{' loopBlock '}' '''
  

def p_doWhile(p):
    '''doWhile : DO '{' loopBlock '}' WHILE '(' expression ')' ';' '''
  

def p_expression(p):
    '''expression : higherExp1 possibleHigherExp1'''
  

def p_possibleHigherExp1(p):
    '''possibleHigherExp1 : OR higherExp1 possibleHigherExp1
        | '''
  



def p_higherExp1(p):
    '''higherExp1 : higherExp2 possibleHigherExp2'''



def p_possibleHigherExp2(p):
    '''possibleHigherExp2 : AND higherExp2 possibleHigherExp2
        | '''


def p_higherExp2(p):
    '''higherExp2 : exp possibleExp'''


def p_possibleExp(p):
    '''possibleExp : possibleExpOp exp
        | '''
  

def p_possibleExpOp(p):
    '''possibleExpOp : LESS
        | GREATER
        | LESSEQUAL
        | GREATEREQUAL
        | DIFFERENT
        | EQUALTO '''

  
def p_exp(p):
    '''exp : possibleSign term possibleTerms'''
    if (len(operatorStack) > 0 and operatorStack[-1] in ['<', '>', '<=', '>=', '!=', '==']):
        print "TOP " + operatorStack[-1] + ", GENERATING"
        GenerateCuadruple()
  

def p_possibleTerms(p):
    '''possibleTerms : possibleTermOp possibleSign term possibleTerms
        | '''

def p_possibleSign(p):
    '''possibleSign : '+'
        | '-' 
        | '''   

def p_possibleTermOp(p):
    '''possibleTermOp : '+'
        | '-' '''
    print "PUSHING +-"
    operatorStack.append(p[1])


def p_term(p):
    '''term : factor possibleFactors'''
    if (len(operatorStack) > 0 and operatorStack[-1] in ['+', '-']):
        print "TOP +-, GENERATING"
        GenerateCuadruple()
  

def p_possibleFactors(p):
    '''possibleFactors : possibleFactorOp factor possibleFactors
        | '''
    if (len(p) == 1):
        p[0] = ''

def p_possibleFactorOp(p):
    '''possibleFactorOp : '*'
        | '/'
        | '%' '''
    p[0] = p[1]
    print "PUSHHING */"
    operatorStack.append(p[1])   

  
  

def p_factor(p):
    '''factor : lPar expression rPar
        | data'''
    if (len(p) == 2):
        p[0] = p[1]
        if (len(operatorStack) > 0 and operatorStack[-1] in ['*', '/', '%']):
            print "TOP */, GENERATING"
            GenerateCuadruple()


def p_lPar(p):
    '''lPar : '(' '''
    print "PUSH ("
    operatorStack.append(p[1])

def p_rPar(p):
    '''rPar : ')' '''
    print operatorStack.pop()

  

def p_data(p):
    '''data : ID possibleIdCall
        | constant
        | input '''
    if (len(p) == 3):
        global localDirectory
        global globalDirectory
        if (p[1] not in localDirectory):
            if (p[1] not in globalDirectory):
                print "ERROR, variable ", p[1], " has not been declared"
                global correctProgram
                correctProgram = False
    p[0] = p[1]
    print "PUSHING TO OPERAND"
    operandStack.append(p[1])


def p_possibleIdCall(p):
    '''possibleIdCall : '[' expression ']'
        | '(' parIn ')'
        | '''
    if(len(p) == 4):
        p[0] = p[2]
    else:
        p[0] = ''

def p_constant(p):
    '''constant : INT
        | FLOAT
        | TRUE
        | FALSE
        | STRING'''
    p[0] = p[1]


def p_input(p):
    '''input : INPUT '(' inputPar ')' '''  
    p[0] = ('INPUT', p[3])

def p_inputPar(p):
    '''inputPar : STRING 
        |  '''
    if(len(p) > 1):    
        p[0] = p[1]
    else:
        p[0] = ''

def p_error(p):
    print('Syntax error in line %d token %s with value %s' % (p.lineno, p.type, p.value))


def GenerateCuadruple():
    op = operatorStack.pop()
    operand2 = operandStack.pop()
    operand1 = operandStack.pop()
    result = SemanticCube.SearchSemantic(operand1, op, operand2)
    if (result != -1):
        cuadruples.append([op, operand1, operand2, (result, '')])
        operandStack.append((result, '')) #Second position would be the temporal name?
    else:
        print "ERROR, type mismatch"


  # Build the parser
RiperParser = yacc.yacc()
if __name__ == '__main__':
    if (len(sys.argv) > 1):
        file = sys.argv[1]
        try:
            f = open(file,'r')
            data = f.read()
            f.close()
            if (RiperParser.parse(data, debug = False, tracking=True)):
                if(correctProgram):
                    print ('This is a correct and complete Riper program');
                    print globalDirectory
                    print cuadruples
        except EOFError:
            print(EOFError)
    else:
        print('File missing')