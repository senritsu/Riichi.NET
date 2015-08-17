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
using RiichiSharp.Domain;
using RiichiSharp.Rules;

namespace RiichiSharp.History
{
    public delegate void TileDrawnEventHandler(object sender, TileDrawnEventArgs e);

    public delegate void TileCalledEventHandler(object sender, TileCalledEventArgs e);

    public delegate void TileDiscardedEventHandler(object sender, TileDiscardedEventArgs e);

    public delegate void MeldFormedEventHandler(object sender, MeldFormedEventArgs e);

    #region abstract classes

    public abstract class PlayerActionEventArgs : EventArgs
    {
        public int Player { get; set; }
    }

    public abstract class TileEventArgs : PlayerActionEventArgs
    {
        public TileState Tile { get; set; }
    }

    #endregion

    public class TileDrawnEventArgs : TileEventArgs
    {
        public bool FromDeadWall { get; set; }
    }

    public class TileCalledEventArgs : TileEventArgs
    {
        public CallType Call { get; set; }
    }

    public class TileDiscardedEventArgs : TileEventArgs
    {
        public RiichiState RiichiState { get; set; }
    }

    public class MeldFormedEventArgs : PlayerActionEventArgs
    {
        public IReadOnlyList<TileState> Meld { get; set; }
        public bool Closed { get { return !Meld.Any(x => x.Open); } }
    }

    public class NewDoraRevealedEventArgs : TileEventArgs
    {
        public TileState Ura { get; set; }
    }
}
