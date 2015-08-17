/***************************************************************************\
The MIT License (MIT)

Copyright (c) 2015 Jonas Schiegl (https://github.com/senritsu)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
\***************************************************************************/

using System;
using System.Collections.Generic;
using System.Linq;
using RiichiSharp.Enums;

namespace RiichiSharp.Analysis
{
    public static class MeldExtensions
    {
        private static readonly Suit[] ValidSequenceSuits = {Suit.Manzu, Suit.Pinzu, Suit.Souzu};

        public static bool IsSequence(this IReadOnlyList<Tile> tiles)
        {
            var suits = tiles.Select(x => x.Suit()).ToArray();
            var minValue = tiles.Min();
            var delta = tiles.Select(x => x - minValue).OrderBy(x => x).Last();

            return delta > 0 && delta == tiles.Count - 1 && suits.Distinct().Count() == 1 && ValidSequenceSuits.Contains(suits.First());
        }

        public static int NormalizedTileCount(this IEnumerable<IReadOnlyList<TileState>> melds)
        {
            return melds.Select(x => x.Count >= 3 ? 3 : 2).Sum();
        }

        public static MeldState MeldState(this IReadOnlyList<Tile> tiles)
        {
            var sequence = tiles.IsSequence();
            var onlyIdenticalTiles = tiles.Distinct().Count() == 1;

            switch (tiles.Count)
            {
                case 0:
                case 1:
                    return Enums.MeldState.Incomplete;
                case 2:
                    if (onlyIdenticalTiles)
                    {
                        return Enums.MeldState.Pair;
                    }
                    if (sequence || Math.Abs(tiles.First() - tiles.Last()) == 2)
                    {
                        return Enums.MeldState.Incomplete;
                    }
                    goto default;
                case 3:
                    if (onlyIdenticalTiles)
                    {
                        return Enums.MeldState.Pon;
                    }
                    if (sequence)
                    {
                        return Enums.MeldState.Chi;
                    }
                    goto default;
                case 4:
                    if (onlyIdenticalTiles)
                    {
                        return Enums.MeldState.Kan;
                    }
                    goto default;
                default:
                    return Enums.MeldState.Invalid;
            }
        }
    }
}
