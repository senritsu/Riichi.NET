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
using RiichiSharp.Analysis;
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

        private readonly List<RoundState> _rounds = new List<RoundState>();
        public IReadOnlyCollection<RoundState> Rounds { get { return _rounds; } }

        public RoundState CurrentRound { get { return Rounds.LastOrDefault(); } }

        public PlayerSpecificObject<MahjongPlayer> Players { get; private set; }
        public MahjongPlayer ActivePlayer { get; private set; }

        public PlayerSpecificValue<int> Points { get; set; }
        public int RiichiPoints { set; get; }

        public PlayerSpecificValue<bool> Yakitori { get; set; }

        public MahjongGame(bool tonpuusen = false)
        {
            Tonpuuseen = tonpuusen;
            Points = new PlayerSpecificValue<int>();
            Yakitori = new PlayerSpecificValue<bool>();
            Players = new PlayerSpecificObject<MahjongPlayer>(
                new MahjongPlayer(this, 0), new MahjongPlayer(this, 1),
                new MahjongPlayer(this, 2), new MahjongPlayer(this, 3));
        }

        public void DeclareDraw()
        {
            var result = new RoundResult();
            foreach (var player in Players)
            {
                result.Tenpai[player] = HandAnalyzer.Shanten(player.Hand, player.Melds) == 0;
            }
            FinishRound(result);
        }

        public void FinishRound(RoundResult result)
        {
            switch (State)
            {
                case GameState.Preparation:
                case GameState.BetweenRounds:
                    throw new NoRoundRunningException();
                case GameState.GameFinished:
                    throw new GameOverException();
            }

            CurrentRound.Result = result;
        }

        public void NextTurn()
        {
            switch (State)
            {
                case GameState.Preparation:
                case GameState.BetweenRounds:
                    throw new NoRoundRunningException();
                case GameState.GameFinished:
                    throw new GameOverException();
            }

            ActivePlayer = Players[(ActivePlayer + 1)%4];
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

            _rounds.Add(new RoundState
            {
                Oya = Oya,
            });
        }
    }

    public class RoundResult
    {
        public WinContext Context { get; set; }
        public Hand WinningHand { get; set; }
        public int Value { get; set; }

        public bool Draw { get { return !Winner.HasValue; } }

        public int? Winner { get; set; }
        public PlayerSpecificValue<bool> Tenpai { get; private set; }

        public RoundResult()
        {
            Tenpai = new PlayerSpecificValue<bool>();
        }
    }

    public class RoundState
    {
        public int Oya { get; set; }

        public Wind RoundWind
        {
            get { return (Wind) (Tile.Ton + Oya); }
        }

        public TileState LastDiscard { get { throw new NotImplementedException(); } }

        private readonly List<TileState> _wall = new List<TileState>();
        public IReadOnlyCollection<TileState> Wall { get { return _wall; } }

        private readonly List<TileState> _deadWall = new List<TileState>();
        public IReadOnlyCollection<TileState> DeadWall { get { return _deadWall; } }

        private readonly PlayerSpecificCollection<TileState> _ponds = new PlayerSpecificCollection<TileState>();
        public IPlayerSpecificReadOnlyCollection<TileState> Ponds { get { return _ponds; } }

        private readonly PlayerSpecificCollection<TileState> _hands = new PlayerSpecificCollection<TileState>();
        public IPlayerSpecificReadOnlyCollection<TileState> Hands { get { return _hands; } }

        private readonly PlayerSpecificCollection<TileState[]> _melds = new PlayerSpecificCollection<TileState[]>();
        public IPlayerSpecificReadOnlyCollection<TileState[]> Melds { get { return _melds; } }

        public List<Tile> Dora { get; set; }
        public List<Tile> Uradora { get; set; }
        
        public RoundResult Result { get; set; }

        private Tile DrawFromSource(MahjongPlayer player, IList<TileState> source)
        {
            if (!player.CanDraw)
            {
                throw new WrongTimingException();
            }

            var tile = source.Last();
            source.RemoveAt(source.Count - 1);
            _hands[player].Add(tile);
            return tile;
        }

        public Tile DrawFromWall(MahjongPlayer player)
        {
            return DrawFromSource(player, _wall);
        }

        public Tile DrawFromDeadWall(MahjongPlayer player)
        {
            return DrawFromSource(player, _deadWall);
        }

        public void RevealNextDora()
        {
            throw new NotImplementedException();
        }

        public void Discard(MahjongPlayer player, TileState tile)
        {
            if (!player.CanDiscard)
            {
                throw new WrongTimingException();
            }

            _hands[player].Remove(tile);
            _ponds[player].Add(tile);
        }
    }
}
