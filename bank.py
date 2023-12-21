from random import randrange

class Bank:
	def __init__(self):
		self.rolls = 0
		self.count = 0
		self.playersBanked = 0
		self.bust = False
	def roll(self):
		dice1 = randrange(6) + 1
		dice2 = randrange(6) + 1
		dice_sum = dice1 + dice2
		#print(f"dice_sum: {dice_sum}")
		if self.rolls <=3:
			if dice_sum == 7:
				self.count += 70
			else:
				self.count += dice_sum	
		else:
			if dice1 == dice2:
				self.count *= 2
			elif dice_sum == 7:
				self.count = 0
				self.bust = True
			else:
				self.count += dice_sum	
#		#print(f"count: {self.count}")
		self.rolls+=1

class Game:
	def __init__(self):
		self.round = 1 
		self.max_rounds = 15
		self.num_players = 7
		self.bank = Bank()
		self.players = []
		self.playerPool = []
		for i in range(0,self.num_players):
			print(i)
			if randrange(2) % 2 == 0:
				self.players.append(RollCountPlayer(self, randrange(20)+3))
			else:
				self.players.append(ScoreCountPlayer(self, randrange(20) * 50 ))
	def refreshPlayerPool(self):

	def selectPlayers(self):
		 
		
	def playGame(self):
		while self.round <= self.max_rounds:
			#print(f"\nRound {self.round}")
			while not self.bank.bust and \
				self.bank.playersBanked < len(self.players):
				self.bank.roll()
				for player in self.players:
					if not player.calledBank:
						player.checkCallBank()

			for player in self.players:
				player.calledBank = False
			self.round += 1	
			self.playersBanked = 0
			self.bank.bust = False
			self.bank.count = 0
			self.bank.rolls = 0
			self.bank.playersBanked = 0
			for player in self.players:
				player.calledBank = False
		topPlayer = None
		for player in self.players:
			print(f"Player with strategy {player.strategy()} ended game with {player.score} points")
			if topPlayer is None or player.score > topPlayer.score:
				topPlayer = player
		print(f"Player with strategy {topPlayer.strategy()} wins game with score {topPlayer.score}")
		winningStrategy = topPlayer.strategy()
		return winningStrategy

class Player:
	def __init__(self, game):
		self.game = game
		self.score = 0
		self.calledBank = False
		
	def strategy(self):
		print("Define a strategy for this player")
	def callBank(self):
		self.score += self.game.bank.count
		self.calledBank = True
		self.game.bank.playersBanked += 1
#		print(f"Player with strategy {self.strategy()} called bank and gained {self.game.bank.count} points")

class RollCountPlayer(Player):
	def __init__(self, game, roll_limit):
		super().__init__(game)
		self.roll_limit = roll_limit #randrange(15) + 1
#		print(f"New RollCountPlayer with roll_limit {self.roll_limit}")
	def checkCallBank(self):		
		if self.roll_limit == self.game.bank.rolls:
			self.callBank()
			return True 
		else:
			return False	
	def strategy(self):
		return str(f"call bank after {self.roll_limit} rolls")

class ScoreCountPlayer(Player):
	def __init__(self, game, score_limit):
		super().__init__(game)
		self.score_limit = score_limit #randrange(15) + 1
#		print(f"New ScoreCountPlayer with roll_limit {self.roll_limit}")
	def checkCallBank(self):		
		if self.score_limit <= self.game.bank.count:
			self.callBank()
			return True 
		else:
			return False	
	def strategy(self):
		return str(f"call bank after round score passes {self.score_limit}")
			

def main():
	winsByWinningStrategy = {}
	for i in range (1, 50000):
		game = Game()
		winningStrategy = game.playGame()
		if winningStrategy not in winsByWinningStrategy:
			winsByWinningStrategy[winningStrategy] = 1 
		else:
			winsByWinningStrategy[winningStrategy] += 1 	
#	print(f"winsByWinningStrategy: {winsByWinningStrategy}")
	sortedWinsByWinningStrategy = sorted(winsByWinningStrategy)
#	print(f"{sortedWinsByWinningStrategy}")
#	print(f"{winsByWinningStrategy[winningStrategy]} wins by {winningStrategy}")	
	sortedWinsByWinningStrategy = sorted(winsByWinningStrategy.items(), key=lambda x:x[1], reverse=True)
	print(f"{sortedWinsByWinningStrategy}")
	count = 1
	for strategy in sortedWinsByWinningStrategy:
		print(f"{count}: {strategy[1]}  wins. Strategy: {strategy[0]}")
		count += 1
		
		

if __name__ == "__main__":
	main()
