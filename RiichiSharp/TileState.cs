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
using System.Linq;
using RiichiSharp.Enums;

namespace RiichiSharp
{
    public class TileState
    {
        public bool Open { get; set; }
        public Tile Tile { get; set; }

        public static implicit operator Tile(TileState state)
        {
            return state.Tile;
        }
    }

    public static class TileGroup
    {
        public static readonly Tile[] Terminals = {Tile.Pin1, Tile.Pin9, Tile.Sou1, Tile.Sou9, Tile.Man1, Tile.Man9};
        public static readonly Tile[] Honors = {Tile.Ton, Tile.Nan, Tile.Xia, Tile.Pei, Tile.Haku, Tile.Hatsu, Tile.Chun};
        public static readonly Tile[] Simples = Enum.GetValues(typeof (Tile)).Cast<Tile>().Except(Terminals).Except(Honors).ToArray();
    }

    public static class TileExtensions
    {
        public static bool IsHonor(this Tile tile)
        {
            return TileGroup.Honors.Contains(tile);
        }

        public static bool IsNumeric(this Tile tile)
        {
            return !tile.IsHonor();
        }

        public static bool IsSimple(this Tile tile)
        {
            return TileGroup.Simples.Contains(tile);
        }

        public static bool IsTerminal(this Tile tile)
        {
            return TileGroup.Terminals.Contains(tile);
        }

        public static Suit Suit(this Tile tile)
        {
            if (tile < Tile.Pin1 || tile > Tile.Chun)
            {
                throw new ArgumentOutOfRangeException("tile", "Invalid tile value");
            }
            foreach (var suit in Enum.GetValues(typeof(Suit)).Cast<Suit>())
            {
                if ((int)tile < (int)suit)
                {
                    return suit;
                }
            }
            throw new IndexOutOfRangeException("Tile value inside bounds, but no suit found");
        }

        public static Tile Shift(this Tile tile, int shift)
        {
            var suit = tile.Suit();

            int mod;
            switch (suit)
            {
                case Enums.Suit.Kazehai:
                    mod = 4;
                    break;
                case Enums.Suit.Sangenpai:
                    mod = 3;
                    break;
                default:
                    mod = 9;
                    break;
            }

            var offset = (int)suit - mod;
            var x = (int)tile - offset + shift;

            return (Tile) (offset + (shift < 0 ? ((x%mod) + mod)%mod : x%mod));
        }

        public static Tile Next(this Tile tile)
        {
            return tile.Shift(1);
        }

        public static Tile Previous(this Tile tile)
        {
            return tile.Shift(-1);
        }

        public static bool CanFormSequence(this Tile tile)
        {
            return (int)tile < (int)Enums.Suit.Manzu;
        }
    }
}
