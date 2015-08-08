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

using System.Collections.Generic;
using NUnit.Framework;
using RiichiSharp.Analysis;

namespace RiichiSharp.Tests
{
    [TestFixture]
    class MeldTests
    {
        public IEnumerable<TestCaseData> IsSequence_Source
        {
            get
            {
                yield return new TestCaseData(new[] { Tile.Sou7 }).Returns(false);
                yield return new TestCaseData(new[] { Tile.Pin3, Tile.Pin4 }).Returns(true);
                yield return new TestCaseData(new[] { Tile.Man9, Tile.Man8 }).Returns(true);
                yield return new TestCaseData(new[] { Tile.Sou2, Tile.Sou4 }).Returns(false);
                yield return new TestCaseData(new[] { Tile.Man1, Tile.Man2, Tile.Man3 }).Returns(true);
                yield return new TestCaseData(new[] { Tile.Pin2, Tile.Pin3, Tile.Pin5 }).Returns(false);
                yield return new TestCaseData(new[] { Tile.Sou2, Tile.Sou3, Tile.Sou4, Tile.Sou5 }).Returns(true);
                yield return new TestCaseData(new[] { Tile.Hatsu, Tile.Haku }).Returns(false);
                yield return new TestCaseData(new[] { Tile.Ton }).Returns(false);
                yield return new TestCaseData(new[] { Tile.Nan, Tile.Xia }).Returns(false);
                yield return new TestCaseData(new[] { Tile.Man9, Tile.Man1 }).Returns(false);
                yield return new TestCaseData(new[] { Tile.Chun }).Returns(false);
            }
        }

        [TestCaseSource("IsSequence_Source")]
        public bool TileCollection_IsSequence(IReadOnlyList<Tile> tiles)
        {
            return tiles.IsSequence();
        }

        public IEnumerable<TestCaseData> MeldState_Source_Incomplete
        {
            get
            {
                yield return new TestCaseData(new[] {Tile.Ton}).Returns(MeldState.Incomplete);
                yield return new TestCaseData(new[] {Tile.Sou7}).Returns(MeldState.Incomplete);
                yield return new TestCaseData(new[] {Tile.Chun}).Returns(MeldState.Incomplete);
                yield return new TestCaseData(new[] {Tile.Pin3, Tile.Pin4}).Returns(MeldState.Incomplete);
                yield return new TestCaseData(new[] {Tile.Man9, Tile.Man8}).Returns(MeldState.Incomplete);
                yield return new TestCaseData(new[] {Tile.Sou2, Tile.Sou4}).Returns(MeldState.Incomplete);
            }
        }

        public IEnumerable<TestCaseData> MeldState_Source_Invalid
        {
            get
            {
                yield return new TestCaseData(new[] {Tile.Pin2, Tile.Pin3, Tile.Pin5}).Returns(MeldState.Invalid);
                yield return new TestCaseData(new[] {Tile.Sou2, Tile.Sou3, Tile.Sou4, Tile.Sou5}).Returns(MeldState.Invalid);
                yield return new TestCaseData(new[] {Tile.Hatsu, Tile.Haku}).Returns(MeldState.Invalid);
                yield return new TestCaseData(new[] {Tile.Nan, Tile.Xia}).Returns(MeldState.Invalid);
                yield return new TestCaseData(new[] {Tile.Man9, Tile.Man1}).Returns(MeldState.Invalid);
                yield return new TestCaseData(new[] {Tile.Sou7, Tile.Sou7, Tile.Sou7, Tile.Sou7, Tile.Sou7}).Returns(MeldState.Invalid);
                yield return new TestCaseData(new[] {Tile.Sou7, Tile.Sou7, Tile.Sou7, Tile.Sou8}).Returns(MeldState.Invalid);
            }
        }

        public IEnumerable<TestCaseData> MeldState_Source_Valid
        {
            get
            {
                yield return new TestCaseData(new[] {Tile.Chun, Tile.Chun}).Returns(MeldState.Pair);
                yield return new TestCaseData(new[] {Tile.Haku, Tile.Haku, Tile.Haku}).Returns(MeldState.Pon);
                yield return new TestCaseData(new[] {Tile.Pin3, Tile.Pin3, Tile.Pin3}).Returns(MeldState.Pon);
                yield return new TestCaseData(new[] {Tile.Sou7, Tile.Sou7, Tile.Sou7, Tile.Sou7}).Returns(MeldState.Kan);
                yield return new TestCaseData(new[] {Tile.Man1, Tile.Man2, Tile.Man3}).Returns(MeldState.Chi);
                yield return new TestCaseData(new[] {Tile.Sou7, Tile.Sou8, Tile.Sou9}).Returns(MeldState.Chi);
            }
        }

        [TestCaseSource("MeldState_Source_Invalid")]
        [TestCaseSource("MeldState_Source_Incomplete")]
        [TestCaseSource("MeldState_Source_Valid")]
        public MeldState TileCollection_MeldState_Source(IReadOnlyList<Tile> tiles)
        {
            return tiles.MeldState();
        }
    }
}
