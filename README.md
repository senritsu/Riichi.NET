# Riichi.NET
C# library for Riichi Mahjong (Japanese Mahjong)

Intended as a standalone pure C# library for everything related to Japanese Riichi Mahjong.
Will be supplemented by a Unity3D wrapper for easy integration in Unity projects.

[![Coverage Status](https://coveralls.io/repos/senritsu/Riichi.NET/badge.svg?branch=master&service=github)](https://coveralls.io/github/senritsu/Riichi.NET?branch=master)

## Planned Features:
### phase 1
- full modeling of game state
- all required logic for running a game from start to finish
- complete rule set for the most common rules

### phase 2
- support for most common variants (double ron, akadora, uma, ...)
- point calculations for any given hand
- hand analysis (which combinations of yaku can be fit into a finished hand)

### phase 3
- hand state validation (shanten, tenpai)
- hand assistance (which yaku are how far away for an unfinished hand)
