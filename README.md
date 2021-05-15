![alt text](https://github.com/gabrielacorona/compilador-concha/blob/main/misc/Logo.jpeg)
# Compilador Concha
'Concha' language is a high-level programming language that can be used for object oriented programming. The main characteristic of this language is that the syntax expressions are in spanish so that any spanish speaker can understand and learn the language.

## Main Objective
Democratize the process of learning a programming language by removing the language barrier as most popular programming languages use english words for their syntax.

## Primer avance
In this first revision we implemented the Lexical/Syntactical analysis of our language, introducing the Tokens and Grammar used to parse the syntax of any program written in Concha in the file 'concha.py' . Additionally, the railroad diagrams are attached in this repository that display graphically the BNF grammar we designed for our programming language.

## Segundo avance
In this second revision we implemented the function directory as well as the symbol table used to identify variables written in the language. We used Transformer interface from Lark library to generate an AST from the syntax that will be compiled.

## Tercer avance
In this third revision we changed the library we were using from Lark to rPLY so that we would be able to follow with the course materials. We translated everything we previously had in our previous files so that they would work with rPLY, it was hard work but we believe it's a good step forward for next revisions.

## Cuarto avance
In this revision we started preparations for jumps when the conditions of loops or conditionals were met. We finished the generation of quadruples to evaluate whether the conditions are met but we are still missing the jumps.

## Quinto avance
For this revision we chaged the way we were doing things since it wasn't the most optimal way to do it. We refactored most of the code for generating quadruples so that the compiler could generate jumps referencing the memory stack. We finished the implementations for writing, reading, assigning, cycles, conditions and functions.

## Example of program written in Concha
```python

vacio funcion hola(entero k)!
vacio funcion holaqueonda(entero k,entero j)!

programa miPrimerPrograma
{    
     entero a;
     entero b = 2;
     entero c = a;
     entero d = a + 2 + 1 + (3 / 4 * 3);
     escribir("Hola mundo!");
};

vacio funcion hola(entero k){
     entero l;
     entero a = 1;
     entero b = 2;
     flotante h = 9 + 8 - 1;
};

vacio funcion holaqueonda(entero k,entero j){
     entero l;
     entero a = 1;
     entero b = 2;
     flotante h = 9 + 8 - 1;
};