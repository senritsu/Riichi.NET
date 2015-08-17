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
using RiichiSharp.Enums;

namespace RiichiSharp.Rules
{
    public class MahjongPlayer
    {
        private readonly MahjongGame _game;
        public int Seat { get; private set; }

        public bool CanDraw
        {
            get { return _game.ActivePlayer == this && Hand.Count + Melds.NormalizedTileCount() < 14; }
        }

        public bool CanDiscard
        {
            get { return _game.ActivePlayer == this && Hand.Count + Melds.NormalizedTileCount() == 14; }
        }

        public bool CanCall
        {
            get { return Hand.Count + Melds.NormalizedTileCount() < 14; }
        }

        public IEnumerable<IReadOnlyCollection<TileState>> PossibleCalls
        {
            get
            {
                var pond = _game.CurrentRound.Ponds[CanDraw ? (Seat + 4 - 1)%4 : Seat];
                return Hand.PossibleMelds(pond.Last());
            }
        }

        public int Points { get { return _game.Points[this]; } }
        public bool Yakitori { get { return _game.Yakitori[this]; } }
        public bool Oya { get { return _game.Oya == this; } }
        public bool Open { get { return Hand.Any(x => x.Open); } }

        public IReadOnlyCollection<TileState> Hand
        {
            get { return _game.State == GameState.Preparation ? null : _game.CurrentRound.Hands[Seat]; }
        }

        public IReadOnlyCollection<TileState> Pond
        {
            get { return _game.State == GameState.Preparation ? null : _game.CurrentRound.Ponds[Seat]; }
        }

        public IReadOnlyCollection<TileState[]> Melds
        {
            get { return _game.State == GameState.Preparation ? null : _game.CurrentRound.Melds[Seat]; }
        }

        public MahjongPlayer(MahjongGame game, int seat)
        {
            if (seat < 0 || seat > 3)
            {
                throw new ArgumentOutOfRangeException("seat");
            }

            _game = game;
            Seat = seat;
        }

        public Tile Draw()
        {
            if (_game.CurrentRound.Wall.Count == 0)
            {
                _game.DeclareDraw();
            }
            return _game.CurrentRound.DrawFromWall(this);
        }

        public void Discard(TileState tile)
        {
            _game.CurrentRound.Discard(this, tile);
            _game.NextTurn();
        }

        public void Call(TileState[] tiles)
        {
            throw new NotImplementedException();
        }

        public void DefaultAction()
        {
            if (CanDraw)
            {
                Draw();
            }
            if (CanDiscard)
            {
                
                Discard(Hand.Last());
            }

            throw new WrongTimingException();
        }

        public static implicit operator int(MahjongPlayer player)
        {
            return player.Seat;
        }
    }
}
