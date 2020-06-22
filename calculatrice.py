import numpy as np

#On utilise ici une classe Expression qui va nous permette de mettre en forme nos expressions afin de les manipuler plus facilement

class Expression:

  def __init__(self , input):
    """Notre constructeur crée nos attributs et les initialise:
    Nous aurons besoin de notre expression qui sera donnée en entrée.
    Nous définissons une liste d'opérateurs mathématiques"""
    self.equation = input
    self.eq = input
    self.operateur = ["+","-","*","/","^","(",")","^","r"]

  def __repr__(self):
    """On affiche l'équation de notre expression"""
    return "Equation : {}".format(self.equation)

  def affiche(self):
    """On definit une fonction affiche a titre d'exemple de polymorphisme"""
    return("Equation : {}".format(self.equation))

  def __add__(self, objet_a_ajouter):
        """Surcharge de l'opérateur + : On additione 2 expressions"""
        nouvelle_expression = Expression(self.equation)
        nouvelle_expression.equation = self.equation
        nouvelle_expression.equation = "(" + nouvelle_expression.equation + ")" + "+" + "(" +objet_a_ajouter.equation + ")"
        return(nouvelle_expression)

  def sup_espace(self):
     """On supprime les espaces de notre expression et on arrange notre expression"""
     expression = self.equation
     expression = expression.replace(" ","")
     expression = expression.replace("sqrt","r")
     for j in self.operateur:
       expression = expression.replace(j, " "+j+" ")
     expression = expression.replace("  "," ")
     return(expression)

  def convert_float(self,expression):
     """On convertit notre expression en liste de float et d'opérateurs"""
     expr = expression.split()
     #On convertit les nombre en float
     nouveau = []
     for j in expr:
       if j in self.operateur:
         nouveau.append(j)
       else:
          nouveau.append(float(j))
     return(nouveau)
     #On modifie les parenthèse en liste

  def parenthese(self,expression):
    """on supprime les parenthese. les expressions entre parenthese seront des liste imbriqué dans notre liste"""
     nouveau = expression
     for h in nouveau:
       if ( h=='(' ):
         idx1 = nouveau.index('(')
         idx2 = nouveau.index(')')
         ss_list = nouveau[idx1+1:idx2]
         del nouveau[idx1:idx2+1]
         if len(nouveau)>idx1-1:
          nouveau.insert(idx1,ss_list)
         else:
          nouveau.insert(idx1,ss_list)
     return(nouveau)

  def modification(self):
    """On applique toutes les modifications dans cette méthodes"""
    expression = self.equation
    expression = self.sup_espace()
    self.eq = expression
    expression = self.convert_float(expression)
    expression = self.parenthese(expression)
    self.equation = expression

#On crée une classe Calculatrice qui va nous permettrede calculer nos résultats. Cette classe hérite de la classe Expression

