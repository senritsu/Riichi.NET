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
using NUnit.Framework;

namespace RiichiSharp.Tests
{
    [TestFixture]
    public class TileTests
    {
        [TestCase(Tile.Pin2, ExpectedResult = Tile.Pin3)]
        [TestCase(Tile.Pin9, ExpectedResult = Tile.Pin1)]
        [TestCase(Tile.Man1, ExpectedResult = Tile.Man2)]
        [TestCase(Tile.Sou6, ExpectedResult = Tile.Sou7)]
        [TestCase(Tile.Ton, ExpectedResult = Tile.Nan)]
        [TestCase(Tile.Nan, ExpectedResult = Tile.Xia)]
        [TestCase(Tile.Xia, ExpectedResult = Tile.Pei)]
        [TestCase(Tile.Pei, ExpectedResult = Tile.Ton)]
        [TestCase(Tile.Haku, ExpectedResult = Tile.Hatsu)]
        [TestCase(Tile.Hatsu, ExpectedResult = Tile.Chun)]
        [TestCase(Tile.Chun, ExpectedResult = Tile.Haku)]
        public Tile Tile_Next(Tile tile)
        {
            return tile.Next();
        }

        [TestCase(Tile.Pin1, ExpectedResult = Tile.Pin9)]
        [TestCase(Tile.Pin7, ExpectedResult = Tile.Pin6)]
        [TestCase(Tile.Man9, ExpectedResult = Tile.Man8)]
        [TestCase(Tile.Sou4, ExpectedResult = Tile.Sou3)]
        [TestCase(Tile.Ton, ExpectedResult = Tile.Pei)]
        [TestCase(Tile.Nan, ExpectedResult = Tile.Ton)]
        [TestCase(Tile.Xia, ExpectedResult = Tile.Nan)]
        [TestCase(Tile.Pei, ExpectedResult = Tile.Xia)]
        [TestCase(Tile.Haku, ExpectedResult = Tile.Chun)]
        [TestCase(Tile.Hatsu, ExpectedResult = Tile.Haku)]
        [TestCase(Tile.Chun, ExpectedResult = Tile.Hatsu)]
        public Tile Tile_Previous(Tile tile)
        {
            return tile.Previous();
        }

        [TestCase(Tile.Haku, 2, ExpectedResult = Tile.Chun)]
        [TestCase(Tile.Pin2, 5, ExpectedResult = Tile.Pin7)]
        [TestCase(Tile.Man8, 3, ExpectedResult = Tile.Man2)]
        [TestCase(Tile.Sou2, -3, ExpectedResult = Tile.Sou8)]
        [TestCase(Tile.Ton, 4, ExpectedResult = Tile.Ton)]
        public Tile Tile_Shift(Tile tile, int shift)
        {
            return tile.Shift(shift);
        }

        [TestCase(Tile.Pin1, ExpectedResult = Suit.Pinzu)]
        [TestCase(Tile.Pin5, ExpectedResult = Suit.Pinzu)]
        [TestCase(Tile.Pin9, ExpectedResult = Suit.Pinzu)]
        [TestCase(Tile.Man1, ExpectedResult = Suit.Manzu)]
        [TestCase(Tile.Man2, ExpectedResult = Suit.Manzu)]
        [TestCase(Tile.Man9, ExpectedResult = Suit.Manzu)]
        [TestCase(Tile.Sou1, ExpectedResult = Suit.Souzu)]
        [TestCase(Tile.Sou7, ExpectedResult = Suit.Souzu)]
        [TestCase(Tile.Sou9, ExpectedResult = Suit.Souzu)]
        [TestCase(Tile.Hatsu, ExpectedResult = Suit.Sangenpai)]
        [TestCase(Tile.Haku, ExpectedResult = Suit.Sangenpai)]
        [TestCase(Tile.Chun, ExpectedResult = Suit.Sangenpai)]
        [TestCase(Tile.Ton, ExpectedResult = Suit.Kazehai)]
        [TestCase(Tile.Nan, ExpectedResult = Suit.Kazehai)]
        [TestCase(Tile.Xia, ExpectedResult = Suit.Kazehai)]
        [TestCase(Tile.Pei, ExpectedResult = Suit.Kazehai)]
        [TestCase((Tile)40, ExpectedException = typeof(ArgumentOutOfRangeException))]
        [TestCase((Tile)(-1), ExpectedException = typeof(ArgumentOutOfRangeException))]
        public Suit Tile_Suit(Tile tile)
        {
            return tile.Suit();
        }

        [TestCase(Tile.Pin8, ExpectedResult = true)]
        [TestCase(Tile.Man4, ExpectedResult = true)]
        [TestCase(Tile.Sou6, ExpectedResult = true)]
        [TestCase(Tile.Chun, ExpectedResult = false)]
        [TestCase(Tile.Pei, ExpectedResult = false)]
        public bool Tile_CanFormSequence(Tile tile)
        {
            return tile.CanFormSequence();
        }
    }
}
