class TeamIterator:
   ''' Iterator class '''
   def __init__(self, team):
       # Team object reference
       self._team = team
       # member variable to keep track of current index
       self._index = 0

   # To create an Iterator class we need to override __next__() function inside our class
   # __next__() function should be implemented in such a way that every time we call the function it should return the next element of the associated Iterable class.
   # If there are no more elements then it should raise StopIteration.
   def __next__(self):
       ''''Returns the next value from team object's lists '''
       if self._index < (len(self._team._juniorMembers) + len(self._team._seniorMembers)) :
           if self._index < len(self._team._juniorMembers): # Check if junior members are fully iterated or not
               result = (self._team._juniorMembers[self._index] , 'junior')
           else:
               result = (self._team._seniorMembers[self._index - len(self._team._juniorMembers)]   , 'senior')
           self._index +=1
           return result
       # End of Iteration
       raise StopIteration



class Team:
   '''
   Contains List of Junior and senior team members and also overrides the __iter__() function.
   '''
   def __init__(self):
       self._juniorMembers = list()
       self._seniorMembers = list()

   def addJuniorMembers(self, members):
       self._juniorMembers += members

   def addSeniorMembers(self, members):
       self._seniorMembers += members

   def __iter__(self):
       ''' Returns the Iterator object '''
       return TeamIterator(self)



def main():
    # Create team class object
    team = Team()
    # Add name of junior team members
    team.addJuniorMembers(['Sid', 'Likhi', 'Bargu','Kishore'])
    # Add name of senior team members
    team.addSeniorMembers(['Sammu', 'Advik', 'Sathu'])

    print(team)
    print('*** Iterate over the team object using for loop ***')

    # Iterate over team object(Iterable)
    # we call the iter() function on the object of class Team,
    # then it in turn calls the __iter__() function on team object.
    # Which returns the object of Iterator class TeamIterator
    for member in team:
        print(member)

    print('*** Iterate over the team object using while loop ***')

    # Get Iterator object from Iterable Team class oject
    iterator = iter(team)

    # Iterate over the team object using iterator
    while True:
        try:
            # Get next element from TeamIterator object using iterator object
            elem = next(iterator)
            # Print the element
            print(elem)
        except StopIteration:
            break

if __name__ == '__main__':
  main()