class Calculatrice(Expression):

  def __init__(self,input):
    """Notre constructeur crée nos attributs et les initialise:
    Nous ajoutons un attributs résultats"""
    Expression.__init__(self, input)
    self.Resultat = 0

  def __repr__(self):
        """Cette méthode affiche l'objet"""
        return "Equation : {}\nResultat : {}".format(self.eq, self.Resultat)

  def affiche(self):
    """C'est pour mettre en évidence le polymorphisme"""
    return("Equation : {} \n Resultat : {}".format(self.eq, self.Resultat))

  def __sub__(self, objet_a_ajouter):
        """surcharge de l'opérateur -"""
        nouvelle_expression = Calculatrice(self.equation)
        nouvelle_expression.Resultat = self.Resultat
        nouvelle_expression.equation = self.equation
        nouvelle_expression.equation = "(" + nouvelle_expression.equation + ")" + "-" + "(" + objet_a_ajouter.equation + ")"
        nouvelle_expression.eq = "(" + nouvelle_expression.eq + ")" + "-" + "(" + objet_a_ajouter.eq + ")"
        nouvelle_expression.Resultat = nouvelle_expression.Resultat - objet_a_ajouter.Resultat
        return nouvelle_expression

  def resultat(self):
    """Ici nous obtenons le résultats final"""
    self.modification()
    expression = self.equation
    for k in expression :
      if(type(k)==list):
        idx = expression.index(k)
        res = self.calcul_list(k)
        del expression[idx]
        expression.insert(idx,res[0])
    expression = self.calcul_list(expression)
    if (expression == 'ERREUR'):
      self.Resultat='ERREUR'
    else:
      self.Resultat = expression[0]

  def calcul_list(self , op):
    """On calcule le resultat pour une liste donnée du format de nos expressions
    L'ordre d'application des méthodes prend en compte les priorité des opérateurs de calculs"""
    expression = op
    for k in expression:
      if (k=='ERREUR'):
        return ('ERREUR')
      else:
        expression = self.puissance(expression)
        expression = self.racine(expression)
        expression = self.multiplication(expression)
        expression = self.division(expression)
        expression = self.addition(expression)
        expression = self.soustraction(expression)
    return(expression)
   
  def puissance(self, op):
    expression = op
    while "^" in expression :
      idx = expression.index("^")
      sous_list = expression[idx-1:idx+2]
      del expression[idx-1:idx+2]
      res = sous_list[0]**sous_list[2]
      expression.insert(idx-1,res)
    return(expression) 

  def racine(self,op):
    expression = op
    while "r" in expression :
      idx = expression.index("r")
      sous_list = expression[idx:idx+2]
      del expression[idx:idx+2]
      res = sous_list[1]**0.5
      expression.insert(idx-1,res)
    return(expression) 

  def multiplication(self , op):
    expression = op
    while "*" in expression :
      idx = expression.index("*")
      sous_list = expression[idx-1:idx+2]
      del expression[idx-1:idx+2]
      res = sous_list[0]*sous_list[2]
      expression.insert(idx-1,res)
    return(expression)

  def division(self, op):
    expression = op
    while "/" in expression :
      idx = expression.index("/")
      sous_list = expression[idx-1:idx+2]
      del expression[idx-1:idx+2]
      if (sous_list[2]==0):
        return ('ERREUR')
      else:
        res = sous_list[0]/sous_list[2]
        expression.insert(idx-1,res)
    return(expression)


  def addition(self,op):
    expression = op
    while "+" in expression :
      idx = expression.index("+")
      if  type(expression[idx-1])!=float or type(expression[idx+1])!=float :
        idx1 = idx
        idx2 = idx
        if(type(expression[idx-1])!=float):
          idx1 = idx1 - 2
          idx2 = idx2 + 1
        if(type(expression[idx+1])!=float):
          idx2 = idx2 + 2
          idx1 = idx1 - 1
        sous_list = expression[idx1:idx2+1]
        del expression[idx1:idx2+1]
        res = sous_list[0]-sous_list[-1]
        expression.insert(idx-1,res)
      else:
        sous_list = expression[idx-1:idx+2]
        del expression[idx-1:idx+2]
        res = sous_list[0]+sous_list[2]
        expression.insert(idx-1,res)
    return(expression)

  def soustraction(self,op):
    expression = op
    while "-" in expression :
      idx = expression.index("-")
      if  type(expression[idx-1])!=float or type(expression[idx+1])!=float :
        idx1 = idx
        idx2 = idx
        if(type(expression[idx-1])!=float):
          idx1 = idx1 - 2
          idx2 = idx2 + 1
        if(type(expression[idx+1])!=float):
          idx2 = idx2 + 2
          idx1 = idx1 - 1
        sous_list = expression[idx1:idx2+1]
        del expression[idx1:idx2+1]
        res = sous_list[0]+sous_list[-1]
        expression.insert(idx-1,res)
      elif(idx == 0):
        sous_list = expression[idx:idx+2]
        del expression[idx:idx+2]
        res = 0-sous_list[1]
        expression.insert(idx,res)
      else:
        sous_list = expression[idx-1:idx+2]
        del expression[idx-1:idx+2]
        res = sous_list[0]-sous_list[2]
        expression.insert(idx-1,res)
    return(expression)

####TEST

test = ["1+1","1 + 2","1 + -1","-1 - -1","5-4","5*2","(2+5)*3","10/2","2+2*5+5","22.8*3-1","2^8","2^8*5-1","sqrt(4)","1/0"]

for k in range(len(test)):
  eq = Calculatrice(test[k])
  eq.resultat()
  print(eq)
    
