class Team:
   '''
   Contains List of Junior and senior team members
   '''
   def __init__(self):
       self._juniorMembers = list()
       self._seniorMembers = list()

   def addJuniorMembers(self, members):
       self._juniorMembers += members

   def addSeniorMembers(self, members):
       self._seniorMembers += members



# Create team class object
team = Team()

# Add name of junior team members
team.addJuniorMembers(['Sid', 'Likhi', 'Bargu'])

# Add name of senior team members
team.addSeniorMembers(['Sammu', 'Advik', 'Sathu'])

iter(team)

for member in team:
   print(member)
