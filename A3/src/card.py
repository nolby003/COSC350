class Card():
    def __init__(self, card_type, image):
        self.card_type = card_type
        self.image = image


class ActionCard(Card):

    def __init__(self, action):
        assert action in ['map', 'sabotage', 'mend', 'dynamite'], "The parameter action must be either map, sabotage, " \
                                                                  "mend or dynamite"

        self._action = action

    def get_action(self):
        return self._action


class InvalidTunnel(Exception):
    pass


class PathCard(Card):

    def __init__(self, tunnels, special_card=None):
        assert isinstance(tunnels, list), "The parameter tunnels must be a list of tuples"
        assert special_card in ['start', 'goal', 'gold', None], "The parameter special_card must be either None, " \
                                                                "start, goal or gold"

        for tunnel in tunnels:
            if not self._is_valid_tunnel(tunnel):
                raise InvalidTunnel("The tunnel '{0}' is an invalid one for this card.".format(tunnel))

        self._special_card = special_card
        self._revealed = False
        if special_card:
            # special cards are all cross roads
            cross_road = PathCard.cross_road()
            self._tunnels = cross_road.get_tunnels()
            if special_card in ['goal', 'gold']:
                self._revealed = False
        else:
            self._tunnels = tunnels

    def cross_road(special_card=None):
        return PathCard(
            [
                ('north', 'south'),
                ('north', 'east'),
                ('north', 'west'),
                ('south', 'east'),
                ('south', 'west'),
                ('east', 'west')
            ], special_card=special_card
            # return PathCard.pathcard['startcard']
        )

    def vertical_tunnel():
        return PathCard(
            [
                ('north', 'south')
            ]
        )

    def horizontal_tunnel():
        return PathCard(
            [
                ('east', 'west')
            ]
        )

    def vertical_junction():
        return PathCard(
            [
                ('north', 'south'),
                ('north', 'east'),
                ('south', 'east')
            ]
        )

    def horizontal_junction():
        return PathCard(
            [
                ('east', 'north'),
                ('west', 'north'),
                ('east', 'west')
            ]
        )

    def turn():
        return PathCard(
            [
                ('south', 'east')
            ]
        )

    def reversed_turn():
        return PathCard(
            [
                ('south', 'west')
            ]
        )

    def dead_end(directions):
        tunnels = []
        for direction in directions:
            tunnels.append((direction, None))
        return PathCard(tunnels)

    def _is_valid_tunnel(self, tunnel):
        if not isinstance(tunnel, tuple):
            return False
        if len(tunnel) != 2:
            return False
        for direction in tunnel:
            if direction not in ['north', 'east', 'south', 'west', None]:
                return False
        if tunnel[0] is None:
            return False
        if tunnel[0] is None and tunnel[1] is None:
            return False
        if tunnel[0] == tunnel[1]:
            return False

        return True

    def is_special_card(self):
        return self._special_card is not None

    def is_gold(self):
        return self._special_card == 'gold'

    def reveal_card(self):
        self._revealed = True

    def turn_card(self):
        tunnels = []
        opposite = {
            'north': 'south',
            'east': 'west',
            'west': 'east',
            'south': 'north',
        }
        for tunnel in self._tunnels:
            new_tunnel = (
                opposite[tunnel[0]] if tunnel[0] is not None else None,
                opposite[tunnel[1]] if tunnel[1] is not None else None
            )
            tunnels.append(new_tunnel)

        self._tunnels = tunnels

    def get_tunnels(self):
        return self._tunnels.copy()

    def __str__(self):
        # print('foo')
        card_rep = ['   ', '   ', '   ']
        if self._revealed:
            for tunnel in self._tunnels:
                directions = [(tunnel[0], tunnel[1]), (tunnel[1], tunnel[0])]
                for direction in directions:
                    tunnel_from = direction[0]
                    tunnel_to = direction[1]
                    if tunnel_from == 'north':
                        card_rep[0] = card_rep[0][:1] + '|' + card_rep[0][2:]
                        if tunnel_to is not None:
                            card_rep[1] = card_rep[1][:1] + '┼' + card_rep[1][2:]
                    elif tunnel_from == 'south':
                        card_rep[2] = card_rep[2][:1] + '|' + card_rep[2][2:]
                        if tunnel_to is not None:
                            card_rep[1] = card_rep[1][:1] + '┼' + card_rep[1][2:]
                    elif tunnel_from == 'east':
                        card_rep[1] = card_rep[1][:2] + '—'
                        if tunnel_to is not None:
                            card_rep[1] = card_rep[1][:1] + '┼' + card_rep[1][2:]
                    elif tunnel_from == 'west':
                        card_rep[1] = '—' + card_rep[1][1:]
                        if tunnel_to is not None:
                            card_rep[1] = card_rep[1][:1] + '┼' + card_rep[1][2:]
        else:
            return '   \n ? \n   '
        return '\n'.join(card_rep)
