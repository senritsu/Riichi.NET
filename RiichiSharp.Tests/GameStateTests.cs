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
using RiichiSharp.Rules;

namespace RiichiSharp.Tests
{
    [TestFixture]
    public class GameStateTests
    {

        private class RoundBuilder
        {
            private readonly GameState _gameState = new GameState();

            public RoundBuilder Result(int oya, int? winner)
            {
                _gameState.Rounds.Add(new RoundState {Oya = oya, Result = new RoundResult {Draw = !winner.HasValue, Winner = winner ?? 0}});
                return this;
            }

            public TestCaseData Unfinished(int oya)
            {
                _gameState.Rounds.Add(new RoundState { Oya = oya });
                return ToTestCaseData();
            }

            public TestCaseData ToTestCaseData()
            {
                return new TestCaseData(_gameState);
            }
        }
        

        private IEnumerable<TestCaseData> Oyarenchan_Source
        {
            get
            {
                yield return new RoundBuilder().Result(0, 2).Result(1, 1).ToTestCaseData().Returns(1);
                yield return new RoundBuilder().Result(0, 0).Result(0, 0).Result(0, 3).Result(1, 1).ToTestCaseData().Returns(1);
                yield return new RoundBuilder().Result(0, 1).Result(1, 1).ToTestCaseData().Returns(1);
                yield return new RoundBuilder().Result(0, 0).Result(0, null).Result(0, 0).ToTestCaseData().Returns(3);
                yield return new RoundBuilder().Result(0, 0).Result(0, null).Result(0, 0).Unfinished(0).Returns(3);
                yield return new RoundBuilder().Result(0, 0).Result(0, null).Result(0, 0).Result(0, 3).ToTestCaseData().Returns(0);
                yield return new RoundBuilder().Result(0, 0).Result(0, 1).Result(1, null).Result(1,2).Result(2, 2).Unfinished(2).Returns(1);
                yield return new RoundBuilder().Result(0, 1).Result(1, 2).Result(2, 3).Result(3,null).Result(3, 4).Unfinished(4).Returns(0);
            }
        }

        [TestCaseSource("Oyarenchan_Source")]
        public int Oyarenchan_Calculation(GameState state)
        {
            return state.Oyarenchan;
        }
    }
}
