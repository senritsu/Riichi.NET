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
using System.Linq;
using NUnit.Framework;
using RiichiSharp.Rules;

namespace RiichiSharp.Tests
{
    [TestFixture]
    public class MahjongGameTests
    {

        private class RoundBuilder
        {
            private readonly MahjongGame _gameState;

            public RoundBuilder(bool tonpuusen = false)
            {
                _gameState = new MahjongGame(tonpuusen);
            }

            public RoundBuilder Result(int oya, int? winner)
            {
                _gameState.Rounds.Add(new RoundState {Oya = oya, Result = new RoundResult { Winner = winner }});
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

        private IEnumerable<TestCaseData> Renchan_Source
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

        [TestCaseSource("Renchan_Source")]
        public int Renchan_Calculation(MahjongGame game)
        {
            return game.Renchan;
        }

        private IEnumerable<TestCaseData> Oya_Source
        {
            get
            {
                yield return new RoundBuilder().Unfinished(0).Returns(0);
                yield return new RoundBuilder().Result(0, null).ToTestCaseData().Returns(0);
                yield return new RoundBuilder().Result(0, 0).ToTestCaseData().Returns(0);
                yield return new RoundBuilder().Result(0, 1).ToTestCaseData().Returns(1);
                yield return new RoundBuilder().Result(0, 1).Result(1, 1).ToTestCaseData().Returns(1);
                yield return new RoundBuilder().Result(0, 1).Result(1, null).ToTestCaseData().Returns(1);
                yield return new RoundBuilder().Result(0, 1).Result(1, 3).ToTestCaseData().Returns(2);
                yield return new RoundBuilder().Result(0, 2).Result(1, 2).Result(2, 0).ToTestCaseData().Returns(3);
                yield return new RoundBuilder().Result(0, 3).Result(1, 3).Result(2, 3).Unfinished(3).Returns(3);
                yield return new RoundBuilder().Result(0, 3).Result(1, 3).Result(2, 3).Result(3, null).ToTestCaseData().Returns(3);
                yield return new RoundBuilder().Result(0, 3).Result(1, 3).Result(2, 3).Result(3, 1).ToTestCaseData().Returns(0);
                yield return new RoundBuilder().Result(0, 3).Result(1, 3).Result(2, 3).Result(3, 1).Result(0,2).ToTestCaseData().Returns(1);
            }
        }

        [TestCaseSource("Oya_Source")]
        public int Oya_Calculation(MahjongGame game)
        {
            return game.Oya;
        }

        private IEnumerable<TestCaseData> GameState_Source
        {
            get
            {
                yield return new RoundBuilder().ToTestCaseData().Returns(GameState.Preparation);

                yield return new RoundBuilder().Result(0, 1).ToTestCaseData().Returns(GameState.BetweenRounds);
                yield return new RoundBuilder()
                    .Result(0, 1).Result(1, 2).Result(2, 3).Result(3, 0)
                    .ToTestCaseData().Returns(GameState.BetweenRounds);

                yield return new RoundBuilder().Unfinished(0).Returns(GameState.RoundRunning);
                yield return new RoundBuilder().Result(0, 1).Unfinished(1).Returns(GameState.RoundRunning);
                yield return new RoundBuilder().Result(0, 1).Result(1, 2).Result(2, 3).Result(3, 1).Unfinished(1).Returns(GameState.RoundRunning);

                yield return new RoundBuilder(true).Result(0, 1).Result(1, 2).Result(2, 3).Result(3, 0).ToTestCaseData().Returns(GameState.GameFinished);
                yield return
                    new RoundBuilder().Result(0, 1)
                        .Result(1, 2)
                        .Result(2, 3)
                        .Result(3, 0)
                        .Result(0, 1)
                        .Result(1, 2)
                        .Result(2, 3)
                        .Result(3, 0)
                        .ToTestCaseData()
                        .Returns(GameState.GameFinished);
            }
        }

        [TestCaseSource("GameState_Source")]
        public GameState GameState_ReturnsCorrectly(MahjongGame game)
        {
            return game.State;
        }

        private IEnumerable<TestCaseData> NextRound_Source
        {
            get
            {
                yield return new RoundBuilder().ToTestCaseData().Returns(1);
                yield return new RoundBuilder().Result(0, 1).ToTestCaseData().Returns(2);
                yield return new RoundBuilder()
                    .Result(0, 1).Result(1, 2).Result(2, 3).Result(3, 0)
                    .ToTestCaseData().Returns(5);
            }
        }

        [TestCaseSource("NextRound_Source")]
        public int NextRound_AddsRoundCorrectly(MahjongGame game)
        {
            game.NextRound();
            return game.Rounds.Count;
        }

        private IEnumerable<TestCaseData> NextRound_Exception_Source
        {
            get
            {
                yield return new RoundBuilder().Unfinished(0).Throws(typeof(RoundRunningException));
                yield return new RoundBuilder().Result(0, 1).Unfinished(1).Throws(typeof(RoundRunningException));

                yield return new RoundBuilder(true)
                    .Result(0, 1).Result(1, 2).Result(2, 3).Result(3, 0)
                    .ToTestCaseData().Throws(typeof(GameOverException));
                yield return
                    new RoundBuilder().Result(0, 1)
                        .Result(1, 2)
                        .Result(2, 3)
                        .Result(3, 0)
                        .Result(0, 1)
                        .Result(1, 2)
                        .Result(2, 3)
                        .Result(3, 0)
                        .ToTestCaseData()
                        .Throws(typeof(GameOverException));
            }
        }

        [TestCaseSource("NextRound_Exception_Source")]
        public void NextRound_ThrowsExceptionWhenRoundRunningOrGameFinished(MahjongGame game)
        {
            game.NextRound();
        }

        private IEnumerable<TestCaseData> NextRound_Oya_Source
        {
            get
            {
                yield return new RoundBuilder().ToTestCaseData().Returns(0);
                yield return new RoundBuilder().Result(0, 1).ToTestCaseData().Returns(1);
                yield return new RoundBuilder()
                    .Result(0, 1).Result(1, 2).Result(2, 3)
                    .ToTestCaseData().Returns(3);
                yield return new RoundBuilder()
                    .Result(0, 1).Result(1, 2).Result(2, 3).Result(3, 0)
                    .ToTestCaseData().Returns(0);
            }
        }

        [TestCaseSource("NextRound_Oya_Source")]
        public int NextRound_UpdatesOyaCorrectly(MahjongGame game)
        {
            game.NextRound();
            return game.Rounds.Last().Oya;
        }
    }
}
