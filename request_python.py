


class Yes():
    pass

uid = 'aasfagew'
object_yes = Yes()

games: dict[str, Yes] = {}

games[uid] = object_yes
games['11'] = object_yes
games['12'] = object_yes

print(games)
print(type(games))