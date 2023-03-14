import math
import re

class Category:

  def __init__(self, categories):
    self.categories = categories
    self.ledger = []
    self.budget = 00.00
    self.withdrawAmt = 00.00

  def __str__(self):
    returnString = f"{self.categories:*^30}"
    totalValue = 0
    
    for i in range(len(self.ledger)):
      for key, value in self.ledger[i].items():
        
        if key == "amount":
          totalValue += value
          emptyString = f"{'%.2f' % value:>7}"
        else:
          returnString += f"\n{value:<23}"[:24] + emptyString

    returnString += f"\nTotal: {totalValue}"

    return returnString
      

  def deposit(self, amount, description=""):
    self.amount = amount
    self.description = description
    self.budget += amount
    self.ledger.append({"amount": self.amount,"description": self.description})

  def withdraw(self, amount, description=""):
    self.amount = amount
    self.description = description
    if self.check_funds(amount):
      self.withdrawAmt += amount
      self.budget -= amount
      self.ledger.append({"amount": -self.amount, "description": self.description})
      return True
    else:
      return False

  def get_balance(self):
    return self.budget

  def transfer(self, amount, categoryDest):
    self.amount = amount
    self.description = f"Transfer to {categoryDest.categories}"

    if self.check_funds(amount):
      self.budget -= amount
      destDescription = f"Transfer from {self.categories}"
      self.ledger.append({"amount": -self.amount, "description": self.description})
      categoryDest.deposit(amount, destDescription)
      return True
    else:
      return False

  def check_funds(self, amount):
    if self.budget >= amount:
      return True
    else:
      return False


def create_spend_chart(categories):
  names = []
  lengthNames = []
  returnString = "Percentage spent by category\n100|\n 90|\n 80|\n 70|\n 60|\n 50|\n 40|\n 30|\n 20|\n 10|\n  0|\n    ----"
  iterInd = [match.start() for match in re.finditer("\n ", returnString)]
  fullAmt = 00.00
  percentages = []
  allPercentages = [100, 90, 80, 70, 60, 50, 40, 30, 20, 10, 0]
  
  for category in categories:
    fullAmt += category.withdrawAmt

  for i in range(len(categories)):
    categoryName = tuple(categories[i].categories)
    names.append(categoryName)
    lengthNames.append(len(categoryName))
    percentage = math.floor((categories[i].withdrawAmt/fullAmt)*10)*10
    percentages.append(percentage)
    if i == 0:
      for j in range(len(iterInd)):
        iterInd = [match.start() for match in re.finditer("\n ", returnString)]
        if allPercentages[j] > percentages[i]:
          returnString = returnString[:iterInd[j]] + "    " + returnString[iterInd[j]:]
        else:
          returnString = returnString[:iterInd[j]] + " o  " + returnString[iterInd[j]:]
    else:
      for j in range(len(iterInd)):
        iterInd = [match.start() for match in re.finditer("\n ", returnString)]
        if allPercentages[j] > percentages[i]:
          returnString = returnString[:iterInd[j]] + "   " + returnString[iterInd[j]:]
        else:
          returnString = returnString[:iterInd[j]] + "o  " + returnString[iterInd[j]:]
      dashIndex = returnString.find("-")
      returnString = returnString[:dashIndex] + "---" + returnString[dashIndex:]

  maxLength = max(lengthNames)
  
  for i in range(maxLength):
    returnString += "\n   "
    for j in range(len(names)):
      try:
        returnString += f"  {names[j][i]}"
      except:
        returnString += "   "
    returnString += "  "
  
  return returnString