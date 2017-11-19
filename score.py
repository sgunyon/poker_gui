class Score:

    def __init__(self, suits, ranks):
        self.suits = suits
        self.ranks = ranks

    def is_flush(self):
        current_suit = self.suits[0]
        return all(suit == current_suit for suit in self.suits)

    def is_royal_flush(self):
        low = min(self.ranks)
        return low == 10 and self.is_straight() and self.is_flush()

    def is_four_of_a_kind(self):
        card_one_count = self.ranks.count(self.ranks[0])
        card_two_count = self.ranks.count(self.ranks[1])
        return card_one_count == 4 or card_two_count == 4

    def is_straight(self):
        self.eval_ace_low()
        low = min(self.ranks)
        return all((low + i) in self.ranks for i in range(1, 5))

    def is_three_of_a_kind(self):
        card_one_count = self.ranks.count(self.ranks[0])
        card_two_count = self.ranks.count(self.ranks[1])
        card_three_count = self.ranks.count(self.ranks[2])
        return card_one_count == 3 or card_two_count == 3 or card_three_count == 3

    def is_two_pair(self):
        count = 0
        for rank in self.ranks:
            if self.ranks.count(rank) > 1:
                count += 1
            else:
                continue
        return count >= 3

    def is_pair(self):
        return any(self.ranks.count(rank) > 1 for rank in self.ranks)

    def is_full_house(self):
        self.ranks.sort()
        card_one_count = self.ranks.count(self.ranks[0])
        card_two_count = self.ranks.count(self.ranks[len(self.ranks) - 1])
        return (card_one_count == 2 and card_two_count == 3) or (card_one_count == 3 and card_two_count == 2)

    def is_straight_flush(self):
        self.eval_ace_low()
        return self.is_flush() and self.is_straight()

    def eval_ace_low(self):
        if all(x in self.ranks for x in range(2, 6)) and 14 in self.ranks:
            self.ranks.append(1)

    def eval_hand(self):
        if self.is_royal_flush():
            return "Royal Flush!"
        elif self.is_straight_flush():
            return "Straight Flush!"
        elif self.is_four_of_a_kind():
            return "Four of a Kind!"
        elif self.is_full_house():
            return "Full House!"
        elif self.is_flush():
            return "Flush!"
        elif self.is_straight():
            return "Straight!"
        elif self.is_three_of_a_kind():
            return "Three of a Kind!"
        elif self.is_two_pair():
            return "Two Pair!"
        elif self.is_pair():
            return "Pair!"
        else:
            return "High card"

