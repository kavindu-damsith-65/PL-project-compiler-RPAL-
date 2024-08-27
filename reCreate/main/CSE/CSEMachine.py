from .elements.EleValue import EleValue
from .elements.EleTuple import EleTuple
from .elements.EleValueOrTuple import EleValueOrTuple
from .ExceptionHandlerOfCSE import ExceptionHandlerOfCSE
from INTERPRETER.OperationHandler import OperationHandler
from .Environment import Environment
from collections import deque

class CSEMachine:
    def __init__(self, controlStructures):
        self.CS = controlStructures
        self.eleValueOrTuples = deque()
        self.operationHandler = OperationHandler()

        self.eleValues = deque()
        self.eleValues.append(EleValue("environment", "0"))
        self.eleValues.append(EleValue("delta", "0"))
        self.eleValueOrTuples.append(EleValue("environment", "0"))
        self.environments = [Environment()]

    def toString(self):
        return str(self.eleValues) + "\n" + str(self.eleValueOrTuples) + "\n" + str(self.currentEnvironment()) + "\n"

    def currentEnvironmentIndex(self):
        closestEnvironment = 0
        for element in self.eleValues:
            if isinstance(element, EleValue) and element.isLabel("environment"):
                closestEnvironmentStr = element.getValue()
                closestEnvironment = int(closestEnvironmentStr)
        return closestEnvironment

    def currentEnvironment(self):
        return self.environments[self.currentEnvironmentIndex()]

    def evaluateTree(self):
        counter=0
      
        while self.eleValues:
            counter+=1
            # print(counter)
            currentElement = self.eleValues.pop()
            # print(currentElement.getLabel())
            if currentElement.isLabel("gamma"):
                firstElem = self.eleValueOrTuples.pop()
                secondElem = self.eleValueOrTuples.pop()
                if firstElem.isLabel("yStar"):
                    self.rule12(secondElem)
                elif firstElem.isLabel("eta"):
                    self.eleValueOrTuples.append(secondElem)
                    self.rule13(currentElement, firstElem)
                elif firstElem.isLabel("lambda"):
                    firstValue = firstElem
                    if "," in firstValue.getValue():
                        self.rule11(firstElem, secondElem)
                    else:
                        self.rule4(firstElem, secondElem)
                elif firstElem.isLabel("tau"):
                    self.rule10(firstElem, secondElem)
                else:
                   
                    self.rule3(firstElem, secondElem)
            elif currentElement.isLabel("delta"):
                controlIndex = int(currentElement.getValue())
                self.extractDelta(controlIndex)
            elif currentElement.isLabel("id"):
                self.rule1(currentElement)
            elif currentElement.isLabel("lambda"):
                self.rule2(currentElement)
            elif currentElement.isLabel("environment"):
                self.rule5(currentElement)
            elif currentElement.isLabel("beta"):
                self.rule8()
            elif currentElement.isLabel("tau"):
                self.rule9(currentElement)
            elif not self.rule6_7(currentElement):
                self.eleValueOrTuples.append(currentElement)
        
    def extractDelta(self, controlIndex):
        control = self.CS[controlIndex]
        for controlElem in control:
            self.eleValues.append(controlElem)

    def rule1(self, name):
        id = name.getValue()
        value = self.currentEnvironment().lookup(id)
        if value is None:
            value = EleValue(id)
        self.eleValueOrTuples.append(value)

    def rule2(self, lambdaVal):
        kAndX = lambdaVal.getValue().split(" ")
        c = str(self.currentEnvironmentIndex())
        newValues = [kAndX[0], kAndX[1], c]
        newLambda = EleValue("lambda", " ".join(newValues))
        self.eleValueOrTuples.append(newLambda)

    def rule3(self, rator, rand):
        
        result = self.operationHandler.apply(rator, rand)
        self.eleValueOrTuples.append(result)

    def rule4(self, lambdaVal, rand):
        if isinstance(lambdaVal, EleValue) and lambdaVal.isLabel("lambda"):
            kAndXAndC = lambdaVal.getValue().split(" ")
            k, x, c = kAndXAndC[0], kAndXAndC[1], kAndXAndC[2]
            envC = self.environments[int(c)]

            newEnvironment = Environment(envC, x, rand)
            newEnvIndex = str(len(self.environments))
            self.environments.append(newEnvironment)
            self.eleValues.append(EleValue("environment", newEnvIndex))
            self.eleValues.append(EleValue("delta", k))
            self.eleValueOrTuples.append(EleValue("environment", newEnvIndex))
            return
        raise ExceptionHandlerOfCSE("Expected lambda element but found: " + lambdaVal)

    def rule5(self, env):
       
        value = self.eleValueOrTuples.pop()
        envS = self.eleValueOrTuples.pop()
        if isinstance(envS, EleValue) and envS.isLabel("environment"):
          
            if env.equals(envS):
                self.eleValueOrTuples.append(value)
                return
            raise ExceptionHandlerOfCSE("Environment element mismatch: {} and {}".format(env, envS))
        raise ExceptionHandlerOfCSE("Expected environment element but found: " + envS)

    def rule6_7(self, element):
        if self.operationHandler.checkMathematicalOperation(element):
            rator = self.eleValueOrTuples.pop()
            rand = self.eleValueOrTuples.pop()
            result = self.operationHandler.applyOperations(element, rator, rand)
            self.eleValueOrTuples.append(result)
        elif self.operationHandler.checkArrayOperation(element):
            rand = self.eleValueOrTuples.pop()
            result = self.operationHandler.apply(element, rand)
            self.eleValueOrTuples.append(result)
        else:
            return False
        return True

    def rule8(self):
        deltaElse = self.eleValues.pop()
        deltaThen = self.eleValues.pop()
        condition = self.eleValueOrTuples.pop()

        if deltaElse.isLabel("delta") and deltaThen.isLabel("delta"):
            if condition.isLabel("true"):
                self.eleValues.append(deltaThen)
                return
            elif condition.isLabel("false"):
                self.eleValues.append(deltaElse)
                return
            raise RuntimeError("If condition must evaluate to a truth value.")
        raise ExceptionHandlerOfCSE("Expected delta elements.")

    def rule9(self, tau):
        elements = int(tau.getValue())
        tupleElements = [self.eleValueOrTuples.pop() for _ in range(elements)]
        tupleVal = EleTuple(tupleElements)
        self.eleValueOrTuples.append(tupleVal)

    def rule10(self, tupleVal, index):
        if isinstance(tupleVal, EleTuple):
            if isinstance(index, EleValue) and index.isLabel("int"):
                ind = int(index.getValue())
                value = tupleVal.getValue()[ind]
                self.eleValueOrTuples.append(value)
                return
            raise ExceptionHandlerOfCSE("Expected integer index but found: " + index)
        raise ExceptionHandlerOfCSE("Expected tuple but found: " + tupleVal)

    def rule11(self, lambdaVal, rand):
        if isinstance(lambdaVal, EleValue) and lambdaVal.isLabel("lambda"):
            if isinstance(rand, EleTuple):
                kAndVAndC = lambdaVal.getValue().split(" ")
                k, v, c = kAndVAndC[0], kAndVAndC[1].split(","), kAndVAndC[2]
                envC = self.environments[int(c)]

                newEnvironment = Environment(envC)
                for i in range(len(v)):
                    newEnvironment.remember(v[i], rand.getValue()[i])
                newEnvIndex = str(len(self.environments))
                self.environments.append(newEnvironment)
                self.eleValues.append(EleValue("environment", newEnvIndex))
                self.eleValues.append(EleValue("delta", k))
                self.eleValueOrTuples.append(EleValue("environment", newEnvIndex))
                return
            raise ExceptionHandlerOfCSE("Expected tuple but found: " + rand)
        raise ExceptionHandlerOfCSE("Expected lambda element but found: " + lambdaVal)

    def rule12(self, lambdaVal):
        if isinstance(lambdaVal, EleValue) and lambdaVal.isLabel("lambda"):
            iAndVAndC = lambdaVal.getValue()
            etaElement = EleValue("eta", iAndVAndC)
            self.eleValueOrTuples.append(etaElement)
            return
        raise ExceptionHandlerOfCSE("Expected lambda element but found: " + lambdaVal)

    def rule13(self, gamma, eta):
        if isinstance(eta, EleValue) and eta.isLabel("eta"):
            iAndVAndC = eta.getValue()
            lambdaVal = EleValue("lambda", iAndVAndC)
            newGamma = EleValue("gamma")

            self.eleValueOrTuples.append(eta)
            self.eleValueOrTuples.append(lambdaVal)

            self.eleValues.append(gamma)
            self.eleValues.append(newGamma)
            return
        raise ExceptionHandlerOfCSE("Expected eta element but found: " + eta)
