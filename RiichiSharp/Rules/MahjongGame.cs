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
using System.Diagnostics;
using System.Linq;
using RiichiSharp.Utilities;

namespace RiichiSharp.Rules
{
    public enum Wind
    {
        Ton = Tile.Ton,
        Nan = Tile.Nan,
        Xia = Tile.Xia,
        Pei = Tile.Pei
    }

    public enum GameState
    {
        Preparation,
        RoundRunning,
        BetweenRounds,
        GameFinished
    }

    public class MahjongGame
    {
        public bool Tonpuuseen { get; private set; }

        public GameState State
        {
            get
            {
                if (Rounds.Count == 0)
                {
                    return GameState.Preparation;
                }

                var last = Rounds.Last();

                if (last.Result == null)
                {
                    return GameState.RoundRunning;
                }

                var lastPlayerDealerCount = Rounds.Select(x => x.Oya).RemoveSequentialDuplicates().Count(x => x == 3);
                var lastPlayerLostOya = last.Oya == 3 && !last.Result.Draw && last.Result.Winner != 3;
                
                var finished = lastPlayerLostOya && lastPlayerDealerCount == (Tonpuuseen ? 1 : 2);
                return finished ? GameState.GameFinished : GameState.BetweenRounds;
            }
        }

        public int Oya
        {
            get
            {
                if (Rounds.Count == 0)
                {
                    return 0;
                }

                var last = Rounds.Last();

                if (last.Result == null)
                {
                    return last.Oya;
                }
                return (last.Result.Draw || last.Oya == last.Result.Winner) ? last.Oya : (last.Oya + 1)%4;
            }
        }

        public int Renchan
        {
            get
            {
                return
                    Rounds.ToArray()
                    .Reverse()
                    .Where(x => x.Result != null)
                    .TakeWhile(x => x.Oya == Rounds.Last().Oya && (x.Result.Winner == x.Oya || x.Result.Draw))
                    .Count();
            }
        }

        public List<RoundState> Rounds { get; set; }

        public int[] Points { get; set; }
        public int RiichiPoints { set; get; }

        public bool[] Yakitori { get; set; }

        public MahjongGame(bool tonpuusen = false)
        {
            Tonpuuseen = tonpuusen;
            Rounds = new List<RoundState>();
            Points = new int[4];
            Yakitori = new[] {false, false, false, false};
        }

        public void NextRound()
        {
            switch (State)
            {
                case GameState.RoundRunning:
                    throw new RoundRunningException();
                case GameState.GameFinished:
                    throw new GameOverException();
            }
        }
    }

    public class RoundResult
    {
        public WinContext Context { get; set; }
        public Hand WinningHand { get; set; }
        public int Value { get; set; }

        public bool Draw { get { return !Winner.HasValue; } }

        public int? Winner { get; set; }
        public bool[] Tenpai { get; set; }

        public RoundResult()
        {
            Tenpai = new bool[4];
        }
    }

    public class RoundState
    {
        public int Oya { get; set; }

        public Wind RoundWind { get; set; }

        public List<Tile> Dora { get; set; }
        public List<Tile> Uradora { get; set; }
        
        public RoundResult Result { get; set; }
    }
}
