"""
Code for parsing PBN files borrowed from PyBridge
http://4coder.org/python-source-code/18/pybridge-0.3.0/pybridge/bridge/pbn.py.html
"""

from game_state import *

class ParseError(Exception):
    """Raised when PBN parser encounters an unexpected input."""

def importPBN(pbn):
    SUIT = 'SHDC'
    CARDRANK = dict(zip('23456789TJQKA',range(2,15)))
    POSITION = dict(zip('NESW',Player.POSITION))
    PLAYERINDEX = dict(zip('NESW',range(1,5)))
    tags, sections, notes = parsePBN(pbn)
    if 'Deal' not in tags:
        raise ParseError, "Required tag 'Deal' not found"
    first, cards = tags['Deal'].split(":")
    index = PLAYERINDEX[first.strip()]
    order = Player.POSITION[index:] + Player.POSITION[:index]
    hands = {}
    for player, hand in zip(order, cards.strip().split()):
        hands[player] = []
        for suit, suitcards in zip(SUIT, hand.split('.')):
            for rank in suitcards:
                card = Card(suit,CARDRANK[rank])
                hands[player].append(card)
    if 'Play' in tags:
        first = POSITION[tags['Play']]
    else:
        first = Player.WEST
    deal = Deal(hands,first)
    if not deal.isValidDeal():
        raise ParseError, "Deal does not validate"
    return GameState.create_initial(deal)

def parsePBN(pbn):
    """Parses the given PBN string and extracts:
    
      * for each PBN tag, a dict of associated key/value pairs.
      * for each data section, a dict of key/data pairs.
        
    This method does not interpret the PBN string itself.
    
    @param pbn: a string containing PBN markup.
    @return: a tuple (tag values, section data, notes).
    """
    tagValues, sectionData, notes = {}, {}, {}
    tag = 'Default Tag'
    for line in pbn.splitlines():
        line.strip()  # Remove whitespace.

        if line.startswith('%'):  # A comment.
            pass  # Skip over comments.

        elif line.startswith('['):  # A tag.
            line = line.strip('[]')  # Remove leading [ and trailing ].
            # The key is the first word, the value is everything after.
            tag, value = line.split(' ', 1)
            tag = tag.capitalize()
            value = value.strip('\'\"')
            if tag == 'Note':
                notes.setdefault(tag, [])
                notes[tag].append(value)
            else:
                tagValues[tag] = value

        else:  # Line follows tag, add line to data buffer for section.
            sectionData.setdefault(tag, '')
            sectionData[tag] += line + '\n'

    return tagValues, sectionData, notes


def testImport():
    pbnstr = file("pbn_files/OptimumResultTable.pbn").read()
    g = importPBN(pbnstr)
    return g
