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
using RiichiSharp.Utilities;

namespace RiichiSharp.Rules
{
    public class Round
    {
        public int Oya { get; set; }

        public Wind RoundWind
        {
            get { return (Wind)(Tile.Ton + Oya); }
        }

        public TileState LastDiscard { get { throw new NotImplementedException(); } }

        private readonly List<TileState> _wall = new List<TileState>();
        public IReadOnlyList<TileState> Wall { get { return _wall; } }

        private readonly List<TileState> _deadWall = new List<TileState>();
        public IReadOnlyList<TileState> DeadWall { get { return _deadWall; } }

        private readonly PlayerSpecificCollection<TileState> _ponds = new PlayerSpecificCollection<TileState>();
        public IPlayerSpecificReadOnlyCollection<TileState> Ponds { get { return _ponds; } }

        private readonly PlayerSpecificCollection<TileState> _hands = new PlayerSpecificCollection<TileState>();
        public IPlayerSpecificReadOnlyCollection<TileState> Hands { get { return _hands; } }

        private readonly PlayerSpecificCollection<TileState[]> _melds = new PlayerSpecificCollection<TileState[]>();
        public IPlayerSpecificReadOnlyCollection<TileState[]> Melds { get { return _melds; } }

        private readonly List<TileState> _dora = new List<TileState>();
        public IReadOnlyList<TileState> Dora { get { return _dora; } }

        private readonly List<TileState> _uradora = new List<TileState>();
        public IReadOnlyList<TileState> Uradora { get { return _uradora; } }

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

        public TileState RevealNextDora()
        {
            var i = 9 - Dora.Count * 2;

            var dora = DeadWall[i];
            var uradora = DeadWall[i - 1];

            _dora.Add(dora);
            _uradora.Add(uradora);

            dora.Open = true;
            return dora;
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
