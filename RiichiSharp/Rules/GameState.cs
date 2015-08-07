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
using System.Security.Cryptography.X509Certificates;

namespace RiichiSharp.Rules
{
    public enum Wind
    {
        Ton = Tile.Ton,
        Nan = Tile.Nan,
        Xia = Tile.Xia,
        Pei = Tile.Pei
    }

    public class GameState
    {
        public bool Tonpuuseen { get; set; }

        public int Oyarenchan
        {
            get
            {
                return
                    Rounds.ToArray()
                    .Reverse()
                    .Where(x => x.Result != null)
                    .TakeWhile(x =>
                    {
                        Debug.WriteLine("Oya: {0}, Current Oya: {1}, Winner: {2}, Draw: {3}", x.Oya, Rounds.Last().Oya, x.Result.Winner, x.Result.Draw);
                        return x.Oya == Rounds.Last().Oya && (x.Result.Winner == x.Oya || x.Result.Draw);
                    })
                    .Count();
            }
        }

        public List<RoundState> Rounds { get; set; }

        public int[] Points { get; set; }
        public int RiichiPoints { set; get; }

        public bool[] Yakitori { get; set; }

        public GameState()
        {
            Rounds = new List<RoundState>();
            Points = new int[4];
            Yakitori = new[] {false, false, false, false};
        }
    }

    public class RoundResult
    {
        public WinContext Context { get; set; }
        public Hand WinningHand { get; set; }
        public int Value { get; set; }

        public bool Draw { get; set; }
        public int Winner { get; set; }
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
